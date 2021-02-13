// pch.cpp: 与预编译标头对应的源文件
#include "pch.h"
#include<iostream>
using namespace std;
int myAdd(int a, int b)
{
	return a + b;
}
int myMax(int a, int b)
{
	return a > b ? a : b;
}


#include "Windows.h"
#include "HCNetSDK.h"


// sdk初始化
int HK_SDK_Init()
{
    //---------------------------------------
    int status = 0;
// 初始化
    status = NET_DVR_Init();
    //设置连接时间与重连时间
    NET_DVR_SetConnectTime(2000, 1);
    NET_DVR_SetReconnect(10000, true);

    return status;
}

 // 用户登录       返回用户id
int HK_USER_Login(char hk_ip[30],int hk_port,char hk_username[50],char hk_passwaord[30])
{
    //---------------------------------------
// 注册设备
    LONG lUserID;

    //登录参数，包括设备地址、登录用户、密码等
    NET_DVR_USER_LOGIN_INFO struLoginInfo = { 0 };
    struLoginInfo.bUseAsynLogin = 0; //同步登录方式
    strcpy_s(struLoginInfo.sDeviceAddress, hk_ip); //设备IP地址
    struLoginInfo.wPort = hk_port; //设备服务端口
    strcpy_s(struLoginInfo.sUserName, hk_username); //设备登录用户名
    strcpy_s(struLoginInfo.sPassword, hk_passwaord); //设备登录密码

    //设备信息, 输出参数
    NET_DVR_DEVICEINFO_V40 struDeviceInfoV40 = { 0 };

    lUserID = NET_DVR_Login_V40(&struLoginInfo, &struDeviceInfoV40);
    if (lUserID < 0)
    {
        printf("Login failed, error code: %d\n", NET_DVR_GetLastError());
        NET_DVR_Cleanup();
        return -1;
    }

    return  lUserID;
}



// 按时间下载视频文件        成功返回 1 失败返回 -1
unsigned short  HK_GetFileByTime(int lUserID,unsigned short start_year, unsigned short start_month, unsigned short start_day, unsigned short start_hour, unsigned short start_minunte, \
    unsigned short start_second, unsigned short stop_year, unsigned short stop_month, unsigned short stop_day, unsigned short stop_hour, unsigned short stop_minunte, \
    unsigned short stop_second,char savepath[60])
{

    NET_DVR_PLAYCOND struDownloadCond = { 0 };
    struDownloadCond.dwChannel = 1;

    struDownloadCond.struStartTime.dwYear = start_year;
    struDownloadCond.struStartTime.dwMonth = start_month;
    struDownloadCond.struStartTime.dwDay = start_day;
    struDownloadCond.struStartTime.dwHour = start_hour;
    struDownloadCond.struStartTime.dwMinute = start_minunte;
    struDownloadCond.struStartTime.dwSecond = start_second;
    struDownloadCond.struStopTime.dwYear = stop_year;
    struDownloadCond.struStopTime.dwMonth = stop_month;
    struDownloadCond.struStopTime.dwDay = stop_day;
    struDownloadCond.struStopTime.dwHour = stop_hour;
    struDownloadCond.struStopTime.dwMinute = stop_minunte;
    struDownloadCond.struStopTime.dwSecond = stop_second;

    //---------------------------------------
    //按时间下载
    int hPlayback;
    hPlayback = NET_DVR_GetFileByTime_V40(lUserID, savepath, &struDownloadCond);
    if (hPlayback < 0)
    {
        printf("NET_DVR_GetFileByTime_V40 fail,last error %d\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return -1 ;
    }

    //---------------------------------------
    //开始下载
    if (!NET_DVR_PlayBackControl_V40(hPlayback, NET_DVR_PLAYSTART, NULL, 0, NULL, NULL))
    {
        printf("Play back control failed [%d]\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return -1 ;
    }

    int nPos = 0;
    for (nPos = 0; nPos < 100 && nPos >= 0; nPos = NET_DVR_GetDownloadPos(hPlayback))
    {
        printf("Be downloading... %d %%\n", nPos);
        Sleep(5000);  //millisecond
    }
    if (!NET_DVR_StopGetFile(hPlayback))
    {
        printf("failed to stop get file [%d]\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return -1 ;
    }
    if (nPos < 0 || nPos>100)
    {
        printf("download err [%d]\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return -1;
    }
    printf("Be downloading... %d %%\n", nPos);

    return 1;
}



void HK_Logout(unsigned short UserID)
{
    //注销用户
    NET_DVR_Logout(UserID);
}

void HK_Cleanup()
{
    //释放SDK资源
    NET_DVR_Cleanup();
}


