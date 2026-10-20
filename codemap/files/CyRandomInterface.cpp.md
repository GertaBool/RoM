# CyRandomInterface.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `CvRandom_get_overloads::CvRandom_get_overloads<2>(boost::python::detail::keywords<2> const&, char const*)`
  - called by (1): CyRandomPythonInterface
- **6** `CvRandom_get_overloads::non_void_return_type::gen<boost::mpl::vector4<unsigned short, CvRandom&, unsigned short, char const*>>::func_0(CvRandom&, unsigned short, char const*)` (static)
  - calls: CvRandom::get [CvRandom.cpp]
- **12** `CyRandomPythonInterface()`
  - calls: CvRandom_get_overloads::CvRandom_get_overloads<2>
  - takes the address of: CvRandom::init [CvRandom.cpp], CvRandom::get [CvRandom.cpp]
  - called by (1): DLLPublishToPython
