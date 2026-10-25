# AIPathReuse.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **27** `AIPathReuse::sameKey(AIPathReuse::Key const&, AIPathReuse::Key const&)`
  - called by (1): AIPathReuse::Owner::admit
- **36** `AIPathReuse::Owner::Owner()`
  - called by (2): , 
- **46** `AIPathReuse::Owner::admit(AIPathReuse::Key const&, bool)`
  - calls: AIPathReuse::sameKey
  - called by (1): `anonymous namespace'::generatePathOn
- **54** `AIPathReuse::Owner::invalidate()`
  - called by (2): CvSelectionGroup::initSecondaryPathFinder, CvSelectionGroup::releaseSecondaryPathFinder
