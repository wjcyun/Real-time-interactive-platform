#include "sys.h"
#include "usart.h"
#include "delay.h"
#include "led.h"
#include "serial.h"
#include "stdlib.h"

u16 flag;
u16 t;  
u16 len;
u16 times=0; //����Ҫ

extern int coords[4];

void recieveData(void)
{
	char strX[4], strY[4],strP[4],strQ[4];
	u8 cnt_x=0;
	u8 cnt_y=0;
	u8 cnt_p=0;
	u8 cnt_q=0;
	u8 *adress = NULL;
	
	if(USART_RX_STA&0x8000)		//�������������
		{	
			LED1=!LED1;//1��ָʾ�Ʊ��״̬
			
			len=USART_RX_STA&0x3fff;//�õ��˴ν��յ������ݳ���
			
			adress = &USART_RX_BUF[0];	//ָ��adress�����ַ���ַ����0-len��һ��
			
			//����Э��ȡ��������ַ���ʽ����strX��strY��
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
			
			//ת���ַ���Ϊ���ͣ����洢��ȫ�ֱ���coords��
			coords[0] = atoi(strX);
			coords[1] = atoi(strY);
			coords[2] = atoi(strP);
			coords[3] = atoi(strQ);
			//��־λ����
			USART_RX_STA=0;
		}
	else
		{
			times++;
			if(times%30==0)LED0=!LED0;//��˸0��ָʾ��,��ʾϵͳ��������.
			delay_ms(10); 
		}
}
