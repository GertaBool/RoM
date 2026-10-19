# FInputDevice.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **194** `FInputDevice::compStruct::operator()(const InputType, const InputType)`
- **198** `FInputDevice::InputValue::InputValue(const InputValue &)`
  - called by (1): FInputDevice::InputEvent::InputEvent(InputType, InputValue, uint)
- **202** `FInputDevice::InputValue::InputValue(int, int, int)`
- **203** `FInputDevice::InputValue::operator==(const InputValue &)`
  - called by (1): FInputDevice::InputEvent::operator==
- **212** `FInputDevice::InputEvent::InputEvent()`
- **213** `FInputDevice::InputEvent::InputEvent(InputType, InputValue, uint)`
  - calls: FInputDevice::InputValue::InputValue(const InputValue &)
- **214** `FInputDevice::InputEvent::operator==(const InputEvent &)`
  - calls: FInputDevice::InputValue::operator==
  - takes the address of: FInputDevice::InputValue::operator==
- **219** `FInputDevice::FInputDevice()` (declared, not defined in the source)
- **220** `FInputDevice::~FInputDevice()` (virtual; declared, not defined in the source)
- **222** `FInputDevice::Init(unsigned long)` (declared, not defined in the source)
- **223** `FInputDevice::UnInit()` (declared, not defined in the source)
- **225** `FInputDevice::ReadInputs()` (virtual; pure virtual, provided by the exe)
- **227** `FInputDevice::GetFlags()`
- **230** `FInputDevice::GetInputEvents()`
- **231** `FInputDevice::GetNumInputEvents()`
- **232** `FInputDevice::GetInputEvent(int)`
- **235** `FInputDevice::GetInputImmediate(InputType)` (virtual; pure virtual, provided by the exe)
- **238** `FInputDevice::AddHotKeyMapping(InputType, InputType)` (declared, not defined in the source)
- **239** `FInputDevice::RemoveHotKeyMapping(InputType)` (declared, not defined in the source)
- **240** `FInputDevice::ClearHotKeyMappings()` (declared, not defined in the source)
- **241** `FInputDevice::TranslateHotKey(InputType)` (declared, not defined in the source)
- **245** `FInputDevice::IInit()` (virtual; pure virtual, provided by the exe)
- **246** `FInputDevice::IUnInit()` (virtual; pure virtual, provided by the exe)
