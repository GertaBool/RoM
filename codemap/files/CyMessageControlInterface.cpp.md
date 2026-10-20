# CyMessageControlInterface.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **9** `CyMessageControlInterface()`
  - takes the address of: CyMessageControl::sendDoTask [CyMessageControl.cpp], CyMessageControl::sendTurnComplete [CyMessageControl.cpp], CyMessageControl::sendUpdateCivics [CyMessageControl.cpp], CyMessageControl::sendConvert [CyMessageControl.cpp], CyMessageControl::sendEmpireSplit [CyMessageControl.cpp], CyMessageControl::sendResearch [CyMessageControl.cpp], CyMessageControl::sendPlayerOption [CyMessageControl.cpp], CyMessageControl::sendEspionageSpendingWeightChange [CyMessageControl.cpp], CyMessageControl::sendAdvancedStartAction [CyMessageControl.cpp], CyMessageControl::sendModNetMessage [CyMessageControl.cpp], CyMessageControl::GetFirstBadConnection [CyMessageControl.cpp], CyMessageControl::GetConnState [CyMessageControl.cpp], CyMessageControl::sendPushOrder [CyMessageControl.cpp]
  - called by (1): DLLPublishToPython
