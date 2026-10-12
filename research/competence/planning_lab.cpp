// Research model only: no BTS engine calls. Original C++03 implementation.
#include <algorithm>
#include <cassert>
#include <climits>
#include <iostream>
#include <map>
#include <vector>

namespace PlanningLab {
enum { MAX_JOBS = 8 };
struct Job {
    int prerequisites, resources, effort, productionWork, productionGain, incomeGain, reward, anarchy;
};
struct Model {
    int n, horizon, production, income, required, deadline;
    Job jobs[MAX_JOBS];
};
struct State {
    int started, done, remaining[MAX_JOBS], start[MAX_JOBS], finish[MAX_JOBS];
    long long utility;
    State():started(0),done(0),utility(0) {
        for(int i=0;i<MAX_JOBS;++i){remaining[i]=0;start[i]=finish[i]=-1;}
    }
};
struct Key {
    int started,done,remaining[MAX_JOBS];
    explicit Key(const State& s):started(s.started),done(s.done) {
        for(int i=0;i<MAX_JOBS;++i)remaining[i]=s.remaining[i];
    }
    bool operator<(const Key& k)const {
        if(started!=k.started)return started<k.started;
        if(done!=k.done)return done<k.done;
        for(int i=0;i<MAX_JOBS;++i)if(remaining[i]!=k.remaining[i])return remaining[i]<k.remaining[i];
        return false;
    }
};
int countBits(int bits){int n=0;while(bits){n+=bits&1;bits>>=1;}return n;}
int income(const Model& m,const State& s){int r=m.income;for(int i=0;i<m.n;++i)if(s.done&(1<<i))r+=m.jobs[i].incomeGain;return r;}
int production(const Model& m,const State& s){int r=m.production;for(int i=0;i<m.n;++i)if(s.done&(1<<i))r+=m.jobs[i].productionGain;return r;}
bool satisfied(const Model& m,const State& s){return (s.done&m.required)==m.required;}
bool better(const State& a,const State& b){
    if(a.utility!=b.utility)return a.utility>b.utility;
    if(countBits(a.started)!=countBits(b.started))return countBits(a.started)<countBits(b.started);
    return Key(a)<Key(b);
}
bool advance(const Model& m,const State& before,int starts,int time,State& after){
    int occupied=0;
    for(int i=0;i<m.n;++i)if(before.remaining[i]>0)occupied|=m.jobs[i].resources;
    if(starts&before.started)return false;
    after=before;
    for(int i=0;i<m.n;++i)if(starts&(1<<i)){
        const Job& j=m.jobs[i];
        if((before.done&j.prerequisites)!=j.prerequisites || (occupied&j.resources))return false;
        occupied|=j.resources;after.started|=1<<i;after.remaining[i]=j.effort;after.start[i]=time;
    }
    bool anarchy=false;
    for(int i=0;i<m.n;++i)if(after.remaining[i]>0 && m.jobs[i].anarchy)anarchy=true;
    if(!anarchy)after.utility+=income(m,before);
    const int rate=production(m,before);
    for(int i=0;i<m.n;++i)if(after.remaining[i]>0){
        after.remaining[i]=std::max(0,after.remaining[i]-(m.jobs[i].productionWork?rate:1));
        if(after.remaining[i]==0){after.done|=1<<i;after.finish[i]=time+1;after.utility+=m.jobs[i].reward;}
    }
    return !(m.deadline>0 && time+1>=m.deadline && !satisfied(m,after));
}
struct Result {
    bool feasible,exact;State best;unsigned long long transitions;size_t peak;
    Result():feasible(false),exact(true),transitions(0),peak(0){}
};
// A complete guard/goal-first schedule is a feasible fallback, not a bound.
Result greedy(const Model& m){
    Result r;r.exact=false;State s;
    for(int t=0;t<m.horizon;++t){
        int mask=0;State next;
        for(int pass=0;pass<2;++pass)for(int i=0;i<m.n;++i){
            if(((m.required&(1<<i))!=0)!=(pass==0))continue;
            if(s.started&(1<<i))continue;
            // Check starts without using the deadline to hide a legal action.
            Model noDeadline=m;noDeadline.deadline=0;
            if(advance(noDeadline,s,mask|(1<<i),t,next))mask|=1<<i;
        }
        if(!advance(m,s,mask,t,next))return r;
        s=next;
    }
    r.feasible=satisfied(m,s);r.best=s;return r;
}
struct Rank {
    const Model* m;int time;
    Rank(const Model& model,int t):m(&model),time(t){}
    bool operator()(const State& a,const State& b)const{
        const long long va=a.utility+(long long)(m->horizon-time)*income(*m,a);
        const long long vb=b.utility+(long long)(m->horizon-time)*income(*m,b);
        if(va!=vb)return va>vb;
        int pa=0,pb=0;
        for(int i=0;i<m->n;++i){
            if(a.started&(1<<i))pa+=m->jobs[i].effort-a.remaining[i];
            if(b.started&(1<<i))pb+=m->jobs[i].effort-b.remaining[i];
        }
        if(pa!=pb)return pa>pb;
        return Key(a)<Key(b);
    }
};
Result search(const Model& m,int width){
    Result result=greedy(m);result.exact=true;
    std::vector<State> layer(1);
    for(int t=0;t<m.horizon && !layer.empty();++t){
        std::map<Key,State> next;
        for(size_t k=0;k<layer.size();++k)for(int starts=0;starts<(1<<m.n);++starts){
            ++result.transitions;State child;
            if(!advance(m,layer[k],starts,t,child))continue;
            Key key(child);std::map<Key,State>::iterator old=next.find(key);
            if(old==next.end() || child.utility>old->second.utility)next[key]=child;
        }
        result.peak=std::max(result.peak,next.size());layer.clear();
        for(std::map<Key,State>::const_iterator it=next.begin();it!=next.end();++it)layer.push_back(it->second);
        if(width>0 && layer.size()>size_t(width)){
            std::sort(layer.begin(),layer.end(),Rank(m,t+1));layer.resize(width);result.exact=false;
        }
    }
    for(size_t i=0;i<layer.size();++i)if(satisfied(m,layer[i]) && (!result.feasible || better(layer[i],result.best))){
        result.feasible=true;result.best=layer[i];
    }
    return result;
}
void print(const Result& r,const Model& m){
    std::cout<<"{\"feasible\":"<<(r.feasible?"true":"false")<<",\"exact\":"<<(r.exact?"true":"false")
             <<",\"utility\":"<<r.best.utility<<",\"transitions\":"<<r.transitions<<",\"peak\":"<<r.peak<<",\"start\":[";
    for(int i=0;i<m.n;++i){if(i)std::cout<<",";std::cout<<r.best.start[i];}
    std::cout<<"],\"finish\":[";for(int i=0;i<m.n;++i){if(i)std::cout<<",";std::cout<<r.best.finish[i];}
    std::cout<<"]}";
}
}
int main(){
    using namespace PlanningLab;Model m;int width;
    while(std::cin>>m.n>>m.horizon>>m.production>>m.income>>m.required>>m.deadline>>width){
        assert(m.n>0 && m.n<=MAX_JOBS && m.horizon>0 && m.horizon<=64 && m.production>0 && m.production<=1000);
        assert(m.income>=0 && m.income<=1000 && m.required>=0 && m.required<(1<<m.n));
        assert(m.deadline>=0 && m.deadline<=m.horizon && width>=0);
        for(int i=0;i<m.n;++i){Job& j=m.jobs[i];
            std::cin>>j.prerequisites>>j.resources>>j.effort>>j.productionWork>>j.productionGain>>j.incomeGain>>j.reward>>j.anarchy;
            assert(j.prerequisites>=0 && j.prerequisites<(1<<m.n) && j.resources>0 && j.resources<16);
            assert(j.effort>0 && j.effort<=1000 && j.productionGain>=0 && j.productionGain<=1000);
            assert(j.incomeGain>=0 && j.incomeGain<=1000 && j.reward>=-1000000 && j.reward<=1000000);
            assert((j.productionWork==0 || j.productionWork==1) && (j.anarchy==0 || j.anarchy==1));
        }
        Result result=search(m,width),baseline=greedy(m);
        std::cout<<"{\"search\":";print(result,m);std::cout<<",\"greedy\":";print(baseline,m);std::cout<<"}\n";
    }
}
