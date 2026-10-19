# FVariableSystem.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **53** `FVariable::FVariable()`
  - called by (14): FVariableSystem::Read, FVariableSystem::SetValue(const char *, bool), FVariableSystem::SetValue(const char *, byte), FVariableSystem::SetValue(const char *, char), FVariableSystem::SetValue(const char *, const char *), FVariableSystem::SetValue(const char *, const wchar *), FVariableSystem::SetValue(const char *, double), FVariableSystem::SetValue(const char *, float), FVariableSystem::SetValue(const char *, int), FVariableSystem::SetValue(const char *, short), FVariableSystem::SetValue(const char *, uint), FVariableSystem::SetValue(const char *, word) …
- **54** `FVariable::FVariable(const FVariable &)`
  - calls: FVariable::CopyFrom [FVariableSystem.inl]
- **57** `FVariable::operator=(const FVariable &)`
  - calls: FVariable::CopyFrom [FVariableSystem.inl]
