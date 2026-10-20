# FVariableSystem.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **53** `FVariable::FVariable()`
  - called by (6): FVariableSystem::SetValue(char const*, bool), FVariableSystem::SetValue(char const*, char const*), FVariableSystem::SetValue(char const*, float), FVariableSystem::SetValue(char const*, int), addVar(std::vector<FVariable, std::allocator<FVariable>>&, int), addVar(std::vector<FVariable, std::allocator<FVariable>>&, unsigned short const*)
- **54** `FVariable::FVariable(FVariable const&)`
  - calls: FVariable::CopyFrom [FVariableSystem.inl]
- **57** `FVariable::operator=(FVariable const&)`
  - calls: FVariable::CopyFrom [FVariableSystem.inl]
- **·** `FVariable::`scalar deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], FVariable::~FVariable [FVariableSystem.inl]
