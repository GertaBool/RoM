# AIPathReuse.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **18** `AIPathReuse::Key::Key()`
  - called by (1): pathReuseKey
- **18** `AIPathReuse::Key::Key(const Key &)`
  - called by (1): pathReuseKey
- **18** `AIPathReuse::Key::operator=(const Key &)`
  - called by (1): AIPathReuse::Owner::admit
- **26** `AIPathReuse::sameKey(const Key &, const Key &)`
  - called by (1): AIPathReuse::Owner::admit
- **35** `AIPathReuse::Owner::Owner()`
- **45** `AIPathReuse::Owner::admit(const Key &, const bool)`
  - calls: AIPathReuse::sameKey, AIPathReuse::Key::operator=
  - takes the address of: AIPathReuse::Key::operator=
  - called by (1): generatePathOn
- **53** `AIPathReuse::Owner::invalidate()`
  - called by (2): CvSelectionGroup::initSecondaryPathFinder, CvSelectionGroup::releaseSecondaryPathFinder
