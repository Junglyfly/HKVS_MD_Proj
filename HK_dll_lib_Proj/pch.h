// pch.h: 这是预编译标头文件。
// 下方列出的文件仅编译一次，提高了将来生成的生成性能。
// 这还将影响 IntelliSense 性能，包括代码完成和许多代码浏览功能。
// 但是，如果此处列出的文件中的任何一个在生成之间有更新，它们全部都将被重新编译。
// 请勿在此处添加要频繁更新的文件，这将使得性能优势无效。

#ifndef PCH_H
#define PCH_H

// 添加要在此处预编译的标头
#include "framework.h"

extern "C" _declspec(dllexport) int myAdd(int a, int b);
extern "C" _declspec(dllexport) int myMax(int a, int b);


extern "C" _declspec(dllexport) int HK_SDK_Init();
extern "C" _declspec(dllexport) int HK_USER_Login(char hk_ip[30], int hk_port, char hk_username[50], char hk_passwaord[30]);

extern "C" _declspec(dllexport) unsigned short HK_GetFileByTime(int lUserID, unsigned short start_year, unsigned short start_month, unsigned short start_day, unsigned short start_hour, unsigned short start_minunte, \
    unsigned short start_second, unsigned short stop_year, unsigned short stop_month, unsigned short stop_day, unsigned short stop_hour, unsigned short stop_minunte, \
    unsigned short stop_second, char savepath[60]);


extern "C" _declspec(dllexport) void HK_Logout(unsigned short UserID);
extern "C" _declspec(dllexport) void HK_Cleanup();




#endif //PCH_H

