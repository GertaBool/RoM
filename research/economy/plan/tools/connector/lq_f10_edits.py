"""LQ.F10 (and the mechanism LQ.F11 uses): improvements produce goods (ProducedBonuses), the lumber camp.
Applies the edits to a mod checkout (CRLF files; old and new written with \n here) and writes the (old, new) pairs
for the GitLab connector, each unique in its file as the earlier pairs leave it.
usage: lq_f10_edits.py <mod checkout> <pairs.json out> [part ...]   (parts: dll, xml; default both)"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
parts = sys.argv[3:] or ['dll', 'xml']
D = 'Assets/CvGameCoreDLL/'
E = []  # (part, file, old, new)

def e(part, f, old, new): E.append((part, f, old, new))

# ---------- DLL: CvImprovementInfo carries the goods it produces ----------
e('dll', D + 'CvInfos.h',
"""	int getImprovementBonusDiscoverRand(int i) const;				// Exposed to Python
	
	// Other
""",
"""	int getImprovementBonusDiscoverRand(int i) const;				// Exposed to Python

	// Settlement economy: goods the improvement yields to the trade network, beside a resource on its plot
	int getNumProducedBonuses() const;
	BonusTypes getProducedBonus(int i) const;
	BonusTypes getProducedBonusPrereq(int i) const;		// the resource the plot must have; NO_BONUS: any plot
	
	// Other
""")
e('dll', D + 'CvInfos.h',
"""	CvImprovementBonusInfo* m_paImprovementBonus;

};
""",
"""	CvImprovementBonusInfo* m_paImprovementBonus;

	std::vector<std::pair<BonusTypes, BonusTypes> > m_aProducedBonuses;	// (good produced, resource the plot must have or NO_BONUS)

};
""")
e('dll', D + 'CvInfos.cpp',
"""	return m_paImprovementBonus[i].m_iDiscoverRand; 
}

const TCHAR* CvImprovementInfo::getButton() const
""",
"""	return m_paImprovementBonus[i].m_iDiscoverRand; 
}

int CvImprovementInfo::getNumProducedBonuses() const
{
	return (int)m_aProducedBonuses.size();
}

BonusTypes CvImprovementInfo::getProducedBonus(int i) const
{
	FAssertMsg(i < getNumProducedBonuses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aProducedBonuses[i].first;
}

BonusTypes CvImprovementInfo::getProducedBonusPrereq(int i) const
{
	FAssertMsg(i < getNumProducedBonuses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aProducedBonuses[i].second;
}

const TCHAR* CvImprovementInfo::getButton() const
""")
# stream cache: version 1 of the record carries the list after the route yields
e('dll', D + 'CvInfos.cpp',
"""		m_ppiRouteYieldChanges[i]  = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
	}
}

void CvImprovementInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);

	uint uiFlag=0;
""",
"""		m_ppiRouteYieldChanges[i]  = new int[NUM_YIELD_TYPES];
		stream->Read(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
	}

	m_aProducedBonuses.clear();
	if (uiFlag >= 1)
	{
		int iNum;
		stream->Read(&iNum);
		for (i = 0; i < iNum; i++)
		{
			int iProduced, iPrereq;
			stream->Read(&iProduced);
			stream->Read(&iPrereq);
			m_aProducedBonuses.push_back(std::make_pair((BonusTypes)iProduced, (BonusTypes)iPrereq));
		}
	}
}

void CvImprovementInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);

	uint uiFlag=1;
""")
e('dll', D + 'CvInfos.cpp',
"""	for(i=0;i<GC.getNumRouteInfos();i++)
	{
		stream->Write(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
	}
}
bool CvImprovementInfo::read(CvXMLLoadUtility* pXML)
""",
"""	for(i=0;i<GC.getNumRouteInfos();i++)
	{
		stream->Write(NUM_YIELD_TYPES, m_ppiRouteYieldChanges[i]);
	}

	stream->Write((int)m_aProducedBonuses.size());
	for (i = 0; i < (int)m_aProducedBonuses.size(); i++)
	{
		stream->Write((int)m_aProducedBonuses[i].first);
		stream->Write((int)m_aProducedBonuses[i].second);
	}
}
bool CvImprovementInfo::read(CvXMLLoadUtility* pXML)
""")
e('dll', D + 'CvInfos.cpp',
"""		pXML->InitImprovementBonusList(&m_paImprovementBonus, GC.getNumBonusInfos());
	}
""",
"""		pXML->InitImprovementBonusList(&m_paImprovementBonus, GC.getNumBonusInfos());
	}

	// <ProducedBonuses><ProducedBonus><BonusType/>[<PrereqBonus/>]</ProducedBonus>...</ProducedBonuses>
	m_aProducedBonuses.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ProducedBonuses"))
	{
		if (pXML->SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				for (j = 0; j < iNumSibs; j++)
				{
					pXML->GetChildXmlValByName(szTextVal, "BonusType");
					int iProduced = pXML->FindInInfoClass(szTextVal);
					pXML->GetChildXmlValByName(szTextVal, "PrereqBonus");
					int iPrereq = (szTextVal.GetLength() > 0) ? pXML->FindInInfoClass(szTextVal) : NO_BONUS;
					if (iProduced > -1)
					{
						m_aProducedBonuses.push_back(std::make_pair((BonusTypes)iProduced, (BonusTypes)iPrereq));
					}

					if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					{
						break;
					}
				}

				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}

		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
""")
e('dll', D + 'CvInfos.cpp',
"""	if (m_iWorldSoundscapeScriptId == iTextDefault) m_iWorldSoundscapeScriptId = pClassInfo->getWorldSoundscapeScriptId();
	//Readpass2 stuff
	if (m_iImprovementPillage == iTextDefault) m_iImprovementPillage = pClassInfo->getImprovementPillage();
""",
"""	if (m_iWorldSoundscapeScriptId == iTextDefault) m_iWorldSoundscapeScriptId = pClassInfo->getWorldSoundscapeScriptId();
	if (m_aProducedBonuses.empty()) m_aProducedBonuses = pClassInfo->m_aProducedBonuses;
	//Readpass2 stuff
	if (m_iImprovementPillage == iTextDefault) m_iImprovementPillage = pClassInfo->getImprovementPillage();
""")

# ---------- DLL: the plot adds the goods to its plot group ----------
e('dll', D + 'CvPlot.h',
"""	bool isBonusNetwork(TeamTypes eTeam) const;""",
"""	bool isBonusNetwork(TeamTypes eTeam) const;
	bool isBonusTech(TechTypes eTech) const;	// eTech reveals, trades or obsoletes a good the plot gives""")
e('dll', D + 'CvPlot.cpp',
"""					if ((pPlotGroup != NULL) && isBonusNetwork(getTeam()))
					{
						pPlotGroup->changeNumBonuses(eNonObsoleteBonus, ((bAdd) ? 1 : -1));
					}
				}
			}
		}
	}
}
""",
"""					if ((pPlotGroup != NULL) && isBonusNetwork(getTeam()))
					{
						pPlotGroup->changeNumBonuses(eNonObsoleteBonus, ((bAdd) ? 1 : -1));
					}
				}
			}
		}

		// Settlement economy: goods the improvement produces (lumber camp: timber; pasture on sheep: wool ...)
		if ((getImprovementType() != NO_IMPROVEMENT) && isBonusNetwork(getTeam()))
		{
			CvImprovementInfo& kImprovement = GC.getImprovementInfo(getImprovementType());
			CvTeam& kTeam = GET_TEAM(getTeam());

			for (iI = 0; iI < kImprovement.getNumProducedBonuses(); ++iI)
			{
				BonusTypes eProduced = kImprovement.getProducedBonus(iI);
				BonusTypes ePrereq = kImprovement.getProducedBonusPrereq(iI);
				TechTypes eTrade = (TechTypes)GC.getBonusInfo(eProduced).getTechCityTrade();

				if ((ePrereq == NO_BONUS || ePrereq == eNonObsoleteBonus) &&
					!kTeam.isBonusObsolete(eProduced) &&
					(eTrade == NO_TECH || kTeam.isHasTech(eTrade)))
				{
					pPlotGroup->changeNumBonuses(eProduced, ((bAdd) ? 1 : -1));
				}
			}
		}
	}
}


bool CvPlot::isBonusTech(TechTypes eTech) const
{
	if (getBonusType() != NO_BONUS)
	{
		CvBonusInfo& kBonus = GC.getBonusInfo(getBonusType());
		if (kBonus.getTechReveal() == eTech || kBonus.getTechCityTrade() == eTech || kBonus.getTechObsolete() == eTech)
		{
			return true;
		}
	}

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		CvImprovementInfo& kImprovement = GC.getImprovementInfo(getImprovementType());
		for (int iI = 0; iI < kImprovement.getNumProducedBonuses(); ++iI)
		{
			CvBonusInfo& kProduced = GC.getBonusInfo(kImprovement.getProducedBonus(iI));
			if (kProduced.getTechCityTrade() == eTech || kProduced.getTechObsolete() == eTech)
			{
				return true;
			}
		}
	}

	return false;
}
""")
# ---------- DLL: a tech that changes a produced good refreshes the plot (both brackets of setHasTech) ----------
for add in ('false', 'true'):
    e('dll', D + 'CvTeam.cpp',
"""				if (pLoopPlot->getBonusType() != NO_BONUS)
				{
					if (pLoopPlot->getTeam() == getID())
					{
						if ((GC.getBonusInfo(pLoopPlot->getBonusType()).getTechReveal() == eIndex) ||
							  (GC.getBonusInfo(pLoopPlot->getBonusType()).getTechCityTrade() == eIndex) ||
""" + ("""								(GC.getBonusInfo(pLoopPlot->getBonusType()).getTechObsolete() == eIndex))
						{
							pLoopPlot->updatePlotGroupBonus(false);
						}
					}
				}
""" if add == 'false' else """							  (GC.getBonusInfo(pLoopPlot->getBonusType()).getTechObsolete() == eIndex))
						{
							pLoopPlot->updatePlotGroupBonus(true);
						}
					}
				}
"""),
"""				if (pLoopPlot->getTeam() == getID() && pLoopPlot->isBonusTech(eIndex))
				{
					pLoopPlot->updatePlotGroupBonus(%s);
				}
""" % add)


# ---------- DLL: helper and the city AI's build choice ----------
e('dll', D + 'CvInfos.h',
"""	BonusTypes getProducedBonusPrereq(int i) const;		// the resource the plot must have; NO_BONUS: any plot
""",
"""	BonusTypes getProducedBonusPrereq(int i) const;		// the resource the plot must have; NO_BONUS: any plot
	bool isProducedBonus(BonusTypes eProduced, BonusTypes ePlotBonus) const;	// produced on a plot with that resource
""")
e('dll', D + 'CvInfos.cpp',
"""	return m_aProducedBonuses[i].second;
}
""",
"""	return m_aProducedBonuses[i].second;
}

bool CvImprovementInfo::isProducedBonus(BonusTypes eProduced, BonusTypes ePlotBonus) const
{
	for (int i = 0; i < getNumProducedBonuses(); i++)
	{
		if (m_aProducedBonuses[i].first == eProduced && (m_aProducedBonuses[i].second == NO_BONUS || m_aProducedBonuses[i].second == ePlotBonus))
		{
			return true;
		}
	}
	return false;
}
""")
e('dll', D + 'CvCityAI.cpp',
"""/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

				iValue = 0;
				
				if (eBonus != NO_BONUS)
				{
/*************************************************************************************************/
/**	Forts Connect Resources									02/12/10			Xienwolf & Fuyu	**/
""",
"""/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

				iValue = 0;

				// Settlement economy: a good the improvement produces counts like a connected resource when the city
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
				
				if (eBonus != NO_BONUS)
				{
/*************************************************************************************************/
/**	Forts Connect Resources									02/12/10			Xienwolf & Fuyu	**/
""")

e('dll', D + 'CvGameTextMgr.cpp',
"""		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_EVOLVES", GC.getImprovementInfo((ImprovementTypes) info.getImprovementUpgrade()).getTextKeyWide(), iTurns));
	}
""",
"""		szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_EVOLVES", GC.getImprovementInfo((ImprovementTypes) info.getImprovementUpgrade()).getTextKeyWide(), iTurns));
	}

	// Settlement economy: goods the improvement gives to the trade network
	for (int iProduced = 0; iProduced < info.getNumProducedBonuses(); iProduced++)
	{
		CvBonusInfo& kProduced = GC.getBonusInfo(info.getProducedBonus(iProduced));
		szBuffer.append(NEWLINE);
		if (info.getProducedBonusPrereq(iProduced) == NO_BONUS)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_PRODUCES_BONUS", kProduced.getChar(), kProduced.getTextKeyWide()));
		}
		else
		{
			CvBonusInfo& kPrereq = GC.getBonusInfo(info.getProducedBonusPrereq(iProduced));
			szBuffer.append(gDLL->getText("TXT_KEY_IMPROVEMENT_PRODUCES_BONUS_ON", kProduced.getChar(), kProduced.getTextKeyWide(), kPrereq.getChar(), kPrereq.getTextKeyWide()));
		}
	}
""")

# ---------- XML ----------
X = 'Assets/XML/'
# schema: the list, after BonusTypeStructs
e('xml', X + 'Terrain/CIV4TerrainSchema.xml',
"""	<ElementType name="ImprovementInfo" content="eltOnly">
""",
"""	<ElementType name="PrereqBonus" content="textOnly"/>
	<ElementType name="ProducedBonus" content="eltOnly">
		<element type="BonusType"/>
		<element type="PrereqBonus" minOccurs="0"/>
	</ElementType>
	<ElementType name="ProducedBonuses" content="eltOnly">
		<element type="ProducedBonus" minOccurs="0" maxOccurs="*"/>
	</ElementType>
	<ElementType name="ImprovementInfo" content="eltOnly">
""")
e('xml', X + 'Terrain/CIV4TerrainSchema.xml',
"""		<element type="BonusTypeStructs" minOccurs="0" maxOccurs="*"/>
		<element type="ImprovementPillage" minOccurs="0"/>
""",
"""		<element type="BonusTypeStructs" minOccurs="0" maxOccurs="*"/>
		<element type="ProducedBonuses" minOccurs="0"/>
		<element type="ImprovementPillage" minOccurs="0"/>
""")
# the lumbermill gives timber; production 2 -> 4 (the camp's three tech steps plus one at Machinery; open, D19)
e('xml', X + 'Terrain/CIV4ImprovementInfos.xml',
"""			<Type>IMPROVEMENT_LUMBERMILL</Type>
			<Description>TXT_KEY_IMPROVEMENT_LUMBERMILL</Description>
			<Civilopedia>TXT_KEY_IMPROVEMENT_LUMBERMILL_PEDIA</Civilopedia>
			<ArtDefineTag>ART_DEF_IMPROVEMENT_LUMBERMILL</ArtDefineTag>
			<YieldChanges>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>2</iYieldChange>
""",
"""			<Type>IMPROVEMENT_LUMBERMILL</Type>
			<Description>TXT_KEY_IMPROVEMENT_LUMBERMILL</Description>
			<Civilopedia>TXT_KEY_IMPROVEMENT_LUMBERMILL_PEDIA</Civilopedia>
			<ArtDefineTag>ART_DEF_IMPROVEMENT_LUMBERMILL</ArtDefineTag>
			<YieldChanges>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>4</iYieldChange>
""")
e('xml', X + 'Terrain/CIV4ImprovementInfos.xml',
"""					<FeatureType>FEATURE_FOREST</FeatureType>
					<bMakesValid>1</bMakesValid>
				</FeatureMakesValid>
			</FeatureMakesValids>
			<ImprovementPillage/>
			<ImprovementUpgrade/>
			<TechYieldChanges>
				<TechYieldChange>
					<PrereqTech>TECH_WATERWORKS</PrereqTech>
""",
"""					<FeatureType>FEATURE_FOREST</FeatureType>
					<bMakesValid>1</bMakesValid>
				</FeatureMakesValid>
			</FeatureMakesValids>
			<ProducedBonuses>
				<ProducedBonus>
					<BonusType>BONUS_TIMBER</BonusType>
				</ProducedBonus>
			</ProducedBonuses>
			<ImprovementPillage/>
			<ImprovementUpgrade/>
			<TechYieldChanges>
				<TechYieldChange>
					<PrereqTech>TECH_WATERWORKS</PrereqTech>
""")
CAMP_TECH = ''.join("""				<TechYieldChange>
					<PrereqTech>%s</PrereqTech>
					<TechYields>
						<iYield>0</iYield>
						<iYield>1</iYield>
						<iYield>0</iYield>
					</TechYields>
				</TechYieldChange>
""" % t for t in ('TECH_BRONZE_WORKING', 'TECH_IRON_WORKING', 'TECH_MATHEMATICS'))
e('xml', X + 'Terrain/CIV4ImprovementInfos.xml',
"""		</ImprovementInfo>
	</ImprovementInfos>
""",
"""		</ImprovementInfo>
		<ImprovementInfo>
			<Type>IMPROVEMENT_LUMBER_CAMP</Type>
			<Description>TXT_KEY_IMPROVEMENT_LUMBER_CAMP</Description>
			<Civilopedia>TXT_KEY_IMPROVEMENT_LUMBER_CAMP_PEDIA</Civilopedia>
			<ArtDefineTag>ART_DEF_IMPROVEMENT_LUMBER_CAMP</ArtDefineTag>
			<YieldChanges>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>0</iYieldChange>
				<iYieldChange>0</iYieldChange>
			</YieldChanges>
			<bActsAsCity>0</bActsAsCity>
			<bRequiresFeature>1</bRequiresFeature>
			<iAdvancedStartCost>20</iAdvancedStartCost>
			<iAirBombDefense>5</iAirBombDefense>
			<iPillageGold>3</iPillageGold>
			<FeatureMakesValids>
				<FeatureMakesValid>
					<FeatureType>FEATURE_FOREST</FeatureType>
					<bMakesValid>1</bMakesValid>
				</FeatureMakesValid>
			</FeatureMakesValids>
			<ProducedBonuses>
				<ProducedBonus>
					<BonusType>BONUS_TIMBER</BonusType>
				</ProducedBonus>
			</ProducedBonuses>
			<TechYieldChanges>
""" + CAMP_TECH + """			</TechYieldChanges>
			<bGraphicalOnly>0</bGraphicalOnly>
		</ImprovementInfo>
	</ImprovementInfos>
""")
e('xml', X + 'Units/CIV4BuildInfos.xml',
"""		</BuildInfo>
	</BuildInfos>
""",
"""		</BuildInfo>
		<BuildInfo>
			<Type>BUILD_LUMBER_CAMP</Type>
			<Description>TXT_KEY_BUILD_LUMBER_CAMP</Description>
			<Help/>
			<PrereqTech>TECH_METAL_CASTING</PrereqTech>
			<iTime>400</iTime>
			<iCost>0</iCost>
			<bKill>0</bKill>
			<ImprovementType>IMPROVEMENT_LUMBER_CAMP</ImprovementType>
			<RouteType>NONE</RouteType>
			<EntityEvent>ENTITY_EVENT_BUILD</EntityEvent>
			<FeatureStructs>
				<FeatureStruct>
					<FeatureType>FEATURE_FOREST</FeatureType>
					<PrereqTech>TECH_METAL_CASTING</PrereqTech>
					<iTime>100</iTime>
					<iProduction>0</iProduction>
					<bRemove>0</bRemove>
				</FeatureStruct>
			</FeatureStructs>
			<HotKey/>
			<bAltDown>0</bAltDown>
			<bShiftDown>0</bShiftDown>
			<bCtrlDown>0</bCtrlDown>
			<iHotKeyPriority>1</iHotKeyPriority>
			<Button>,Art/Interface/Buttons/Builds/BuildCamp.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,1,7</Button>
		</BuildInfo>
	</BuildInfos>
""")
e('xml', X + 'Art/CIV4ArtDefines_Improvement.xml',
"""		</ImprovementArtInfo>
	</ImprovementArtInfos>
""",
"""		</ImprovementArtInfo>
		<ImprovementArtInfo>
			<Type>ART_DEF_IMPROVEMENT_LUMBER_CAMP</Type>
			<bExtraAnimations>0</bExtraAnimations>
			<fScale>1.0</fScale>
			<fInterfaceScale>1.0</fInterfaceScale>
			<NIF>Art/Structures/Improvements/Camp/Camp.nif</NIF>
			<KFM>Art/Structures/Improvements/Camp/Camp.kfm</KFM>
			<Button>,Art/Interface/Buttons/Builds/BuildCamp.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,1,7</Button>
		</ImprovementArtInfo>
	</ImprovementArtInfos>
""")
# Timber trades from Metal Casting, when the camp can be built (D19, M36); TechReveal stays NONE (Timber is never placed)
e('xml', X + 'Terrain/CIV4BonusInfos.xml',
"""			<ArtDefineTag>ART_DEF_BONUS_TIMBER</ArtDefineTag>
			<TechReveal>NONE</TechReveal>
			<TechCityTrade>TECH_BRONZE_WORKING</TechCityTrade>
""",
"""			<ArtDefineTag>ART_DEF_BONUS_TIMBER</ArtDefineTag>
			<TechReveal>NONE</TechReveal>
			<TechCityTrade>TECH_METAL_CASTING</TechCityTrade>
""")
def text(tag, en, fr, de, it, es):
    ref = lambda x: ''.join(c if ord(c) < 128 else '&#%d;' % ord(c) for c in x)
    return """	<TEXT>
		<Tag>%s</Tag>
		<English>%s</English>
		<French>%s</French>
		<German>%s</German>
		<Italian>%s</Italian>
		<Spanish>%s</Spanish>
		<Finnish></Finnish>
		<Hungarian></Hungarian>
		<Polish></Polish>
		<Russian></Russian>
		<Chinese></Chinese>
		<Japanese></Japanese>
	</TEXT>
""" % (tag, ref(en), ref(fr), ref(de), ref(it), ref(es))
e('xml', X + 'Text/RoM_GameText_SettlementEconomy.xml',
"""</Civ4GameText>""",
text('TXT_KEY_IMPROVEMENT_LUMBER_CAMP', 'Lumber Camp', 'Camp de bûcherons', 'Holzfällerlager', 'Campo di taglialegna', 'Campamento maderero') +
text('TXT_KEY_IMPROVEMENT_PRODUCES_BONUS', '[ICON_BULLET]Provides %F1 %s2 to the trade network', '[ICON_BULLET]Fournit %F1 %s2 au r\u00e9seau commercial', '[ICON_BULLET]Liefert %F1 %s2 ins Handelsnetz', '[ICON_BULLET]Fornisce %F1 %s2 alla rete commerciale', '[ICON_BULLET]Proporciona %F1 %s2 a la red comercial') +
text('TXT_KEY_IMPROVEMENT_PRODUCES_BONUS_ON', '[ICON_BULLET]On %F3 %s4: provides %F1 %s2 to the trade network', '[ICON_BULLET]Sur %F3 %s4 : fournit %F1 %s2 au r\u00e9seau commercial', '[ICON_BULLET]Auf %F3 %s4: liefert %F1 %s2 ins Handelsnetz', '[ICON_BULLET]Su %F3 %s4: fornisce %F1 %s2 alla rete commerciale', '[ICON_BULLET]Sobre %F3 %s4: proporciona %F1 %s2 a la red comercial') +
text('TXT_KEY_BUILD_LUMBER_CAMP', 'Build Lumber Camp', 'Construire un camp de bûcherons', 'Holzfällerlager bauen', 'Costruisci campo di taglialegna', 'Construir campamento maderero') +
text('TXT_KEY_IMPROVEMENT_LUMBER_CAMP_PEDIA',
 '[TAB]A lumber camp is where woodcutters fell trees, trim them and drag the logs out of the forest. It keeps the forest standing and sends timber to every city on the trade network. Better tools of bronze and iron, and the measuring of mathematics, make each camp yield more. With machinery the camp can become a lumbermill.',
 "[TAB]Le camp de bûcherons est le lieu où l'on abat les arbres, les ébranche et tire les grumes hors de la forêt. La forêt reste debout et le bois part vers chaque ville du réseau commercial. De meilleurs outils de bronze et de fer, et la mesure qu'apportent les mathématiques, accroissent le rendement de chaque camp. Avec la mécanique, le camp peut devenir une scierie.",
 '[TAB]Im Holzfällerlager fällen Holzfäller Bäume, entasten sie und ziehen die Stämme aus dem Wald. Der Wald bleibt stehen, und das Holz geht an jede Stadt im Handelsnetz. Bessere Werkzeuge aus Bronze und Eisen und das Messen der Mathematik steigern den Ertrag jedes Lagers. Mit der Mechanik kann aus dem Lager ein Sägewerk werden.',
 "[TAB]Il campo di taglialegna è il luogo dove si abbattono gli alberi, si sramano e si trascinano i tronchi fuori dalla foresta. La foresta resta in piedi e il legname va a ogni città della rete commerciale. Attrezzi migliori di bronzo e di ferro, e la misura della matematica, aumentano la resa di ogni campo. Con la meccanica il campo può diventare una segheria.",
 '[TAB]El campamento maderero es donde los leñadores talan los árboles, los desraman y sacan los troncos del bosque. El bosque sigue en pie y la madera llega a cada ciudad de la red comercial. Mejores herramientas de bronce y de hierro, y la medida de las matemáticas, aumentan el rendimiento de cada campamento. Con la maquinaria el campamento puede convertirse en un aserradero.') +
"""</Civ4GameText>""")

# every unit that can build a lumbermill can build a lumber camp (CvUnitInfo Builds: without it no worker builds one)
EACH = []  # (part, file, old, new): applied at every occurrence, each pair made unique by widening it by lines
EACH.append(('xml', X + 'Units/CIV4UnitInfos.xml',
"""				<Build>
					<BuildType>BUILD_LUMBERMILL</BuildType>
					<bBuild>1</bBuild>
				</Build>
""",
"""				<Build>
					<BuildType>BUILD_LUMBERMILL</BuildType>
					<bBuild>1</bBuild>
				</Build>
				<Build>
					<BuildType>BUILD_LUMBER_CAMP</BuildType>
					<bBuild>1</bBuild>
				</Build>
"""))

# ---------- apply ----------
pairs = []
for part, f, old, new in E:
    if part not in parts: continue
    p = os.path.join(mod, f)
    s = open(p, 'rb').read().decode('latin-1')
    crlf = '\r\n' in s
    o, n = (old.replace('\n', '\r\n'), new.replace('\n', '\r\n')) if crlf else (old, new)
    assert s.count(o) == 1, (f, s.count(o), old[:100])
    s = s.replace(o, n)
    open(p, 'wb').write(s.encode('latin-1'))
    pairs.append({'file': f, 'old': o, 'new': n})
for part, f, old, new in EACH:
    if part not in parts: continue
    p = os.path.join(mod, f)
    s = open(p, 'rb').read().decode('latin-1')
    crlf = '\r\n' in s
    nl = '\r\n' if crlf else '\n'
    o, n = (old.replace('\n', nl), new.replace('\n', nl))
    pos = 0
    while True:
        i = s.find(o, pos)
        if i < 0: break
        # the shortest window around this occurrence (whole lines, any split before and after) unique in the file
        L = s[:i].split(nl); R = s[i + len(o):].split(nl)
        best = None
        for kb in range(0, 200):
            a = i - len(nl.join(L[len(L) - kb:])) - (len(nl) if kb else 0) if kb else i
            if kb and kb > len(L): break
            for kf in range(0, 200):
                b = i + len(o) + (len(nl.join(R[:kf])) + (len(nl) if kf else 0) if kf else 0)
                if best is not None and b - a >= best[1] - best[0]: break
                if s.count(s[a:b]) == 1:
                    best = (a, b); break
        a, b = best
        old_w = s[a:b]; new_w = s[a:i] + n + s[i + len(o):b]
        pairs.append({'file': f, 'old': old_w, 'new': new_w})
        s = s[:a] + new_w + s[b:]
        pos = a + len(new_w)
    open(p, 'wb').write(s.encode('latin-1'))
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(x)) for x in pairs), 'bytes of JSON')
