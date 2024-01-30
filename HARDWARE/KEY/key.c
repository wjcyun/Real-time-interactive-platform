#include "stm32f10x.h"
#include "key.h"
#include "sys.h" 
#include "delay.h"
								    
//Security Check Initial Function
void KEY_Init(void) //IO initialization
{ 
 	GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOE,ENABLE);//Enable PORTA ,PORTE Clock

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_4|GPIO_Pin_3;//KEY0-KEY1
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //Set as pull-up input
 	GPIO_Init(GPIOE, &GPIO_InitStructure);//Initialize GPIO3,4


	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPD; //POA set to input, default drop down	  
	GPIO_Init(GPIOA, &GPIO_InitStructure);//Initialize GPIOA

}
//Key Handling Functions
//Returns the key value

u8 KEY_Scan(u8 mode)
{	 
	static u8 key_up=1;//Key Release Symbol
	if(mode)key_up=1;  //	  
	if(key_up&&(KEY0==0||KEY1==0||WK_UP==1))
	{
		delay_ms(10);
		key_up=0;
		if(KEY0==0)return KEY0_PRES;
		else if(KEY1==0)return KEY1_PRES;
		else if(WK_UP==1)return WKUP_PRES;
	}else if(KEY0==1&&KEY1==1&&WK_UP==0)key_up=1; 	    
 	return 0;
}
