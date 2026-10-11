// Isolated algorithm experiments, not game code or a production AI replacement.
// C++03 style; the 64-bit extension matches the legacy DLL's arithmetic needs.
#include <algorithm>
#include <cassert>
#include <climits>
#include <ctime>
#include <iostream>
#include <vector>
#if defined(_MSC_VER)
typedef __int64 Wide;
#else
typedef long long Wide;
#endif
const Wide INF = (Wide)1000000000 * 1000000;

struct Tech {
    unsigned int andMask, orMask;
    int cost;
    Tech(int c=0, unsigned int a=0, unsigned int o=0):andMask(a),orMask(o),cost(c){}
};
struct ResearchResult {
    Wide cost, scanned, expanded, checks;
    unsigned int mask;
    std::vector<int> order;
    ResearchResult():cost(INF),scanned(0),expanded(0),checks(0),mask(0){}
};
bool available(const Tech& t, unsigned int mask) {
    return (mask & t.andMask)==t.andMask && (t.orMask==0 || (mask & t.orMask)!=0);
}
ResearchResult researchDP(const std::vector<Tech>& tech, int goal) {
    const int n=(int)tech.size(); assert(n>0 && n<=20 && goal>=0 && goal<n);
    const unsigned int count=1u<<n, goalBit=1u<<goal;
    for(int i=0;i<n;++i)assert(tech[i].cost>=0 && (tech[i].andMask|tech[i].orMask)<count);
    std::vector<Wide> cost(count,INF);
    std::vector<int> last(count,-1);
    cost[0]=0;
    ResearchResult result;
    for(unsigned int mask=0;mask<count;++mask) {
        ++result.scanned;
        if(cost[mask]==INF)continue;
        if(mask & goalBit) {
            if(cost[mask]<result.cost){result.cost=cost[mask];result.mask=mask;}
            continue; // Costs are nonnegative; a completed goal needs no extra research.
        }
        ++result.expanded;
        for(int i=0;i<n;++i) {
            ++result.checks;
            const unsigned int bit=1u<<i;
            if((mask & bit) || !available(tech[i],mask))continue;
            const unsigned int next=mask|bit;
            const Wide value=cost[mask]+tech[i].cost;
            if(value<cost[next]){cost[next]=value;last[next]=i;}
        }
    }
    if(result.cost!=INF) {
        unsigned int cursor=result.mask;
        while(cursor) {
            const int i=last[cursor];assert(i>=0);
            result.order.push_back(i);cursor^=1u<<i;
        }
        std::reverse(result.order.begin(),result.order.end());
    }
    return result;
}
// Independent oracle: enumerate complete subsets and compute a reachability
// fixed point within each subset, without the DP's transition recurrence.
Wide researchOracle(const std::vector<Tech>& tech,int goal) {
    const int n=(int)tech.size();assert(n<=9);
    Wide best=INF;
    for(unsigned int subset=0;subset<(1u<<n);++subset) {
        if(!(subset & (1u<<goal)))continue;
        unsigned int reached=0,previous;
        do {
            previous=reached;
            for(int i=0;i<n;++i)
                if((subset&(1u<<i)) && available(tech[i],reached))reached|=1u<<i;
        }while(reached!=previous);
        if(reached!=subset)continue;
        Wide value=0;
        for(int i=0;i<n;++i)if(subset&(1u<<i))value+=tech[i].cost;
        best=std::min(best,value);
    }
    return best;
}
Wide scalarTreeCost(const std::vector<Tech>& t,int i) {
    Wide value=t[i].cost,orCost=INF;
    for(int j=0;j<(int)t.size();++j) {
        if(t[i].andMask&(1u<<j))value+=scalarTreeCost(t,j);
        if(t[i].orMask&(1u<<j))orCost=std::min(orCost,scalarTreeCost(t,j));
    }
    return value+(t[i].orMask?orCost:0);
}
void checkResearchPlan(const std::vector<Tech>& tech,int goal,const ResearchResult& r) {
    if(r.cost==INF){assert(r.order.empty());return;}
    unsigned int mask=0;Wide cost=0;
    for(unsigned int j=0;j<r.order.size();++j) {
        const int i=r.order[j];assert(!(mask&(1u<<i)) && available(tech[i],mask));
        mask|=1u<<i;cost+=tech[i].cost;
    }
    assert((mask&(1u<<goal)) && mask==r.mask && cost==r.cost);
}

typedef std::vector<std::vector<int> > Matrix;
struct AssignmentResult {
    Wide cost,edgeChecks;
    std::vector<int> column;
    AssignmentResult():cost(0),edgeChecks(0){}
};
// Dense square minimum-cost assignment, primal-dual shortest augmenting paths.
// O(n^3) time, O(n) auxiliary storage beyond the O(n^2) cost matrix.
AssignmentResult assignment(const Matrix& c) {
    const int n=(int)c.size();
    for(int i=0;i<n;++i)assert((int)c[i].size()==n);
    std::vector<Wide> u(n+1,0),v(n+1,0);
    std::vector<int> owner(n+1,0),previous(n+1,0);
    AssignmentResult result;result.column.assign(n,-1);
    for(int row=1;row<=n;++row) {
        owner[0]=row;int col=0;
        std::vector<Wide> distance(n+1,INF);
        std::vector<char> used(n+1,0);
        do {
            used[col]=1;
            const int active=owner[col];int next=0;Wide delta=INF;
            for(int j=1;j<=n;++j)if(!used[j]) {
                ++result.edgeChecks;
                const Wide reduced=(Wide)c[active-1][j-1]-u[active]-v[j];
                if(reduced<distance[j]){distance[j]=reduced;previous[j]=col;}
                if(distance[j]<delta){delta=distance[j];next=j;}
            }
            assert(next!=0);
            for(int j=0;j<=n;++j) {
                if(used[j]){u[owner[j]]+=delta;v[j]-=delta;}
                else distance[j]-=delta;
            }
            col=next;
        }while(owner[col]!=0);
        do {
            const int old=previous[col];owner[col]=owner[old];col=old;
        }while(col!=0);
    }
    for(int col=1;col<=n;++col)result.column[owner[col]-1]=col-1;
    for(int row=0;row<n;++row)result.cost+=c[row][result.column[row]];
    return result;
}
Wide assignmentOracle(const Matrix& c) {
    const int n=(int)c.size();std::vector<int> p(n);
    for(int i=0;i<n;++i)p[i]=i;
    Wide best=INF;
    do {
        Wide cost=0;for(int i=0;i<n;++i)cost+=c[i][p[i]];
        best=std::min(best,cost);
    }while(std::next_permutation(p.begin(),p.end()));
    return best;
}
unsigned int randomState=314159;
unsigned int nextRandom(){randomState=1664525u*randomState+1013904223u;return randomState;}
void verify() {
    // Real base XML costs/dependencies, with other prerequisites already owned.
    std::vector<Tech> diamond;
    diamond.push_back(Tech(50));diamond.push_back(Tech(48,1));diamond.push_back(Tech(120,1,2));
    ResearchResult r=researchDP(diamond,2);checkResearchPlan(diamond,2,r);
    assert(r.cost==218 && r.order.size()==3 && scalarTreeCost(diamond,2)==268);
    // Shared OR option wins globally even though each branch prefers a private option.
    std::vector<Tech> shared;
    shared.push_back(Tech(6));shared.push_back(Tech(4));shared.push_back(Tech(4));
    shared.push_back(Tech(1,0,3));shared.push_back(Tech(1,0,5));shared.push_back(Tech(1,24));
    r=researchDP(shared,5);checkResearchPlan(shared,5,r);
    assert(r.cost==9 && scalarTreeCost(shared,5)==11);
    assert((r.mask&1)!=0 && (r.mask&6)==0);
    std::vector<Tech> cycle(2);cycle[0]=Tech(1,2);cycle[1]=Tech(1,1);
    assert(researchDP(cycle,1).cost==INF);
    std::vector<Tech> zero(2);zero[1]=Tech(0,1);assert(researchDP(zero,1).cost==0);
    for(int trial=0;trial<300;++trial) {
        const int n=1+trial%8;std::vector<Tech> tech(n);
        for(int i=0;i<n;++i) {
            const unsigned int earlier=(1u<<i)-1;
            const int price=(int)(nextRandom()%25);
            const unsigned int andMask=nextRandom()&earlier;
            const unsigned int orMask=nextRandom()&earlier;
            tech[i]=Tech(price,andMask,orMask);
        }
        r=researchDP(tech,n-1);checkResearchPlan(tech,n-1,r);
        assert(r.cost==researchOracle(tech,n-1));
    }
    Matrix greedyTrap(2,std::vector<int>(2));
    greedyTrap[0][0]=-10;greedyTrap[0][1]=-9;greedyTrap[1][0]=-9;greedyTrap[1][1]=0;
    assert(assignment(greedyTrap).cost==-18); // Row-greedy gives -10.
    Matrix extreme(3,std::vector<int>(3,INT_MAX));
    extreme[0][0]=INT_MIN;assert(assignment(extreme).cost==(Wide)INT_MIN+2*(Wide)INT_MAX);
    for(int trial=0;trial<160;++trial) {
        const int n=1+trial%8;Matrix c(n,std::vector<int>(n));
        for(int i=0;i<n;++i)for(int j=0;j<n;++j)c[i][j]=(int)(nextRandom()%101)-50;
        AssignmentResult a=assignment(c);assert(a.cost==assignmentOracle(c));
        assert(a.column==assignment(c).column);
    }
    Matrix ties(12,std::vector<int>(12,0));
    assert(assignment(ties).cost==0 && assignment(ties).column==assignment(ties).column);
    std::cout<<"{\"kind\":\"verification\",\"research_random_oracle_cases\":300,"
             <<"\"assignment_random_oracle_cases\":160,\"chariot_scalar\":268,\"chariot_exact\":218,"
             <<"\"shared_or_local\":11,\"shared_or_exact\":9,\"greedy_assignment_utility\":10,"
             <<"\"exact_assignment_utility\":18,\"passed\":true}\n";
}
void benchmarks() {
    // Deliberate dense-array stress: production must use the linear pure-AND
    // closure shortcut here. This measures oracle overhead, not gameplay speed.
    const int sizes[]={8,12,16,20};
    for(int s=0;s<4;++s) {
        const int n=sizes[s];std::vector<Tech> tech(n,Tech(10));
        tech[n-1].andMask=(1u<<(n-1))-1;
        const std::clock_t start=std::clock();ResearchResult r=researchDP(tech,n-1);
        const double ms=1000.0*(std::clock()-start)/CLOCKS_PER_SEC;
        assert(r.cost==10*n);
        std::cout<<"{\"kind\":\"research_stress\",\"k\":"<<n<<",\"scanned\":"<<r.scanned
                 <<",\"expanded\":"<<r.expanded<<",\"candidate_checks\":"<<r.checks
                 <<",\"table_bytes\":"<<(1u<<n)*(sizeof(Wide)+sizeof(int))<<",\"cpu_ms\":"<<ms<<"}\n";
    }
    const int counts[]={16,32,64,128};
    for(int s=0;s<4;++s) {
        const int n=counts[s];Matrix cost(n,std::vector<int>(n));
        for(int i=0;i<n;++i)for(int j=0;j<n;++j)cost[i][j]=(int)(nextRandom()%20001)-10000;
        const std::clock_t start=std::clock();AssignmentResult a=assignment(cost);
        const double ms=1000.0*(std::clock()-start)/CLOCKS_PER_SEC;
        std::cout<<"{\"kind\":\"assignment_stress\",\"n\":"<<n<<",\"edge_checks\":"<<a.edgeChecks
                 <<",\"matrix_bytes\":"<<n*n*sizeof(int)<<",\"cost\":"<<a.cost<<",\"cpu_ms\":"<<ms<<"}\n";
    }
}
int main(int argc,char**) {
    assert(sizeof(unsigned int)==4 && sizeof(int)==4 && sizeof(Wide)==8);
    verify();if(argc>1)benchmarks();return 0;
}
