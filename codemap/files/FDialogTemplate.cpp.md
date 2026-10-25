# FDialogTemplate.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **12** `CDialogTemplate::CDialogTemplate(char const*, unsigned long, int, int, int, int, char const*, unsigned short)`
  - calls: CDialogTemplate::AppendData, CDialogTemplate::AppendString
- **48** `CDialogTemplate::~CDialogTemplate()`
- **54** `CDialogTemplate::AddComponent(char const*, char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AppendData, CDialogTemplate::AppendString
- **80** `CDialogTemplate::AddButton(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **89** `CDialogTemplate::AddEditBox(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **98** `CDialogTemplate::AddStatic(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **107** `CDialogTemplate::AddListBox(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **116** `CDialogTemplate::AddScrollBar(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **125** `CDialogTemplate::AddComboBox(char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **133** `CDialogTemplate::GetDialogTemplate() const`
- **139** `CDialogTemplate::AddStandardComponent(unsigned short, char const*, unsigned long, unsigned long, int, int, int, int, unsigned short)`
  - calls: CDialogTemplate::AlignData, CDialogTemplate::AppendData, CDialogTemplate::AppendString
  - called by (6): CDialogTemplate::AddButton, CDialogTemplate::AddComboBox, CDialogTemplate::AddEditBox, CDialogTemplate::AddListBox, CDialogTemplate::AddScrollBar, CDialogTemplate::AddStatic
- **167** `CDialogTemplate::AlignData(int)`
  - calls: CDialogTemplate::EnsureSpace
  - called by (1): CDialogTemplate::AddStandardComponent
- **178** `CDialogTemplate::AppendString(char const*)`
  - calls: CDialogTemplate::AppendData
  - called by (3): CDialogTemplate::AddComponent, CDialogTemplate::AddStandardComponent, CDialogTemplate::CDialogTemplate
- **189** `CDialogTemplate::AppendData(void*, int)`
  - calls: CDialogTemplate::EnsureSpace
  - called by (10): CDialogTemplate::AddButton, CDialogTemplate::AddComboBox, CDialogTemplate::AddComponent, CDialogTemplate::AddEditBox, CDialogTemplate::AddListBox, CDialogTemplate::AddScrollBar, CDialogTemplate::AddStandardComponent, CDialogTemplate::AddStatic, CDialogTemplate::AppendString, CDialogTemplate::CDialogTemplate
- **197** `CDialogTemplate::EnsureSpace(int)`
  - called by (2): CDialogTemplate::AlignData, CDialogTemplate::AppendData
