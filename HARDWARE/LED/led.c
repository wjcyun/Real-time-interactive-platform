#include "led.h"

//Initialize PB.5 and PE.5 as outputs and enable the two clocks---	Status light    
// Initialize PE.6 and PE.1 as outputs and enable the two clocks---	Directional signal outlet
void LED_Init(void)
{
 
 GPIO_InitTypeDef  GPIO_InitStructure;
 	
 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB|RCC_APB2Periph_GPIOE, ENABLE);	 //The clock of PB and PE ports is enabled
	
 GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5;				 //LED0-PB5 Indicates the configuration of a port
 GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //Push-pull output
 GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 //The I/O port speed is 50Mhz
 GPIO_Init(GPIOB, &GPIO_InitStructure);					 //Example Initialize GPIOPB.5
 GPIO_SetBits(GPIOB,GPIO_Pin_5);						 //PB.5 High output

 GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5;	    		 //LED1-PE5 Indicates the configuration of a port
 GPIO_Init(GPIOE, &GPIO_InitStructure);	  				 //The I/O port speed is 50Mhz
 GPIO_SetBits(GPIOE,GPIO_Pin_5); 						 //PB.5 High output
 
		
 GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6;				 	 
 GPIO_Init(GPIOE, &GPIO_InitStructure);					 
 GPIO_SetBits(GPIOE,GPIO_Pin_6);						 

 GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;	    		 
 GPIO_Init(GPIOE, &GPIO_InitStructure);	  				
 GPIO_SetBits(GPIOE,GPIO_Pin_1); 			
	
}
 
