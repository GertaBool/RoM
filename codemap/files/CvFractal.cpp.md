# CvFractal.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **17** `CvFractal::CvFractal()` (exported)
  - calls: CvFractal::reset
- **22** `CvFractal::~CvFractal()` (exported; virtual)
  - calls: CvFractal::uninit
  - called by (1): CvFractal::`vector deleting dtor'
- **27** `CvFractal::uninit()` (exported)
  - calls: operator delete[](void*) [CvGameCoreDLL.cpp]
  - called by (1): CvFractal::~CvFractal
- **39** `CvFractal::reset()` (exported)
  - called by (2): CvFractal::CvFractal, CvFractal::fracInitInternal
- **51** `CvFractal::fracInit(int, int, int, CvRandom&, int, CvFractal*, int, int)` (exported)
  - calls: CvFractal::fracInitInternal
- **62** `CvFractal::fracInitHinted(int, int, int, CvRandom&, unsigned char*, int, int, CvFractal*, int, int)` (exported)
  - calls: CvFractal::fracInitInternal
- **68** `CvFractal::fracInitInternal(int, int, int, CvRandom&, unsigned char*, int, int, CvFractal*, int, int)`
  - calls: CvFractal::reset, operator new[](unsigned int) [CvGameCoreDLL.cpp], range(int, int, int) [CvGameCoreUtils.h], CvDLLUtilityIFaceBase::callUpdater [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvRandom::get [CvRandom.cpp], CvFractal::tectonicAction
  - called by (2): CvFractal::fracInit, CvFractal::fracInitHinted
- **277** `CvFractal::getHeight(int, int)` (exported)
  - calls: range(int, int, int) [CvGameCoreUtils.h]
- **325** `CvFractal::getHeightFromPercent(int)` (exported)
  - calls: range(int, int, int) [CvGameCoreUtils.h]
- **371** `CvFractal::tectonicAction(CvFractal*)`
  - calls: CvFractal::yieldX
  - called by (1): CvFractal::fracInitInternal
- **405** `CvFractal::yieldX(int)`
  - called by (1): CvFractal::tectonicAction
- **·** `CvFractal::`vector deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: CvFractal::~CvFractal, operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp]
  - takes the address of: CvFractal::~CvFractal
