# CvFractal.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **16** `CvFractal::CvFractal()` (exported)
  - calls: CvFractal::reset
- **21** `CvFractal::~CvFractal()` (exported; virtual)
  - calls: CvFractal::uninit
- **26** `CvFractal::uninit()` (exported)
  - called by (1): CvFractal::~CvFractal
- **38** `CvFractal::reset()` (exported)
  - called by (2): CvFractal::CvFractal, CvFractal::fracInitInternal
- **50** `CvFractal::fracInit(int, int, int, CvRandom &, int, CvFractal *, int, int)` (exported)
  - calls: CvFractal::fracInitInternal
- **61** `CvFractal::fracInitHinted(int, int, int, CvRandom &, byte *, int, int, CvFractal *, int, int)` (exported)
  - calls: CvFractal::fracInitInternal
- **67** `CvFractal::fracInitInternal(int, int, int, CvRandom &, byte *, int, int, CvFractal *, int, int)`
  - calls: CvFractal::reset, range(int, int, int) [CvGameCoreUtils.h], CvDLLUtilityIFaceBase::callUpdater [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvRandom::get [CvRandom.cpp], CvFractal::tectonicAction
  - called by (2): CvFractal::fracInit, CvFractal::fracInitHinted
- **276** `CvFractal::getHeight(int, int)` (exported)
  - calls: range(int, int, int) [CvGameCoreUtils.h]
- **324** `CvFractal::getHeightFromPercent(int)` (exported)
  - calls: range(int, int, int) [CvGameCoreUtils.h]
- **370** `CvFractal::tectonicAction(CvFractal *)`
  - calls: CvFractal::yieldX
  - called by (1): CvFractal::fracInitInternal
- **404** `CvFractal::yieldX(int)`
  - called by (1): CvFractal::tectonicAction
