#include "sys.h"
#include "usart.h"
#include "delay.h"
#include "led.h"
#include "serial.h"
#include "stdlib.h"

u16 flag;
u16 t;  
u16 len;
u16 times=0; 

extern int coords[4];

void recieveData(void)
{
	char strX[4], strY[4],strP[4],strQ[4];
	u8 cnt_x=0;
	u8 cnt_y=0;
	u8 cnt_p=0;
	u8 cnt_q=0;
	u8 *adress = NULL;
	
	if(USART_RX_STA&0x8000)		//If the data is accepted
		{	
			LED1=!LED1;//Indicator No. 1 changes status
			
			len=USART_RX_STA&0x3fff;//Get the length of the received data
			
			adress = &USART_RX_BUF[0];	//The pointer adress stores character addresses and traverses them from 0-len
			
			//Retrieves the character form of coordinates to strx and stry according to the protocol
			for(t=0;t<len;t++)
			{

				if(*adress>='0' && *adress<='9')
				{
					if(flag==1)
					{
						strX[cnt_x] = *adress;
						cnt_x++;
					}
					else if(flag==2)
					{
						strY[cnt_y] = *adress;
						cnt_y++;
					}	
					else if(flag==3)
					{
						strP[cnt_p] = *adress;
						cnt_p++;
					}	
					else
					{
						strQ[cnt_q] = *adress;
						cnt_q++;
					}	
				}
				else
				{
					if(*adress=='A')
						flag = 1;
					if(*adress=='B')
						flag = 2;
					if(*adress=='C')
						flag = 3;
					if(*adress=='D')
						flag = 4;
				}
				adress++;	
			}
			
			//Converts the string to an integer and stores it in the global variable coords.
			coords[0] = atoi(strX);
			coords[1] = atoi(strY);
			coords[2] = atoi(strP);
			coords[3] = atoi(strQ);
			//Flag bit clear 0
			USART_RX_STA=0;
		}
	else
		{
			times++;
			if(times%30==0)LED0=!LED0;//Indicator 0 blinks, indicating that the system is running
			delay_ms(10); 
		}
}
