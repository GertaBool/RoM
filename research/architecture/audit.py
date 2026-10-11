#!/usr/bin/env python3
"""Measure pinned source structure and execute narrow architecture contracts.

Reads Git objects, without changing the source checkout. Native probes execute
unchanged method bodies with explicit service stubs, not the BTS executable.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import types

BASE = '1ab4f99a76adb530f86b278390ab8139ef41cc96'
NATIVE = 'Assets/CvGameCoreDLL/'


def mask(text):
    # Legacy C++ strings/chars/comments; preserves offsets and newlines.
    pattern = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*[\s\S]*?\*/|//[^\n]*'
    return re.sub(pattern, lambda m: re.sub(r'[^\n]', ' ', m[0]), text)


def extract(text, signature):
    clean = mask(text)
    start = clean.index(signature)
    opening = clean.index('{', start)
    depth, end = 1, opening + 1
    while depth:
        depth += (clean[end] == '{') - (clean[end] == '}')
        end += 1
    return text[start:end], start


def sites(clean):
    return {name: len(re.findall(pattern, clean)) for name, pattern in {
        'GC_accesses': r'\bGC\s*\.',
        'gDLL_accesses': r'\bgDLL\s*->',
        'GET_PLAYER_calls': r'\bGET_PLAYER\s*\(',
        'GET_TEAM_calls': r'\bGET_TEAM\s*\(',
        'gameplay_rng_calls': r'\bgetSorenRandNum\s*\(',
        'generatePath_calls': r'\bgeneratePath\s*\(',
    }.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--revision', default=BASE)
    parser.add_argument('--compare-ref', help='verify probe bodies are unchanged in this revision')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('evidence.json'))
    args = parser.parse_args()

    def git(*command):
        return subprocess.check_output(['git', '-C', str(args.source), *command])

    revision = git('rev-parse', args.revision + '^{commit}').decode().strip()
    compare = git('rev-parse', args.compare_ref + '^{commit}').decode().strip() if args.compare_ref else None
    texts, hashes, fragments = {}, {}, []

    def read(path):
        if path not in texts:
            raw = git('show', revision + ':' + path)
            texts[path] = raw.decode('latin1').replace('\r\n', '\n')
            hashes[path] = hashlib.sha256(raw).hexdigest()
        return texts[path]

    def fragment(path, signature):
        body, start = extract(read(path), signature)
        row = {'path': path, 'signature': signature,
               'start_line': read(path).count('\n', 0, start) + 1,
               'physical_lines': len(body.splitlines()),
               'sha256_normalized_fragment': hashlib.sha256(body.encode()).hexdigest()}
        if compare:
            other = git('show', compare + ':' + path).decode('latin1').replace('\r\n', '\n')
            row['unchanged_in_comparison_revision'] = extract(other, signature)[0] == body
        fragments.append(row)
        return body

    paths = git('ls-tree', '-r', '--name-only', revision, NATIVE).decode().splitlines()
    paths = [p for p in paths if Path(p).parent.as_posix() == NATIVE.rstrip('/')
             and Path(p).suffix in {'.cpp', '.h', '.inl'}]
    files = []
    for path in paths:
        source = read(path)
        clean = mask(source)
        files.append(dict(path=path, physical_lines=len(source.splitlines()),
                          nonblank_lines_after_comment_literal_mask=sum(bool(x.strip()) for x in clean.splitlines()),
                          **sites(clean)))

    selected = {
        'CvPlayerAI.cpp': ['void CvPlayerAI::AI_doDiplo(', 'int CvPlayerAI::AI_techValue(',
                           'void CvPlayerAI::AI_updateAgenda(', 'void CvPlayerAI::AI_doCentralizedProduction(',
                           'int CvPlayerAI::AI_getOperationRoleTarget('],
        'CvCityAI.cpp': ['void CvCityAI::AI_chooseProduction(', 'int CvCityAI::AI_buildingValueThreshold(',
                         'bool CvCityAI::AI_chooseBuilding('],
        'CvUnitAI.cpp': ['void CvUnitAI::AI_attackMove(', 'bool CvUnitAI::AI_operationMove('],
        'CvPlayer.cpp': ['void CvPlayer::doTurn(', 'void CvPlayer::setTurnActive(',
                         'int CvPlayer::findPathLength(', 'bool CvPlayer::pushResearch('],
        'CvGame.cpp': ['void CvGame::doTurn('],
    }
    functions = []
    for file, signatures in selected.items():
        for signature in signatures:
            body = fragment(NATIVE + file, signature)
            clean = mask(body)
            functions.append(dict(fragments[-1], return_statements=len(re.findall(r'\breturn\b', clean)),
                                  if_tokens=len(re.findall(r'\bif\s*\(', clean)), **sites(clean)))

    flags = ['-std=c++03', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined',
             '-fno-sanitize-recover=undefined']

    def compile_run(program):
        with tempfile.TemporaryDirectory(prefix='rom-architecture-') as folder:
            cpp, binary = Path(folder)/'probe.cpp', Path(folder)/'probe'
            cpp.write_text(program)
            subprocess.run(['g++', *flags, str(cpp), '-o', str(binary)], check=True)
            return json.loads(subprocess.check_output([str(binary)], text=True))

    probe_fragment_start = len(fragments)
    rng_method = fragment(NATIVE + 'CvPlayerAI.cpp', 'int CvPlayerAI::AI_getStrategyRand() const')
    rng_result = compile_run(RNG_ADAPTER.replace('ACTUAL_METHOD', rng_method))
    assert rng_result == {'first_const_query_draws': 1, 'repeated_const_query_draws': 0,
                          'without_diagnostic_next_draw': 1, 'with_diagnostic_next_draw': 2}

    path_method = fragment(NATIVE + 'CvSelectionGroup.cpp', 'bool CvSelectionGroup::generatePath(')
    last_method = fragment(NATIVE + 'CvSelectionGroup.cpp', 'FAStarNode* CvSelectionGroup::getPathLastNode() const')
    path_result = compile_run(PATH_ADAPTER.replace('ACTUAL_METHODS', path_method + '\n' + last_method))
    assert path_result == {'group_A_copied_endpoint_x': 7, 'group_A_accessor_after_B_x': 11,
                           'group_B_endpoint_x': 11, 'shared_pathfinder': True}

    event_path = 'Assets/Python/BUG/BugEventManager.py'
    event_text = read(event_path)
    start = event_text.index('\tdef _handleDefaultEvent(')
    end = event_text.index('\n\tdef ', start + 1)
    method = event_text[start:end]
    event_fragment = {'path': event_path, 'signature': 'def _handleDefaultEvent(',
                      'start_line': event_text.count('\n', 0, start) + 1,
                      'sha256_normalized_fragment': hashlib.sha256(method.encode()).hexdigest()}
    if compare:
        other = git('show', compare + ':' + event_path).decode('latin1').replace('\r\n', '\n')
        event_fragment['unchanged_in_comparison_revision'] = method in other
    fragments.append(event_fragment)
    errors = []
    namespace = {'BugUtil': types.SimpleNamespace(trace=lambda *args: errors.append(args[0]))}
    exec(textwrap.dedent(method), namespace)
    class LegacyMap(dict):
        def has_key(self, key):
            return key in self
    state, order = {'gold': 10}, []
    def first(args):
        state['gold'] += 5
        order.append('mutate_then_raise')
        raise ValueError('controlled probe failure')
    def second(args):
        order.append('later_handler')
        state['gold'] *= 2
    manager = types.SimpleNamespace(EventHandlerMap=LegacyMap(event=[first, second]))
    namespace['_handleDefaultEvent'](manager, 'event', [])
    assert state['gold'] == 30 and order == ['mutate_then_raise', 'later_handler'] and len(errors) == 1
    event_result = {'initial_gold': 10, 'final_gold': state['gold'], 'handler_order': order,
                    'logged_exceptions': len(errors), 'exception_propagated': False}

    policy_files = [f for f in files if re.fullmatch(r'AI.*Policy\.h', Path(f['path']).name)]
    result = {
        'source_repository': 'https://gitlab.com/aretemaxxing-group/rise-of-mankind',
        'source_revision': revision, 'comparison_revision': compare,
        'scope': 'Pinned Git objects; lexical structural measurements and source-fragment contracts with service stubs. No host execution, full DLL build, engine equivalence, or measured campaign defect.',
        'metric_definition': 'Direct children of Assets/CvGameCoreDLL with .cpp/.h/.inl suffix; excludes vendor subdirectories. Physical lines include comments/blanks. Token counts mask comments/literals but do not preprocess conditional compilation or infer runtime call frequency. Selected functions are explicitly enumerated, not all functions.',
        'native_file_count': len(files), 'native_physical_lines': sum(f['physical_lines'] for f in files),
        'top_translation_units': sorted([f for f in files if f['path'].endswith('.cpp')], key=lambda f: -f['physical_lines'])[:12],
        'policy_headers': policy_files, 'selected_functions': functions,
        'probes': [
            {'id': 'A01', 'title': 'A const strategy getter lazily consumes gameplay randomness', 'result': rng_result,
             'adapter_boundary': 'Counter stub for getSorenRandNum establishes calls and ordering; it does not emulate CvRandom or demonstrate an actual network desync.'},
            {'id': 'A02', 'title': 'Group path accessors reference the shared most-recent host path', 'result': path_result,
             'adapter_boundary': 'Single-buffer host stub records SetData/GeneratePath/GetLastNode. Tests DLL wrapper ownership and interleaving contract, not host path costs or a proven faulty game call sequence.'},
            {'id': 'A03', 'title': 'A failed ordinary Python event handler leaves mutations and later handlers execute', 'result': event_result,
             'adapter_boundary': 'Unchanged dispatcher method runs in Python 3 with a Python-2-compatible has_key adapter; controlled handlers and logging stub. Does not boot BUG, Python 2.4, or the native bridge.'},
        ],
        'compiler': subprocess.check_output(['g++', '--version'], text=True).splitlines()[0],
        'compiler_flags': flags, 'probe_fragments': fragments,
        'source_file_sha256': hashes,
        'audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    if compare:
        assert all(f['unchanged_in_comparison_revision'] for f in fragments[probe_fragment_start:]), 'An executed probe fragment changed'
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    for probe in result['probes']:
        print(probe['id'], json.dumps(probe['result']))
    for function in functions:
        print(function['signature'], function['physical_lines'], 'lines;', function['return_statements'], 'returns')
    print('Measured', len(files), 'native files and', len(policy_files), 'policy headers. All three contract probes passed.')


RNG_ADAPTER = r'''
#include <cassert>
#include <iostream>
struct Game {
    int calls;
    Game(): calls(0) {}
    int getSorenRandNum(int bound, const char*) { ++calls; return calls % bound; }
};
struct Globals { Game game; Game& getGameINLINE() { return game; } } GC;
struct CvPlayerAI {
    mutable int m_iStrategyRand;
    CvPlayerAI(): m_iStrategyRand(0) {}
    int AI_getStrategyRand() const;
};
ACTUAL_METHOD
int main() {
    const CvPlayerAI player;
    assert(GC.game.calls == 0);
    const int first = player.AI_getStrategyRand();
    const int afterFirst = GC.game.calls;
    assert(first == player.AI_getStrategyRand());
    const int repeat = GC.game.calls - afterFirst;
    GC.game.calls = 0;
    const int normal = GC.game.getSorenRandNum(100, "unrelated gameplay");
    GC.game.calls = 0;
    const CvPlayerAI observed;
    observed.AI_getStrategyRand();
    const int diagnosed = GC.game.getSorenRandNum(100, "unrelated gameplay");
    std::cout << "{\"first_const_query_draws\":" << afterFirst
              << ",\"repeated_const_query_draws\":" << repeat
              << ",\"without_diagnostic_next_draw\":" << normal
              << ",\"with_diagnostic_next_draw\":" << diagnosed << "}\n";
}
'''

PATH_ADAPTER = r'''
#include <cassert>
#include <climits>
#include <cstddef>
#include <iostream>
#define MAX_INT INT_MAX
#define PROFILE(x)
struct FAStarNode { int m_iData2, m_iX, m_iY; };
struct FAStar { FAStarNode last; const void* actor; };
struct CvPlot {
    int x,y;
    int getX_INLINE()const{return x;} int getY_INLINE()const{return y;}
};
struct Globals { FAStar finder; FAStar& getPathFinder(){return finder;} } GC;
struct HostPath {
    void SetData(FAStar* finder,const void* actor){finder->actor=actor;}
    bool GeneratePath(FAStar* finder,int,int,int x,int y,bool,int,bool){
        finder->last.m_iX=x;finder->last.m_iY=y;finder->last.m_iData2=1;return true;
    }
    FAStarNode* GetLastNode(FAStar* finder){return &finder->last;}
};
struct DLL { HostPath path; HostPath* getFAStarIFace(){return &path;} } dll;
DLL* gDLL=&dll;
struct CvSelectionGroup {
    bool generatePath(const CvPlot*,const CvPlot*,int,bool,int*)const;
    FAStarNode* getPathLastNode()const;
};
ACTUAL_METHODS
int main(){
    const CvSelectionGroup a,b;CvPlot start={0,0},targetA={7,0},targetB={11,0};
    int turns=0;
    assert(a.generatePath(&start,&targetA,0,false,&turns));
    assert(turns==1 && GC.finder.actor==&a);
    const FAStarNode copy=*a.getPathLastNode();
    assert(b.generatePath(&start,&targetB,0,false,&turns));
    assert(GC.finder.actor==&b);
    assert(a.getPathLastNode()==b.getPathLastNode());
    std::cout << "{\"group_A_copied_endpoint_x\":" << copy.m_iX
              << ",\"group_A_accessor_after_B_x\":" << a.getPathLastNode()->m_iX
              << ",\"group_B_endpoint_x\":" << b.getPathLastNode()->m_iX
              << ",\"shared_pathfinder\":true}\n";
}
'''

if __name__ == '__main__':
    main()
