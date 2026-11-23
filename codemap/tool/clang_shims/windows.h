#pragma once
#include_next <windows.h>
#include <cstring>

#ifndef ZeroMemory
#define ZeroMemory(Destination, Length) memset((Destination), 0, (Length))
#endif
#ifndef VK_LSHIFT
#define VK_LSHIFT 0xA0
#endif
#ifndef VK_RSHIFT
#define VK_RSHIFT 0xA1
#endif
#ifndef DS_SETFONT
#define DS_SETFONT 0x40L
#endif
typedef UINT MMRESULT;
typedef unsigned long long DWORDLONG;
typedef struct _MEMORYSTATUSEX {
    DWORD dwLength;
    DWORD dwMemoryLoad;
    DWORDLONG ullTotalPhys;
    DWORDLONG ullAvailPhys;
    DWORDLONG ullTotalPageFile;
    DWORDLONG ullAvailPageFile;
    DWORDLONG ullTotalVirtual;
    DWORDLONG ullAvailVirtual;
    DWORDLONG ullAvailExtendedVirtual;
} MEMORYSTATUSEX, *LPMEMORYSTATUSEX;
inline BOOL GlobalMemoryStatusEx(LPMEMORYSTATUSEX) { return TRUE; }
inline DWORD GetCurrentDirectory(DWORD, LPSTR) { return 0; }
inline DWORD GetCurrentDirectoryA(DWORD, LPSTR) { return 0; }
inline short GetKeyState(int) { return 0; }
inline short GetAsyncKeyState(int) { return 0; }
