"""Batched good-count updates (M43) on GitLab claude/settlement-economy at f70541a9.
A change of goods is a vector aiChange (aiChange[e] = change of the count of good e). A plot hands its whole change to
its plot group at once; the plot group walks its plots once; a city applies all counts, processes each gain or loss of
a good, and updates its corporations once. Same end state as one good at a time: processBonus(e, +1/-1) is additive
(a gain then a loss cancel) and updateCorporation recomputes everything it sets from the current counts.
usage: batch_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
D = 'Assets/CvGameCoreDLL/'
E = []
def e(f, old, new): E.append((f, old, new))

# ---- CvCity ----
e(D + 'CvCity.h', """	void changeNumBonuses(BonusTypes eIndex, int iChange);
""", """	void changeNumBonuses(BonusTypes eIndex, int iChange);
	void changeNumBonuses(const std::vector<int>& aiChange);	// aiChange[e]: change of the count of good e
	bool changeNumBonusesNoCorporation(BonusTypes eIndex, int iChange);	// true if a corporation of the city consumes eIndex
""")
e(D + 'CvCity.cpp', """void CvCity::changeNumBonuses(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		bool bOldHasBonus = hasBonus(eIndex);

		m_paiNumBonuses[eIndex] += iChange;

		if (bOldHasBonus != hasBonus(eIndex))
		{
			if (hasBonus(eIndex))
			{
				processBonus(eIndex, 1);
			}
			else
			{
				processBonus(eIndex, -1);
			}
		}

		if (isCorporationBonus(eIndex))
		{
			updateCorporation();
		}
	}
}
""", """void CvCity::changeNumBonuses(BonusTypes eIndex, int iChange)
{
	if (changeNumBonusesNoCorporation(eIndex, iChange))
	{
		updateCorporation();
	}
}

// Adds iChange to the count of eIndex and processes the gain or loss of the good; leaves the corporations to the caller.
// Returns whether a corporation of the city consumes eIndex, so that its output depends on the count.
bool CvCity::changeNumBonusesNoCorporation(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange == 0)
	{
		return false;
	}

	bool bOldHasBonus = hasBonus(eIndex);

	m_paiNumBonuses[eIndex] += iChange;

	if (bOldHasBonus != hasBonus(eIndex))
	{
		processBonus(eIndex, hasBonus(eIndex) ? 1 : -1);
	}

	return isCorporationBonus(eIndex);
}

// All counts first, then one corporation update. The end state equals applying the goods one at a time:
// processBonus is additive (a gain followed by a loss cancels), so only each good's net gain or loss counts, and
// updateCorporation recomputes everything it sets from the counts, so one call after the last count equals one per count.
void CvCity::changeNumBonuses(const std::vector<int>& aiChange)
{
	bool bCorporation = false;

	for (int iI = 0; iI < (int)aiChange.size(); ++iI)
	{
		if (changeNumBonusesNoCorporation((BonusTypes)iI, aiChange[iI]))
		{
			bCorporation = true;
		}
	}

	if (bCorporation)
	{
		updateCorporation();
	}
}
""")

# ---- CvPlotGroup ----
e(D + 'CvPlotGroup.h', """	void changeNumBonuses(BonusTypes eBonus, int iChange);
""", """	void changeNumBonuses(BonusTypes eBonus, int iChange);
	void changeNumBonuses(const std::vector<int>& aiChange);	// aiChange[e]: change of the count of good e; one walk of the plots
""")
e(D + 'CvPlotGroup.cpp', """void CvPlotGroup::insertAtEndPlots(XYCoords xy)
""", """// Every good at once: the counts change, then the plots are walked once and each city of the owner applies the whole
// vector (CvCity::changeNumBonuses), instead of one walk and one corporation update per good.
void CvPlotGroup::changeNumBonuses(const std::vector<int>& aiChange)
{
	bool bChange = false;

	for (int iI = 0; iI < (int)aiChange.size(); ++iI)
	{
		if (aiChange[iI] != 0)
		{
			m_paiNumBonuses[iI] += aiChange[iI];
			bChange = true;
		}
	}

	if (!bChange)
	{
		return;
	}

	for (CLLNode<XYCoords>* pPlotNode = headPlotsNode(); pPlotNode != NULL; pPlotNode = nextPlotsNode(pPlotNode))
	{
		CvCity* pCity = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY)->getPlotCity();

		if (pCity != NULL && pCity->getOwnerINLINE() == getOwnerINLINE())
		{
			pCity->changeNumBonuses(aiChange);
		}
	}
}


void CvPlotGroup::insertAtEndPlots(XYCoords xy)
""")

# ---- CvPlot::updatePlotGroupBonus: one change vector per plot ----
NEW_UPDATE = """void CvPlot::updatePlotGroupBonus(bool bAdd)
{
	PROFILE_FUNC();

	if (!isOwned())
	{
		return;
	}

	CvPlotGroup* pPlotGroup = getPlotGroup(getOwnerINLINE());

	if (pPlotGroup == NULL)
	{
		return;
	}

	CvCity* pPlotCity = getPlotCity();
	BonusTypes eNonObsoleteBonus = getNonObsoleteBonusType(getTeam());
	ImprovementTypes eImprovement = getImprovementType();

	// Most plots give nothing: no city, no resource and no improvement that produces goods
	if (pPlotCity == NULL && eNonObsoleteBonus == NO_BONUS &&
		(eImprovement == NO_IMPROVEMENT || GC.getImprovementInfo(eImprovement).getNumProducedBonuses() == 0))
	{
		return;
	}

	// What the plot gives, as one change vector: aiChange[e] = iSign x (instances of good e this plot gives)
	const int iSign = bAdd ? 1 : -1;
	CvTeam& kTeam = GET_TEAM(getTeam());
	std::vector<int> aiChange(GC.getNumBonusInfos(), 0);

	if (pPlotCity != NULL)
	{
		for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
		{
			if (!kTeam.isBonusObsolete((BonusTypes)iI))
			{
				aiChange[iI] += iSign * pPlotCity->getFreeBonus((BonusTypes)iI);
			}
		}

		if (pPlotCity->isCapital())
		{
			CvPlayer& kOwner = GET_PLAYER(getOwnerINLINE());
			for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
			{
				aiChange[iI] += iSign * (kOwner.getBonusImport((BonusTypes)iI) - kOwner.getBonusExport((BonusTypes)iI));
			}
		}
	}

	if (eNonObsoleteBonus != NO_BONUS)
	{
		if (kTeam.isHasTech((TechTypes)(GC.getBonusInfo(eNonObsoleteBonus).getTechCityTrade())))
		{
			if (isCity(true, getTeam()) ||
				((eImprovement != NO_IMPROVEMENT) && GC.getImprovementInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus)))
			{
				if (isBonusNetwork(getTeam()))
				{
					aiChange[eNonObsoleteBonus] += iSign;
				}
			}
		}
	}

	// Settlement economy: goods the improvement produces (lumber camp: timber; pasture on sheep: wool ...)
	if ((eImprovement != NO_IMPROVEMENT) && (GC.getImprovementInfo(eImprovement).getNumProducedBonuses() > 0) && isBonusNetwork(getTeam()))
	{
		CvImprovementInfo& kImprovement = GC.getImprovementInfo(eImprovement);

		for (int iI = 0; iI < kImprovement.getNumProducedBonuses(); ++iI)
		{
			BonusTypes eProduced = kImprovement.getProducedBonus(iI);
			BonusTypes ePrereq = kImprovement.getProducedBonusPrereq(iI);
			TechTypes eTrade = (TechTypes)GC.getBonusInfo(eProduced).getTechCityTrade();

			if ((ePrereq == NO_BONUS || ePrereq == eNonObsoleteBonus) &&
				!kTeam.isBonusObsolete(eProduced) &&
				(eTrade == NO_TECH || kTeam.isHasTech(eTrade)))
			{
				aiChange[eProduced] += iSign;
			}
		}
	}

	pPlotGroup->changeNumBonuses(aiChange);
}
"""

# ---- the city's own count when it joins or leaves a plot group: one batch instead of one call per good ----
for sign, getter in (('-', 'pPlotGroup->getNumBonuses((BonusTypes)iI)'),):
    pass
e(D + 'CvPlot.cpp', """				for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				{
					getPlotCity()->changeNumBonuses(((BonusTypes)iI), -(pPlotGroup->getNumBonuses((BonusTypes)iI)));
				}
""", """				std::vector<int> aiChange(GC.getNumBonusInfos());
				for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				{
					aiChange[iI] = -(pPlotGroup->getNumBonuses((BonusTypes)iI));
				}
				getPlotCity()->changeNumBonuses(aiChange);
""")
e(D + 'CvPlot.cpp', """				for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				{
					getPlotCity()->changeNumBonuses(((BonusTypes)iI), pPlotGroup->getNumBonuses((BonusTypes)iI));
				}
""", """				std::vector<int> aiChange(GC.getNumBonusInfos());
				for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				{
					aiChange[iI] = pPlotGroup->getNumBonuses((BonusTypes)iI);
				}
				getPlotCity()->changeNumBonuses(aiChange);
""")
e(D + 'CvPlot.cpp', """					for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
					{
						pCity->changeNumBonuses(((BonusTypes)iI), -(pOldPlotGroup->getNumBonuses((BonusTypes)iI)));
					}
""", """					std::vector<int> aiChange(GC.getNumBonusInfos());
					for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
					{
						aiChange[iI] = -(pOldPlotGroup->getNumBonuses((BonusTypes)iI));
					}
					pCity->changeNumBonuses(aiChange);
""")
e(D + 'CvPlot.cpp', """					for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
					{
						pCity->changeNumBonuses(((BonusTypes)iI), getPlotGroup(ePlayer)->getNumBonuses((BonusTypes)iI));
					}
""", """					std::vector<int> aiChange(GC.getNumBonusInfos());
					for (iI = 0; iI < GC.getNumBonusInfos(); ++iI)
					{
						aiChange[iI] = getPlotGroup(ePlayer)->getNumBonuses((BonusTypes)iI);
					}
					pCity->changeNumBonuses(aiChange);
""")

pairs = []
for f, old, new in E:
    p = os.path.join(mod, f)
    s = open(p, 'rb').read().decode('latin-1')
    nl = '\r\n' if '\r\n' in s else '\n'
    o, n = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(o) == 1, (f, s.count(o), old[:80])
    s = s.replace(o, n); open(p, 'wb').write(s.encode('latin-1'))
    pairs.append({'file': f, 'old': o, 'new': n})
# updatePlotGroupBonus: the whole function, from its signature to the next function
f = D + 'CvPlot.cpp'; p = os.path.join(mod, f)
s = open(p, 'rb').read().decode('latin-1'); nl = '\r\n' if '\r\n' in s else '\n'
a = s.index('void CvPlot::updatePlotGroupBonus(bool bAdd)'); b = s.index('bool CvPlot::isBonusTech(TechTypes eTech) const')
b = s.rindex('}' + nl, a, b) + len('}' + nl)
o = s[a:b]; n = NEW_UPDATE.replace('\n', nl)
assert s.count(o) == 1
s = s.replace(o, n); open(p, 'wb').write(s.encode('latin-1'))
pairs.append({'file': f, 'old': o, 'new': n})
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(x)) for x in pairs), 'bytes of JSON')
