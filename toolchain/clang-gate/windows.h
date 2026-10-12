#pragma once
/* Minimal Win32 surface for host-side syntax checking of the BTS DLL. */
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <wchar.h>
#include <ctype.h>
#include <limits.h>
typedef unsigned long DWORD; typedef int BOOL; typedef unsigned char BYTE; typedef unsigned short WORD;
typedef void* HANDLE; typedef void* HMODULE; typedef void* HINSTANCE; typedef void* HWND; typedef void* LPVOID;
typedef const char* LPCSTR; typedef char* LPSTR; typedef const wchar_t* LPCWSTR; typedef wchar_t* LPWSTR;
typedef long LONG; typedef unsigned int UINT; typedef long LRESULT; typedef unsigned int WPARAM; typedef long LPARAM;
typedef char TCHAR; typedef long long __int64_t_shim; typedef unsigned long ULONG; typedef float FLOAT;
typedef DWORD* LPDWORD; typedef void VOID; typedef const void* LPCVOID; typedef int INT;
#define WINAPI
#define APIENTRY
#define CALLBACK
#define TRUE 1
#define FALSE 0
#define MAX_PATH 260
#define DLL_PROCESS_ATTACH 1
#define DLL_THREAD_ATTACH 2
#define DLL_THREAD_DETACH 3
#define DLL_PROCESS_DETACH 0
#define MB_OK 0
#define MB_ICONEXCLAMATION 0
#define MB_YESNO 0
#define MB_ICONQUESTION 0
#define IDYES 6
#define IDNO 7
#define _MAX_PATH 260
#define _TRUNCATE ((size_t)-1)
inline DWORD GetTickCount() { return 0; }
inline DWORD timeGetTime() { return 0; }
inline void OutputDebugString(const char*) {}
inline void OutputDebugStringA(const char*) {}
inline int MessageBox(HWND, const char*, const char*, UINT) { return 0; }
inline int MessageBoxA(HWND, const char*, const char*, UINT) { return 0; }
inline BOOL DisableThreadLibraryCalls(HMODULE) { return TRUE; }
inline DWORD GetModuleFileName(HMODULE, char*, DWORD) { return 0; }
inline DWORD GetModuleFileNameA(HMODULE, char*, DWORD) { return 0; }
inline HMODULE GetModuleHandle(const char*) { return 0; }
inline void Sleep(DWORD) {}
inline long InterlockedIncrement(long volatile* p) { return ++*p; }
inline long InterlockedDecrement(long volatile* p) { return --*p; }
inline BOOL QueryPerformanceCounter(void*) { return TRUE; }
inline BOOL QueryPerformanceFrequency(void*) { return TRUE; }
typedef union { struct { DWORD LowPart; LONG HighPart; } u; long long QuadPart; } LARGE_INTEGER;
inline int _vsnprintf(char* b, size_t n, const char* f, va_list a) { return vsnprintf(b, n, f, a); }
inline int _snprintf(char* b, size_t n, const char* f, ...) { va_list a; va_start(a, f); int r = vsnprintf(b, n, f, a); va_end(a); return r; }
inline int _vsnwprintf(wchar_t* b, size_t n, const wchar_t* f, va_list a) { return vswprintf(b, n, f, a); }
inline int _snwprintf(wchar_t* b, size_t n, const wchar_t* f, ...) { va_list a; va_start(a, f); int r = vswprintf(b, n, f, a); va_end(a); return r; }
inline int _stricmp(const char* a, const char* b) { return strcasecmp(a, b); }
inline int stricmp(const char* a, const char* b) { return strcasecmp(a, b); }
inline int _strnicmp(const char* a, const char* b, size_t n) { return strncasecmp(a, b, n); }
inline int strnicmp(const char* a, const char* b, size_t n) { return strncasecmp(a, b, n); }
inline int _wcsicmp(const wchar_t* a, const wchar_t* b) { return wcscasecmp(a, b); }
inline int wcsicmp(const wchar_t* a, const wchar_t* b) { return wcscasecmp(a, b); }
inline char* _itoa(int v, char* s, int) { sprintf(s, "%d", v); return s; }
inline char* itoa(int v, char* s, int) { sprintf(s, "%d", v); return s; }
inline wchar_t* _itow(int v, wchar_t* s, int) { swprintf(s, 16, L"%d", v); return s; }
inline char* _strlwr(char* s) { for (char* p = s; *p; ++p) *p = (char)tolower(*p); return s; }
inline char* _strupr(char* s) { for (char* p = s; *p; ++p) *p = (char)toupper(*p); return s; }
inline char* strlwr(char* s) { return _strlwr(s); }
inline char* strupr(char* s) { return _strupr(s); }
inline wchar_t* _wcslwr(wchar_t* s) { return s; }
inline wchar_t* _wcsupr(wchar_t* s) { return s; }
inline int MultiByteToWideChar(UINT, DWORD, const char*, int, wchar_t*, int) { return 0; }
inline int WideCharToMultiByte(UINT, DWORD, const wchar_t*, int, char*, int, const char*, BOOL*) { return 0; }
#define CP_ACP 0
#define CP_UTF8 65001
#define __forceinline inline
#define __cdecl
#define __stdcall
#define _cdecl
#define __declspec(x)
#define _int64 long long
#define __int64 long long
#define _alloca alloca
#include <alloca.h>
#define _isnan isnan
#define _finite isfinite
#define _countof(a) (sizeof(a)/sizeof((a)[0]))
typedef const char* LPCTSTR; typedef char* LPTSTR;
typedef struct tagPOINT { LONG x; LONG y; } POINT;
typedef struct tagRECT { LONG left, top, right, bottom; } RECT;
inline int swprintf(wchar_t* b, const wchar_t* f, ...) { va_list a; va_start(a, f); int r = vswprintf(b, 4096, f, a); va_end(a); return r; }
inline int vswprintf(wchar_t* b, const wchar_t* f, va_list a) { return vswprintf(b, 4096, f, a); }
typedef wchar_t WCHAR;
#include <float.h>
#include <math.h>
inline double _wtof(const wchar_t* s) { return wcstod(s, 0); }
inline int _vsnprintf(char* b, size_t n, const char* f, char* a);
#define INVALID_HANDLE_VALUE ((HANDLE)(long)-1)
#define FILE_ATTRIBUTE_DIRECTORY 0x10
#define ERROR_NO_MORE_FILES 18
typedef struct { DWORD dwFileAttributes; char cFileName[MAX_PATH]; } WIN32_FIND_DATA;
inline HANDLE FindFirstFile(const char*, WIN32_FIND_DATA*) { return 0; }
inline BOOL FindNextFile(HANDLE, WIN32_FIND_DATA*) { return 0; }
inline BOOL FindClose(HANDLE) { return 0; }
inline DWORD GetLastError() { return 0; }
typedef struct { DWORD style; DWORD dwExtendedStyle; WORD cdit; short x, y, cx, cy; } DLGTEMPLATE;
typedef struct { DWORD style; DWORD dwExtendedStyle; short x, y, cx, cy; WORD id; } DLGITEMTEMPLATE;
inline UINT timeBeginPeriod(UINT) { return 0; }
inline UINT timeEndPeriod(UINT) { return 0; }
#define _tcscmp strcmp
#define _tcsicmp _stricmp
inline char* _strdup(const char* s) { return strdup(s); }
extern char* _pgmptr;
