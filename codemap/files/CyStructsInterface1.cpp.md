# CyStructsInterface1.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **12** `CyStructsPythonInterface1()`
  - takes the address of: EventMessage::getDescription [CvStructs.h], FOWVis::getOffsets [CvStructs.h], PBGameSetupData::getCustomMapOption [CvStructs.h], PBGameSetupData::getVictory [CvStructs.h], PBGameSetupData::getMapName [CvStructs.h], PBGameSetupData::getOptionAt [CvStructs.h], PBGameSetupData::getMPOptionAt [CvStructs.h], PBPlayerSetupData::getStatusText [CvStructs.h], PBPlayerAdminData::getName [CvStructs.h], PBPlayerAdminData::getPing [CvStructs.h], PBPlayerAdminData::getScore [CvStructs.h]
  - called by (1): DLLPublishToPython
