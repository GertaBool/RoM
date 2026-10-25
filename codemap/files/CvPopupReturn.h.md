# CvPopupReturn.h

Group: interface, text and messages. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **41** `PopupReturn::getSelectedRadioButton(int) const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **47** `PopupReturn::getRadioButtonSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **60** `PopupReturn::getCheckboxBitfield(int) const`
  - called by (3): CvDLLButtonPopup::OnOkClicked, PopupReturn::PopupReturn, PopupReturn::operator=
- **66** `PopupReturn::getCheckboxSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **79** `PopupReturn::getEditBoxString(int) const`
  - calls: CvWString::operator unsigned short const * [CvString.h]
  - called by (3): CvDLLButtonPopup::OnOkClicked, PopupReturn::PopupReturn, PopupReturn::operator=
- **88** `PopupReturn::getEditboxSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **101** `PopupReturn::getSpinnerWidgetValue(int) const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **107** `PopupReturn::getSpinnerWidsize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **119** `PopupReturn::getSelectedPullDownValue(int) const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **125** `PopupReturn::getPulldownSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **137** `PopupReturn::getSelectedListBoxValue(int) const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **143** `PopupReturn::getListBoxSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **161** `PopupReturn::getSpinBoxSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
- **173** `PopupReturn::getButtonClicked(int) const`
  - called by (3): CvDLLButtonPopup::OnOkClicked, PopupReturn::PopupReturn, PopupReturn::operator=
- **179** `PopupReturn::getButtonSize() const`
  - called by (2): PopupReturn::PopupReturn, PopupReturn::operator=
