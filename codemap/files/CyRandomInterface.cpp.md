# CyRandomInterface.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `CvRandom_get_overloads::CvRandom_get_overloads(const char *)`
- **6** `CvRandom_get_overloads::CvRandom_get_overloads(const ::boost::python::detail::keywords<N> &, const char *)`
  - called by (1): CyRandomPythonInterface
- **6** `CvRandom_get_overloads::CvRandom_get_overloads(const char *, const ::boost::python::detail::keywords<N> &)`
- **6** `CvRandom_get_overloads::non_void_return_type::gen::func_0(ClassT, T0, T1)` (static)
- **11** `CyRandomPythonInterface()`
  - calls: CvRandom_get_overloads::CvRandom_get_overloads(const ::boost::python::detail::keywords<N> &, const char *)
  - takes the address of: CvRandom::get [CvRandom.cpp], CvRandom::init [CvRandom.cpp]
  - called by (1): DLLPublishToPython
