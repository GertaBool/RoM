# FProfiler.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **26** `ProfileSample::ProfileSample(char *)`
- **47** `CProfileScope::CProfileScope()`
- **48** `CProfileScope::CProfileScope(ProfileSample *)`
  - calls: CvDLLUtilityIFaceBase::BeginSample [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **54** `CProfileScope::~CProfileScope()`
  - calls: CvDLLUtilityIFaceBase::EndSample [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
