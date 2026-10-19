# CvDLLIniParserIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **13** `CvDLLIniParserIFaceBase::create(const char *)` (virtual; pure virtual, provided by the exe)
- **14** `CvDLLIniParserIFaceBase::destroy(FIniParser *&, bool)` (virtual; pure virtual, provided by the exe)
- **15** `CvDLLIniParserIFaceBase::SetGroupKey(FIniParser *, const LPCTSTR)` (virtual; pure virtual, provided by the exe)
- **16** `CvDLLIniParserIFaceBase::GetKeyValue(FIniParser *, const LPCTSTR, bool *)` (virtual; pure virtual, provided by the exe)
- **17** `CvDLLIniParserIFaceBase::GetKeyValue(FIniParser *, const LPCTSTR, short *)` (virtual; pure virtual, provided by the exe)
- **18** `CvDLLIniParserIFaceBase::GetKeyValue(FIniParser *, const LPCTSTR, int *)` (virtual; pure virtual, provided by the exe)
- **19** `CvDLLIniParserIFaceBase::GetKeyValue(FIniParser *, const LPCTSTR, float *)` (virtual; pure virtual, provided by the exe)
- **20** `CvDLLIniParserIFaceBase::GetKeyValue(FIniParser *, const LPCTSTR, LPTSTR)` (virtual; pure virtual, provided by the exe)
