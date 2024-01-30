#ifndef __LED_H
#define __LED_H	 
#include "sys.h"

#define LED0 PBout(5)// PB5
#define LED1 PEout(5)// PE5	

#define PWM0 PEout(6)
#define PWM1 PEout(1)

void LED_Init(void);//initialize

		 				    
#endif
