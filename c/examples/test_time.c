#include <stdlib.h>
#include <signal.h>
#include <time.h>
#include "ADS1263.h"
#include "stdio.h"
#include <string.h>

#define REF         4.73
                                //external AVDD and AVSS(Default), or internal 2.5V

void  Handler(int signo)
{
    //System Exit
    printf("\r\n END \r\n");
    DEV_Module_Exit();
    exit(0);
}

int main(void)
{
    UDOUBLE ADC[10];
    UWORD i;
    double RES, TEMP;
    
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
    
    printf("ADS1263 Demo \r\n");
    DEV_Module_Init();

    // 0 is singleChannel, 1 is diffChannel
    ADS1263_SetMode(0);
    
    // The faster the rate, the worse the stability
    // and the need to choose a suitable digital filter(REG_MODE1)
    if(ADS1263_init_ADC1(ADS1263_400SPS) == 1) {
        printf("\r\n END \r\n");
        DEV_Module_Exit();
        exit(0);
    }
        
    #define ChannelNumber 5
    UBYTE ChannelList[ChannelNumber] = {0};    // The channel must be less than 10
            
    UDOUBLE Value[ChannelNumber] = {0};
    
    time_t start_time;
    start_time = time(0);
    ADS1263_GetAll(ChannelList, Value, ChannelNumber);
    printf(time(0)-start_time)
}