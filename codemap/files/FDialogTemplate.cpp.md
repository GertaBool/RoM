# FDialogTemplate.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **10** `CDialogTemplate::CDialogTemplate(LPCSTR, DWORD, int, int, int, int, LPCSTR, WORD)`
  - calls: CDialogTemplate::AppendString, CDialogTemplate::AppendData
- **47** `CDialogTemplate::~CDialogTemplate()`
- **52** `CDialogTemplate::AddComponent(LPCSTR, LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AppendData, CDialogTemplate::AppendString
- **78** `CDialogTemplate::AddButton(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **87** `CDialogTemplate::AddEditBox(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **96** `CDialogTemplate::AddStatic(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **105** `CDialogTemplate::AddListBox(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **114** `CDialogTemplate::AddScrollBar(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **123** `CDialogTemplate::AddComboBox(LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AddStandardComponent, CDialogTemplate::AppendData
- **132** `CDialogTemplate::GetDialogTemplate()`
- **137** `CDialogTemplate::AddStandardComponent(WORD, LPCSTR, DWORD, DWORD, int, int, int, int, WORD)`
  - calls: CDialogTemplate::AlignData, CDialogTemplate::AppendData, CDialogTemplate::AppendString
  - called by (6): CDialogTemplate::AddButton, CDialogTemplate::AddComboBox, CDialogTemplate::AddEditBox, CDialogTemplate::AddListBox, CDialogTemplate::AddScrollBar, CDialogTemplate::AddStatic
- **166** `CDialogTemplate::AlignData(int)`
  - calls: CDialogTemplate::EnsureSpace
  - called by (1): CDialogTemplate::AddStandardComponent
- **177** `CDialogTemplate::AppendString(LPCSTR)`
  - calls: CDialogTemplate::AppendData
  - called by (3): CDialogTemplate::AddComponent, CDialogTemplate::AddStandardComponent, CDialogTemplate::CDialogTemplate(LPCSTR, DWORD, int, int, int, int, LPCSTR, WORD)
- **188** `CDialogTemplate::AppendData(void *, int)`
  - calls: CDialogTemplate::EnsureSpace
  - called by (10): CDialogTemplate::AddButton, CDialogTemplate::AddComboBox, CDialogTemplate::AddComponent, CDialogTemplate::AddEditBox, CDialogTemplate::AddListBox, CDialogTemplate::AddScrollBar, CDialogTemplate::AddStandardComponent, CDialogTemplate::AddStatic, CDialogTemplate::AppendString, CDialogTemplate::CDialogTemplate(LPCSTR, DWORD, int, int, int, int, LPCSTR, WORD)
- **196** `CDialogTemplate::EnsureSpace(int)`
  - called by (2): CDialogTemplate::AlignData, CDialogTemplate::AppendData
