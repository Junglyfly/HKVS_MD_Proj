#include <stdio.h>
#include <iostream>
#include "Windows.h"
#include "HCNetSDK.h"
using namespace std;


void main() {

    //---------------------------------------
    // 初始化
    NET_DVR_Init();
    //设置连接时间与重连时间
    NET_DVR_SetConnectTime(2000, 1);
    NET_DVR_SetReconnect(10000, true);

    //---------------------------------------
    // 注册设备
    LONG lUserID;

    //登录参数，包括设备地址、登录用户、密码等
    NET_DVR_USER_LOGIN_INFO struLoginInfo = { 0 };
    struLoginInfo.bUseAsynLogin = 0; //同步登录方式
    strcpy(struLoginInfo.sDeviceAddress, "192.168.1.64"); //设备IP地址
    struLoginInfo.wPort = 8000; //设备服务端口
    strcpy(struLoginInfo.sUserName, "admin"); //设备登录用户名
    strcpy(struLoginInfo.sPassword, "a12345678"); //设备登录密码

    //设备信息, 输出参数
    NET_DVR_DEVICEINFO_V40 struDeviceInfoV40 = { 0 };

    lUserID = NET_DVR_Login_V40(&struLoginInfo, &struDeviceInfoV40);
    if (lUserID < 0)
    {
        printf("Login failed, error code: %d\n", NET_DVR_GetLastError());
        NET_DVR_Cleanup();
        return;
    }

    NET_DVR_PLAYCOND struDownloadCond = { 0 };
    struDownloadCond.dwChannel = 1;

    struDownloadCond.struStartTime.dwYear = 2021;
    struDownloadCond.struStartTime.dwMonth = 1;
    struDownloadCond.struStartTime.dwDay = 24;
    struDownloadCond.struStartTime.dwHour = 8;
    struDownloadCond.struStartTime.dwMinute = 30;
    struDownloadCond.struStartTime.dwSecond = 0;
    struDownloadCond.struStopTime.dwYear = 2021;
    struDownloadCond.struStopTime.dwMonth = 1;
    struDownloadCond.struStopTime.dwDay = 24;
    struDownloadCond.struStopTime.dwHour = 8;
    struDownloadCond.struStopTime.dwMinute = 32;
    struDownloadCond.struStopTime.dwSecond = 0;

    //---------------------------------------
    //按时间下载
    int hPlayback;
    char savepath[40] = "./test.mp4";
    hPlayback = NET_DVR_GetFileByTime_V40(lUserID, savepath, &struDownloadCond);
    if (hPlayback < 0)
    {
        printf("NET_DVR_GetFileByTime_V40 fail,last error %d\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return;
    }

    //---------------------------------------
    //开始下载
    if (!NET_DVR_PlayBackControl_V40(hPlayback, NET_DVR_PLAYSTART, NULL, 0, NULL, NULL))
    {
        printf("Play back control failed [%d]\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return;
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
        return;
    }
    if (nPos < 0 || nPos>100)
    {
        printf("download err [%d]\n", NET_DVR_GetLastError());
        NET_DVR_Logout(lUserID);
        NET_DVR_Cleanup();
        return;
    }
    printf("Be downloading... %d %%\n", nPos);

    //注销用户
    NET_DVR_Logout(lUserID);
    //释放SDK资源
    NET_DVR_Cleanup();
    return;
}



