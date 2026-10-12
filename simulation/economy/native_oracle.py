"""Compile pinned native methods with explicit getter/side-effect adapters.

This is a source-fragment oracle. Native population and order-completion effects
are stopping boundaries, not stubbed successes. No engine equivalence is claimed.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
SIGNATURES = [
    'int CvCity::foodDifference(bool bBottom) const',
    'void CvCity::doGrowth()',
    'int CvCity::getProductionDifference(',
    'int CvCity::getCurrentProductionDifference(',
    'void CvCity::changeOverflowProduction(',
    'void CvCity::doProduction(bool bAllowNoProduction)',
]

def block(text, signature):
    start = text.index(signature)
    masked = re.sub(r'"(?:\\.|[^"\\])*"|/\*[\s\S]*?\*/|//[^\n]*',
                    lambda m: re.sub(r'[^\n]', ' ', m[0]), text)
    begin = masked.index('{', start)
    depth, end = 1, begin + 1
    while depth:
        depth += (masked[end] == '{') - (masked[end] == '}')
        end += 1
    return text[start:end]

UNIT_FRAGMENT = 'unit completion arithmetic before initUnit in CvCity::popOrder'

def extract(source):
    text = (source/'Assets/CvGameCoreDLL/CvCity.cpp').read_text()
    methods = {signature: block(text, signature) for signature in SIGNATURES}
    order = block(text, 'void CvCity::popOrder(')
    begin = order.index('iProductionNeeded = getProductionNeeded(eTrainUnit);')
    end = order.index('pUnit = GET_PLAYER(getOwnerINLINE()).initUnit', begin)
    methods[UNIT_FRAGMENT] = order[begin:end]
    return methods

def verify_contract(source):
    methods = extract(source)
    contract = json.loads((HERE/'source_contract.json').read_text())
    for signature, code in methods.items():
        if hashlib.sha256(code.encode()).hexdigest() != contract['methods'][signature]['sha256_lf']:
            raise ValueError('native method changed; review the adapter before updating its contract: '+signature)
    return methods

HOST = r'''
#include "city_economy.h"
#include "snapshot_adapter.h"
#include <algorithm>
#include <cassert>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
using namespace CityEconomy;
enum YieldTypes { YIELD_FOOD, YIELD_PRODUCTION };
struct PopulationBoundary {};
struct CompletionBoundary {};
template<class T> T range(T value,T low,T high){return std::max(low,std::min(value,high));}
struct CvCity;
struct CyCity { explicit CyCity(CvCity*) {} };
struct CyArgsList {void add(int){} int makeFunctionArgs(){return 0;}};
struct Python {int makePythonObject(CyCity*){std::abort();}
 void callFunction(const char*,const char*,int,long*){std::abort();}};
struct DLL {Python* getPythonIFace(){std::abort();}};
DLL* gDLL = NULL;
const char* PYGameModule = "not-executed";
int unitGoldPercent=0;
struct Globals {int getDefineINT(const char*){return unitGoldPercent;}
 bool getUSE_CAN_DO_GROWTH_CALLBACK(){return false;}
 bool getUSE_CAN_DO_PRODUCTION_CALLBACK(){return false;}} GC;
struct CvEventReporter {static CvEventReporter& getInstance(){std::abort();}
 void cityGrowth(CvCity*,int){std::abort();}};
struct CvCity {
 GrowthSnapshot g; ProductionSnapshot p; char phase; int produced;
 bool m_bPopProductionProcess, human, automated, dirty;
 CvCity():g(),p(),phase('G'),produced(0),m_bPopProductionProcess(false),human(true),automated(false),dirty(false){}
 int getPopulation()const{return g.population;} int getFood()const{return g.food;}
 int getFoodKept()const{return g.foodKept;} int growthThreshold()const{return g.threshold;}
 int getMaxFoodKeptPercent()const{return g.keptPercent;}
 bool AI_isEmphasizeAvoidGrowth(){return g.avoidGrowth!=0;}
 bool isDisorder()const{return phase=='G'?g.disorder!=0:p.disorder!=0;}
 bool isFoodProduction()const{return phase=='G'?g.foodProduction!=0:p.foodProduction!=0;}
 int getYieldRate(YieldTypes type)const{assert(type==YIELD_FOOD);return phase=='G'?g.foodYield:p.foodYield;}
 int foodConsumption(bool noAngry=false)const{
  assert(noAngry==(phase=='P'));return phase=='G'?g.consumption:p.consumptionNoAngry;}
 int getOwnerINLINE(){return 0;}
 void setFood(int value){g.food=value;} void changeFood(int value){g.food+=value;}
 void setFoodKept(int value){g.foodKept=value;} void changeFoodKept(int value){g.foodKept+=value;}
 void changePopulation(int value){g.population+=value;throw PopulationBoundary();}
 int foodDifference(bool bBottom=true)const; void doGrowth();
 int getProductionDifference(int,int,int,bool,bool)const;
 int getCurrentProductionDifference(bool,bool)const;
 int getBaseYieldRate(YieldTypes type)const{assert(type==YIELD_PRODUCTION);return p.baseProduction;}
 int getBaseYieldRateModifier(YieldTypes type,int=0)const{assert(type==YIELD_PRODUCTION);return p.totalModifier;}
 int getOverflowProduction()const{return p.overflow;} int getFeatureProduction()const{return p.feature;}
 int getProduction()const{return p.progress;} int getProductionNeeded()const{return p.needed;}
 int getProductionModifier()const{return 0;}
 bool isHuman()const{return human;} bool isProductionAutomated()const{return automated;}
 bool isProduction()const{return p.hasOrder!=0;} bool isProductionProcess()const{return p.process!=0;}
 bool AI_isChooseProductionDirty(){return dirty;} void AI_chooseProduction(){std::abort();}
 void changeProduction(int value){produced=value;p.progress+=value;}
 void setOverflowProduction(int value){p.overflow=value;}
 void setFeatureProduction(int value){p.feature=value;}
 void changeOverflowProduction(int,int);
 void popOrder(int,bool finish,bool){assert(finish);throw CompletionBoundary();}
 void doProduction(bool);
};
'''
UNIT_HOST = r'''
struct UnitPlayer {int gold;void changeGold(int delta){gold+=delta;}} unitPlayer;
#define GET_PLAYER(owner) unitPlayer
struct UnitOracle {
 UnitCompletionSnapshot s;
 int getOwnerINLINE()const{return 0;}
 int getProductionNeeded(int)const{return s.needed;}
 int getUnitProduction(int)const{return s.progress;}
 int getCurrentProductionDifference(bool food,bool overflow)const{
  assert(!food && !overflow);return s.currentProductionNoOverflow;}
 int getProductionModifier(int)const{return 1;}
 int getBaseYieldRateModifier(YieldTypes type,int extra=0)const{
  assert(type==YIELD_PRODUCTION);return extra?s.totalModifier:s.baseModifier;}
 void setUnitProduction(int,int value){s.progress=value;}
 void setUnitProductionTime(int,int value){assert(value==0);}
 int getOverflowProduction()const{return s.overflow;}
 void setOverflowProduction(int value){s.overflow=value;}
 void changeOverflowProduction(int,int);
 void finish();
};
'''

MAIN = r'''
int main(){
 std::string line;
 while(std::getline(std::cin,line)){
  std::istringstream in(line);CvCity city;in>>city.phase;
  if(city.phase=='G'){
   GrowthSnapshot& s=city.g;
   in>>s.population>>s.food>>s.foodKept>>s.threshold>>s.keptPercent>>s.foodYield
     >>s.consumption>>s.foodProduction>>s.disorder>>s.avoidGrowth>>s.callback;
   assert(in && !s.callback);
   GrowthSnapshot copy=captureGrowth(city,YIELD_FOOD,false);
   assert(copy.population==s.population && copy.food==s.food && copy.foodKept==s.foodKept &&
    copy.threshold==s.threshold && copy.keptPercent==s.keptPercent && copy.foodYield==s.foodYield &&
    copy.consumption==s.consumption && copy.foodProduction==s.foodProduction && copy.disorder==s.disorder &&
    copy.avoidGrowth==s.avoidGrowth && copy.callback==s.callback);
   int before=s.population;int difference=city.foodDifference();
   const char* status="applied";
   try{city.doGrowth();}catch(const PopulationBoundary&){status="population_effects_required";}
   std::cout<<"{\"status\":\""<<status<<"\",\"population\":"<<s.population<<",\"food\":"<<s.food
    <<",\"food_kept\":"<<s.foodKept<<",\"difference\":"<<difference<<",\"grew\":"<<(s.population>before?1:0)<<"}\n";
  }else if(city.phase=='U'){
   UnitOracle unit;UnitCompletionSnapshot& s=unit.s;
   in>>s.progress>>s.needed>>s.currentProductionNoOverflow>>s.totalModifier
     >>s.baseModifier>>s.goldPercent>>s.overflow;
   assert(in);unitGoldPercent=s.goldPercent;unitPlayer.gold=0;
   unit.finish();
   std::cout<<"{\"status\":\"unit_creation_required\",\"progress\":"<<s.progress
    <<",\"overflow\":"<<s.overflow<<",\"gold\":"<<unitPlayer.gold<<"}\n";
  }else{
   assert(city.phase=='P');ProductionSnapshot& s=city.p;
   in>>s.progress>>s.needed>>s.baseProduction>>s.totalModifier>>s.foodYield>>s.consumptionNoAngry
     >>s.overflow>>s.feature>>s.foodProduction>>s.disorder>>s.callback>>s.choiceRequired
     >>s.process>>s.hasOrder>>s.allowNoProduction;
   assert(in && !s.callback && !s.choiceRequired && !s.process);
   ProductionSnapshot copy=captureProduction(city,YIELD_FOOD,YIELD_PRODUCTION,false,s.allowNoProduction!=0);
   assert(copy.baseProduction==s.baseProduction && copy.totalModifier==s.totalModifier &&
    copy.foodYield==s.foodYield && copy.consumptionNoAngry==s.consumptionNoAngry && copy.overflow==s.overflow &&
    copy.feature==s.feature && copy.foodProduction==s.foodProduction && copy.disorder==s.disorder &&
    copy.callback==s.callback && copy.choiceRequired==s.choiceRequired && copy.process==s.process &&
    copy.hasOrder==s.hasOrder && copy.allowNoProduction==s.allowNoProduction);
   if(s.hasOrder)assert(copy.progress==s.progress && copy.needed==s.needed);
   int difference=0;
   if(!s.disorder && (s.hasOrder || s.allowNoProduction))
    difference=city.getCurrentProductionDifference(false,s.hasOrder!=0);
   const char* status="applied";
   try{city.doProduction(s.allowNoProduction!=0);}catch(const CompletionBoundary&){status="completion_effects_required";}
   std::cout<<"{\"status\":\""<<status<<"\",\"progress\":"<<s.progress<<",\"overflow\":"<<s.overflow
    <<",\"feature\":"<<s.feature<<",\"difference\":"<<difference<<"}\n";
  }
 }
}
'''

def compile_oracle(source, folder):
    methods = verify_contract(source)
    cpp = folder/'native.cpp'; exe = folder/'native'
    fragment = methods.pop(UNIT_FRAGMENT)
    overflow = methods['void CvCity::changeOverflowProduction('].replace('CvCity::','UnitOracle::',1)
    unit_body = 'void UnitOracle::finish(){int iProductionNeeded;int iOverflow;int eTrainUnit=0;\n'+fragment+'\n}'
    cpp.write_text(HOST+'\n'+'\n'.join(methods.values())+'\n'+UNIT_HOST+'\n'+overflow+'\n'+unit_body+'\n'+MAIN)
    subprocess.run(['g++','-std=c++03','-Wall','-Wextra','-Werror','-Wno-unused-parameter',
                    '-O1','-fsanitize=undefined','-fno-sanitize-recover=undefined',
                    '-I',str(HERE),str(cpp),'-o',str(exe)],check=True)
    return exe
