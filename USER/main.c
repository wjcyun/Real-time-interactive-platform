#include "stm32f10x.h"
#include "led.h"
#include "delay.h"
#include "key.h"
#include "sys.h"
#include "usart.h"
#include "serial.h"
#include "timer.h"
#include "pid.h"

//Defining Global Variables
PID_TypeDef PID_x, PID_y;//Two PID structures

int coords[4];//Array storing direction and speed information

int main(void)
{
	u16 pwmval_x, pwmval_y;//Variables controlling duty cycle

	delay_init();	    	   
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); //Set NVIC interrupt group 2, 2-bit preemption priority, 2-bit response priority
	uart_init(115200);	 //Serial port initialized to 115200
 	LED_Init();			     //Direction Port Initialization
	KEY_Init();          //Initialize the hardware interface to the keys

	//Speed and direction initialization
	coords[0] = 0;
	coords[1] = 0;
	coords[2] = 0;
	coords[3] = 0;
	//PWM0 = 1;
	//PWM1 = 1;
	
 	while(1)
	{

		recieveData();

		pwmval_x = coords[0];
		pwmval_y = coords[2];
		printf("aaa%d\r\n",coords[0]);
		printf("bbb%d\r\n",coords[1]);
		printf("ccc%d\r\n",coords[2]);
		printf("ddd%d\r\n",coords[3]);
		PWM0 =coords[1] ; 
		PWM1 =coords[3] ; 


		TIM3_PWM_Init(pwmval_x*10-1,0);
		TIM_SetCompare2(TIM3,(pwmval_x*10)/2);
		
		TIM4_PWM_Init(pwmval_y*10-1,0);
		TIM_SetCompare1(TIM4,(pwmval_y*10)/2);
		
	}	 
}
