# CvMessageData.h

Group: interface, text and messages. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **11** `CvMessageData::Debug(char *)` (exported; virtual; pure virtual)
- **12** `CvMessageData::Execute()` (exported; virtual; pure virtual)
- **13** `CvMessageData::PutInBuffer(FDataStreamBase *)` (exported; virtual; pure virtual)
- **14** `CvMessageData::SetFromBuffer(FDataStreamBase *)` (exported; virtual; pure virtual)
