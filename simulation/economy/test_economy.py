#!/usr/bin/env python3
"""Native-fragment differential tests; not an engine replay or gameplay benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile
import unittest

from run import HERE, compile_runner, execute, encode
from native_oracle import HOST, compile_oracle, verify_contract

SOURCE = None
RESULTS = {}

def growth(name, **changes):
    state = dict(population=2,food=8,food_kept=4,threshold=24,kept_percent=50,
                 food_yield=7,consumption=4,food_production=0,disorder=0,avoid_growth=0,callback=0)
    state.update(changes)
    return dict(id=name,phase='growth',snapshot=state)

def production(name, **changes):
    state = dict(progress=0,needed=40,base_production=3,total_modifier=150,
                 food_yield=7,consumption_no_angry=4,overflow=0,feature=0,
                 food_production=0,disorder=0,callback=0,choice_required=0,
                 process=0,has_order=1,allow_no_production=0)
    state.update(changes)
    return dict(id=name,phase='production',snapshot=state)

def completion(name, **changes):
    state = dict(progress=43,needed=40,current_production_no_overflow=4,total_modifier=150,
                 base_modifier=100,gold_percent=50,overflow=0)
    state.update(changes)
    return dict(id=name,phase='unit_completion',snapshot=state)

FIXTURES = [
    (completion('unit_overflow_normalized'),dict(status='unit_creation_required',progress=0,overflow=2,gold=0)),
    (completion('unit_cap_and_gold_rounding',progress=37,needed=5,current_production_no_overflow=10),dict(status='unit_creation_required',progress=0,overflow=6,gold=7)),
    (completion('unit_no_excess',progress=40),dict(status='unit_creation_required',progress=0,overflow=0,gold=0)),
    (completion('unit_zero_modifier',total_modifier=0),dict(status='unit_creation_required',progress=0,overflow=300,gold=0)),
    (completion('unit_existing_overflow',overflow=7),dict(status='unit_creation_required',progress=0,overflow=9,gold=0)),
    (growth('ordinary_growth'),dict(status='applied',population=2,food=11,food_kept=7,difference=3,grew=0)),
    (growth('granary_growth',food=23,food_kept=11),dict(status='population_effects_required',population=3,food=14,food_kept=12,difference=3,grew=1)),
    (growth('avoid_growth',food=23,avoid_growth=1),dict(status='applied',population=2,food=24,food_kept=7,difference=3,grew=0)),
    (growth('starvation',food=1,food_kept=1,food_yield=1),dict(status='population_effects_required',population=1,food=0,food_kept=0,difference=-3,grew=0)),
    (growth('population_one_floor',population=1,food=0,food_yield=0),dict(status='applied',population=1,food=0,food_kept=4,difference=0,grew=0)),
    (growth('settler_stops_food_storage',food_production=1),dict(status='applied',population=2,food=8,food_kept=4,difference=0,grew=0)),
    (growth('settler_can_still_starve',food_production=1,food=1,food_yield=1),dict(status='population_effects_required',population=1,food=0,food_kept=1,difference=-3,grew=0)),
    (growth('disorder_freezes_difference',disorder=1),dict(status='applied',population=2,food=8,food_kept=4,difference=0,grew=0)),
    (growth('stored_food_can_grow_in_disorder',disorder=1,food=24),dict(status='population_effects_required',population=3,food=4,food_kept=4,difference=0,grew=1)),
    (production('production_rounds_once'),dict(status='applied',progress=4,overflow=0,feature=0,difference=4)),
    (production('food_not_production_multiplied',food_production=1),dict(status='applied',progress=7,overflow=0,feature=0,difference=7)),
    (production('ignore_angry_for_food_production',food_production=1,consumption_no_angry=2),dict(status='applied',progress=9,overflow=0,feature=0,difference=9)),
    (production('overflow_and_chop_multiplied',overflow=2,feature=3),dict(status='applied',progress=12,overflow=0,feature=0,difference=12)),
    (production('completion_boundary',progress=39),dict(status='completion_effects_required',progress=43,overflow=0,feature=0,difference=4)),
    (production('disorder_preserves_overflow',overflow=2,feature=3,disorder=1),dict(status='applied',progress=0,overflow=2,feature=3,difference=0)),
    (production('idle_normalizes_overflow',has_order=0,allow_no_production=1,overflow=2,feature=3),dict(status='applied',progress=0,overflow=4,feature=3,difference=4)),
    (production('idle_disallowed',has_order=0,overflow=2,feature=3),dict(status='applied',progress=0,overflow=2,feature=3,difference=0)),
    (production('zero_modifier_food_only',total_modifier=0,food_production=1),dict(status='applied',progress=3,overflow=0,feature=0,difference=3)),
]

class EconomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='rom-native-economy-')
        cls.directory = Path(cls.temp.name)
        cls.runner = cls.directory/'kernel'
        compile_runner(cls.runner,sanitize=True)
        cls.oracle = compile_oracle(SOURCE,cls.directory)

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def test_named_native_cases(self):
        records = [x[0] for x in FIXTURES]
        actual = execute(self.runner,records)
        native = execute(self.oracle,records)
        for (record,want),got,reference in zip(FIXTURES,actual,native):
            self.assertEqual(got['result'],want,record['id'])
            self.assertEqual(got,reference,record['id'])
        RESULTS['named_cases'] = actual

    def test_seeded_native_differential(self):
        rng = random.Random(912621);records=[]
        for n in range(5000):
            records.append(growth('g'+str(n),population=rng.randint(1,30),food=rng.randint(0,250),
                food_kept=rng.randint(0,100),threshold=rng.randint(1,200),kept_percent=rng.randint(0,150),
                food_yield=rng.randint(0,100),consumption=rng.randint(0,100),food_production=rng.randrange(2),
                disorder=rng.randrange(2),avoid_growth=rng.randrange(2)))
            records.append(production('p'+str(n),progress=rng.randint(0,500),needed=rng.randint(1,500),
                base_production=rng.randint(0,100),total_modifier=rng.randint(0,400),food_yield=rng.randint(0,100),
                consumption_no_angry=rng.randint(0,100),overflow=rng.randint(0,100),feature=rng.randint(0,100),
                food_production=rng.randrange(2),disorder=rng.randrange(2),has_order=rng.randrange(2),
                allow_no_production=rng.randrange(2)))
        self.assertEqual(execute(self.runner,records),execute(self.oracle,records))
        RESULTS['random_differential_cases']=len(records)
        RESULTS['random_seed']=912621

    def test_unsupported_is_explicit_and_transactional(self):
        records=[growth('growth_callback',callback=1), production('production_callback',callback=1),
                 production('needs_choice',choice_required=1,disorder=1),production('process',process=1)]
        statuses=['callback_unsupported','callback_unsupported','production_choice_required','process_unsupported']
        for record,out,want in zip(records,execute(self.runner,records),statuses):
            result=out['result'];self.assertEqual(result['status'],want)
            for key in ('food','food_kept','population') if record['phase']=='growth' else ('progress','overflow','feature'):
                self.assertEqual(result[key],record['snapshot'][key])
            self.assertEqual(result['difference'],0)

    def test_rejects_native_overflow_before_clamps(self):
        top=2**31-1
        records=[growth('food_add',food=top),growth('kept_add',food_kept=top),
                 growth('cap_product',threshold=top,kept_percent=100),
                 growth('population_add',population=top,food=24),
                 production('combined_overflow',overflow=top,feature=top),
                 production('base_add',overflow=top),production('multiply',base_production=top),
                 production('progress_add',progress=top),
                 production('idle_conversion',has_order=0,allow_no_production=1,total_modifier=1,base_production=top,food_production=1,food_yield=top),
                 production('idle_accumulate',has_order=0,allow_no_production=1,overflow=top)]
        for record,out in zip(records,execute(self.runner,records)):
            self.assertEqual(out['result']['status'],'native_arithmetic_range',record['id'])
            self.assertEqual(out['result']['difference'],0)
        # The source's nonnegative subtractions and zero multiplier remain safe at INT_MAX.
        safe=[growth('wide_safe_growth',threshold=top,kept_percent=0,food_yield=0,consumption=top),
              production('wide_safe_production',base_production=top,total_modifier=0)]
        self.assertEqual(execute(self.runner,safe),execute(self.oracle,safe))

    def test_invalid_inputs_and_wire_format(self):
        records=[growth('bad_pop',population=0),growth('bad_flag',disorder=2),
                 production('bad_progress',progress=-1),production('bad_flag_p',has_order=2)]
        for out in execute(self.runner,records):self.assertEqual(out['result']['status'],'invalid_snapshot')
        for wire in ['','G 1\n','P x\n','X 1\n','G 1 0 0 20 0 2 2 0 0 0 0 extra\n']:
            if not wire:wire='\n'
            result=subprocess.run([str(self.runner)],input=wire,text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
        for change in [dict(food=2**31),dict(food=True),dict(extra=1)]:
            record=growth('bad_json');record['snapshot'].update(change)
            with self.assertRaises(ValueError):encode(record)

    def test_population_change_can_invalidate_production_rates(self):
        # Explicit supplied yields after the population boundary, NOT an inferred allocation.
        g=growth('grow_then_refresh',food=23)
        grown=execute(self.runner,[g])[0]['result']
        self.assertEqual(grown['status'],'population_effects_required')
        stale=production('stale',base_production=3,total_modifier=100)
        fresh=production('fresh_supplied_after_population_and_culture',base_production=5,total_modifier=100)
        actual=execute(self.runner,[stale,fresh])
        self.assertEqual([r['result']['difference'] for r in actual],[3,5])
        self.assertEqual(actual,execute(self.oracle,[stale,fresh]))

    def test_stock_sequences_until_boundary(self):
        # Fixed getters are an explicit fixture assumption, valid only until stopped.
        g=growth('growth_sequence',food=0,food_kept=0)
        p=production('production_sequence',needed=20)
        for record,keys in [(g,('food','food_kept','population')),(p,('progress','overflow','feature'))]:
            for tick in range(20):
                native=execute(self.oracle,[record]);actual=execute(self.runner,[record])
                self.assertEqual(actual,native)
                out=actual[0]['result']
                if out['status']!='applied':break
                for key in keys:record['snapshot'][key]=out[key]
            else:self.fail('expected finite growth/production boundary')

    def test_unit_completion_native_differential(self):
        rng=random.Random(912622);records=[]
        for i in range(5000):
            cost=rng.randint(1,1000)
            records.append(completion('u'+str(i),progress=cost+rng.randint(0,3000),needed=cost,
                current_production_no_overflow=rng.randint(0,1000),total_modifier=rng.randint(0,500),
                base_modifier=rng.randint(0,500),gold_percent=rng.randint(0,100),overflow=rng.randint(0,500)))
        self.assertEqual(execute(self.runner,records),execute(self.oracle,records))
        RESULTS['random_unit_completion_cases']=len(records)
        RESULTS['unit_completion_seed']=912622

    def test_unit_completion_rejects_undefined_arithmetic(self):
        top=2**31-1
        records=[completion('normalization',needed=0,progress=top,current_production_no_overflow=top),
                 completion('lost_scaling',needed=0,progress=top,current_production_no_overflow=0),
                 completion('overflow_add',overflow=top),
                 completion('gold_product',progress=1000,needed=1,current_production_no_overflow=1,gold_percent=top)]
        for record,out in zip(records,execute(self.runner,records)):
            self.assertEqual(out['result']['status'],'native_arithmetic_range',record['id'])
            self.assertEqual(out['result']['progress'],record['snapshot']['progress'])
            self.assertEqual(out['result']['gold'],0)
        for record in [completion('not_finished',progress=39),completion('negative',overflow=-1)]:
            self.assertEqual(execute(self.runner,[record])[0]['result']['status'],'invalid_snapshot')

    def test_unit_overflow_feeds_next_build_once(self):
        p=production('last_tick',progress=39)
        accrued=execute(self.runner,[p])[0]['result']
        self.assertEqual(accrued['status'],'completion_effects_required')
        u=completion('finish_accounting',progress=accrued['progress'],overflow=accrued['overflow'])
        ended=execute(self.runner,[u])[0]['result']
        self.assertEqual(ended['status'],'unit_creation_required')
        # Caller supplies the next snapshot only after resolving unit creation/queue effects.
        next_build=production('next_build',total_modifier=100,overflow=ended['overflow'])
        next_result=execute(self.runner,[next_build])[0]['result']
        self.assertEqual(next_result['difference'],5)
        next_build['snapshot'].update(progress=next_result['progress'],overflow=next_result['overflow'])
        self.assertEqual(execute(self.runner,[next_build])[0]['result']['difference'],3)
        self.assertEqual(execute(self.runner,[p,u,next_build]),execute(self.oracle,[p,u,next_build]))

    def test_adapter_detects_native_reselection_boundary(self):
        cpp=self.directory/'adapter.cpp';exe=self.directory/'adapter'
        cpp.write_text(HOST+r'''
int main(){
 CvCity city;city.phase='P';city.p.needed=40;city.p.hasOrder=1;city.p.totalModifier=100;
 assert(!captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.human=false;
 assert(!captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.dirty=true;
 assert(captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.dirty=false;city.p.hasOrder=0;
 assert(captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.p.hasOrder=1;city.p.process=1;
 assert(captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.human=true;city.p.process=0;city.dirty=true;
 assert(!captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 city.automated=true;
 assert(captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,false).choiceRequired);
 assert(captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,true,false).callback);
}
''')
        subprocess.run(['g++','-std=c++03','-Wall','-Wextra','-Werror','-fsanitize=undefined',
            '-fno-sanitize-recover=undefined','-I',str(HERE),str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True)

    def test_source_changes_require_contract_review(self):
        folder=self.directory/'altered';path=folder/'Assets/CvGameCoreDLL/CvCity.cpp'
        path.parent.mkdir(parents=True)
        text=(SOURCE/'Assets/CvGameCoreDLL/CvCity.cpp').read_text()
        path.write_text(text.replace('int iFoodProduction = ((bFoodProduction)', 'int iFoodProduction = 0 + ((bFoodProduction)',1))
        with self.assertRaisesRegex(ValueError,'native method changed'):verify_contract(folder)


def main():
    global SOURCE
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=HERE/'results.json')
    args=parser.parse_args();SOURCE=args.source.resolve()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EconomyTests)
    outcome=unittest.TextTestRunner(verbosity=2).run(suite)
    if not outcome.wasSuccessful():raise SystemExit(1)
    RESULTS.update(scope='Arithmetic and stop boundaries compared with six extracted native methods and unit-completion arithmetic; not a DLL replay',
        tests_run=outcome.testsRun,compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
        flags='C++03, Wall/Wextra/Werror, O1, fatal UBSan; native fragments suppress unused-parameter warnings',
        artifact_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*'))
                         if p.is_file() and p.suffix in ('.h','.cpp','.py')},
        source_contract_sha256=hashlib.sha256((HERE/'source_contract.json').read_bytes()).hexdigest(),
        unsupported_engine_work=['population/citizen effects','culture and plot ownership','order completion and callbacks',
                                 'trade/maintenance/research','worker travel and improvement completion','whole-turn orchestration'])
    args.output.write_text(json.dumps(RESULTS,indent=2)+'\n')

if __name__=='__main__':main()
