"""Fixes after P30 (M41, M42) on GitLab claude/settlement-economy at 8bb55694:
- CvCityAI::AI_bestPlotBuild: the produced-goods term follows the resource code: building an improvement that gives
  a good the city lacks (and can trade) is worth the good; replacing the improvement that gives the city its only
  instance costs it; the improvement already on the plot gets nothing (before: every improvement giving a good the
  plot already gave was boosted, which pushed values past the iValue > 0 gate and inflated best builds every turn).
- CvPlot::updatePlotGroupBonus: test the produced list before isBonusNetwork.
- XML: lumbermill production 4 -> 5 (M41); IMPROVEMENT_CAMP gives Leather on Sheep, Cow and Horse (M41, D20).
- Pedia: Leather also from hunting camps.
usage: lq_fix1_edits.py <mod checkout> <pairs.json out>"""
import json, os, re, sys

mod, out = sys.argv[1], sys.argv[2]
D = 'Assets/CvGameCoreDLL/'
E = []
def e(f, old, new): E.append((f, old, new))

e(D + 'CvCityAI.cpp',
"""				// Settlement economy: a good the improvement produces counts like a connected resource when the city
				// lacks it, or when the plot's improvement already gives it (so a camp is kept, or upgraded to a mill)
				{
					CvImprovementInfo& kFinal = GC.getImprovementInfo(eFinalImprovement);
					for (iJ = 0; iJ < kFinal.getNumProducedBonuses(); iJ++)
					{
						BonusTypes eProduced = kFinal.getProducedBonus(iJ);
						if (kFinal.isProducedBonus(eProduced, eNonObsoleteBonus) &&
							(!hasBonus(eProduced) || (eCurImprovement != NO_IMPROVEMENT && GC.getImprovementInfo(eCurImprovement).isProducedBonus(eProduced, eNonObsoleteBonus))))
						{
							iValue += (GET_PLAYER(getOwnerINLINE()).AI_bonusVal(eProduced) * 10);
						}
					}
				}
""",
"""				// Settlement economy: goods improvements produce, valued as the resource code below values a resource:
				// building one that gives a good the city lacks and can trade is worth the good; replacing the one that
				// gives the city its only instance of a good costs it; keeping the improvement on the plot is neither
				if (eImprovement != eCurImprovement)
				{
					CvImprovementInfo& kFinal = GC.getImprovementInfo(eFinalImprovement);
					for (iJ = 0; iJ < kFinal.getNumProducedBonuses(); iJ++)
					{
						BonusTypes eProduced = kFinal.getProducedBonus(iJ);
						TechTypes eTrade = (TechTypes)GC.getBonusInfo(eProduced).getTechCityTrade();
						if (kFinal.isProducedBonus(eProduced, eNonObsoleteBonus) && !hasBonus(eProduced) &&
							(eCurImprovement == NO_IMPROVEMENT || !GC.getImprovementInfo(eCurImprovement).isProducedBonus(eProduced, eNonObsoleteBonus)) &&
							(eTrade == NO_TECH || GET_TEAM(getTeam()).isHasTech(eTrade)))
						{
							iValue += (GET_PLAYER(getOwnerINLINE()).AI_bonusVal(eProduced) * 10);
						}
					}
					if (eCurImprovement != NO_IMPROVEMENT)
					{
						CvImprovementInfo& kCurrent = GC.getImprovementInfo(eCurImprovement);
						for (iJ = 0; iJ < kCurrent.getNumProducedBonuses(); iJ++)
						{
							BonusTypes eProduced = kCurrent.getProducedBonus(iJ);
							if (kCurrent.isProducedBonus(eProduced, eNonObsoleteBonus) && !kFinal.isProducedBonus(eProduced, eNonObsoleteBonus) &&
								getNumBonuses(eProduced) == 1)
							{
								iValue -= 1000;
								break;
							}
						}
					}
				}
""")
e(D + 'CvPlot.cpp',
"""		if ((getImprovementType() != NO_IMPROVEMENT) && isBonusNetwork(getTeam()))
		{
			CvImprovementInfo& kImprovement = GC.getImprovementInfo(getImprovementType());
""",
"""		if ((getImprovementType() != NO_IMPROVEMENT) && (GC.getImprovementInfo(getImprovementType()).getNumProducedBonuses() > 0) && isBonusNetwork(getTeam()))
		{
			CvImprovementInfo& kImprovement = GC.getImprovementInfo(getImprovementType());
""")
X = 'Assets/XML/'
e(X + 'Terrain/CIV4ImprovementInfos.xml',
"""			<ArtDefineTag>ART_DEF_IMPROVEMENT_LUMBERMILL</ArtDefineTag>
			<YieldChanges>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>4</iYieldChange>
""",
"""			<ArtDefineTag>ART_DEF_IMPROVEMENT_LUMBERMILL</ArtDefineTag>
			<YieldChanges>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>5</iYieldChange>
""")
CAMP = ''.join("""				<ProducedBonus>
					<BonusType>BONUS_LEATHER</BonusType>
					<PrereqBonus>%s</PrereqBonus>
				</ProducedBonus>
""" % a for a in ('BONUS_SHEEP', 'BONUS_COW', 'BONUS_HORSE'))
E.append(('CAMP', X + 'Terrain/CIV4ImprovementInfos.xml', None, """			<ProducedBonuses>
""" + CAMP + """			</ProducedBonuses>
"""))
T = 'Assets/XML/Text/RoM_GameText_SettlementEconomy.xml'
for o, n in [('From pastures and latifundia on sheep, cows and horses.', 'From pastures and latifundia on sheep, cows and horses, and hunting camps on them.'),
             ('Fourni par les p&#226;turages et les latifundia sur les moutons, les vaches et les chevaux.', 'Fourni par les p&#226;turages et les latifundia sur les moutons, les vaches et les chevaux, et par les camps de chasse sur ces animaux.'),
             ('Aus Weiden und Latifundien auf Schafen, Rindern und Pferden.', 'Aus Weiden und Latifundien auf Schafen, Rindern und Pferden und aus Jagdlagern auf ihnen.'),
             ('Dai pascoli e dai latifondi su pecore, mucche e cavalli.', 'Dai pascoli e dai latifondi su pecore, mucche e cavalli, e dai campi di caccia su di essi.'),
             ('De los pastos y latifundios sobre ovejas, vacas y caballos.', 'De los pastos y latifundios sobre ovejas, vacas y caballos, y de los campamentos de caza sobre ellos.')]:
    e(T, o, n)

pairs = []
for f, old, new in [(x[1], x[2], x[3]) if x[0] == 'CAMP' else x for x in E]:
    p = os.path.join(mod, f)
    s = open(p, 'rb').read().decode('latin-1')
    nl = '\r\n' if '\r\n' in s else '\n'
    if old is None:  # the hunting camp: insert after its BonusTypeStructs
        r0 = s.index('<Type>IMPROVEMENT_CAMP</Type>'); r1 = s.index('</ImprovementInfo>', r0)
        assert '<ProducedBonuses>' not in s[r0:r1]
        k = s.index('</BonusTypeStructs>' + nl, r0) + len('</BonusTypeStructs>' + nl); assert k < r1
        a = s.rfind(nl, 0, k - len(nl)) + len(nl); b = s.find(nl, k) + len(nl)
        while s.count(s[a:b]) != 1: b = s.find(nl, b) + len(nl)
        o = s[a:b]; n = s[a:k] + new.replace('\n', nl) + s[k:b]
    else:
        o, n = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(o) == 1, (f, s.count(o), (old or '')[:80])
    s = s.replace(o, n)
    open(p, 'wb').write(s.encode('latin-1'))
    pairs.append({'file': f, 'old': o, 'new': n})
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(x)) for x in pairs), 'bytes of JSON')
