# FDataStreamBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **39** `FDataStreamBase::WriteString(…)` (virtual; pure virtual, provided by the exe)
  - called by (34): CvBonusInfo::write, CvBuildingInfo::write, CvCity::write, CvCivicInfo::write, CvCivilizationInfo::write, CvDiploParameters::write, CvDiplomacyResponse::write, CvDiplomacyTextInfo::Response::write, CvEventInfo::write, CvEventTriggerInfo::write, CvGame::write, CvGameRecord::write …
- **46** `FDataStreamBase::ReadString(…)` (virtual; pure virtual, provided by the exe)
  - called by (34): CvBonusInfo::read(FDataStreamBase*), CvBuildingInfo::read(FDataStreamBase*), CvCity::read, CvCivicInfo::read(FDataStreamBase*), CvCivilizationInfo::read(FDataStreamBase*), CvDiploParameters::read, CvDiplomacyResponse::read(FDataStreamBase*), CvDiplomacyTextInfo::Response::read, CvEventInfo::read(FDataStreamBase*), CvEventTriggerInfo::read(FDataStreamBase*), CvGame::read, CvGameRecord::read …
- **54** `FDataStreamBase::ReadWideString(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): FVariable::Read
- **56** `FDataStreamBase::Read(…)` (virtual; pure virtual, provided by the exe)
  - called by (110): BuildingCommerceChange::read, BuildingYieldChange::read, CLinkList<IDInfo>::Read, CLinkList<MissionData>::Read, CLinkList<OrderData>::Read, CLinkList<TechTypes>::Read, CLinkList<TradeData>::Read, CLinkList<XYCoords>::Read, CLinkList<int>::Read, CvArea::read, CvBonusInfo::read(FDataStreamBase*), CvBuildingInfo::read(FDataStreamBase*) …
- **82** `FDataStreamBase::Write(…)` (virtual; pure virtual, provided by the exe)
  - called by (110): BuildingCommerceChange::write, BuildingYieldChange::write, CLinkList<IDInfo>::Write, CLinkList<MissionData>::Write, CLinkList<OrderData>::Write, CLinkList<TechTypes>::Write, CLinkList<TradeData>::Write, CLinkList<XYCoords>::Write, CLinkList<int>::Write, CvArea::write, CvBonusInfo::write, CvBuildingInfo::write …
