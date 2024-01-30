#include "timer.h"
#include "led.h"
#include "usart.h" 
   	  
//Universal timer 3 interrupts initialization

//arr£ºAutomatic loading value
//psc£Clock predivision frequency

void TIM3_Int_Init(u16 arr,u16 psc)
{
  TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	NVIC_InitTypeDef NVIC_InitStructure;

	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE); //Clock enable

	TIM_TimeBaseStructure.TIM_Period = arr; //Sets the value of the auto-reload register cycle for the next update event load activity, counting to 5000 for 500ms
	TIM_TimeBaseStructure.TIM_Prescaler =psc; //Set the pre-division value used as the TIMX clock frequency divisor, the 10Khz count frequency 
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1; //Set clock split
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  //TIM upward count mode
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure); //Initializes the time base unit of TIMX
 
	TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE ); //Enables the specified TIM3 interrupt to allow the update interrupt

	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;  //TIM3 interrupt
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;  //Priority 0 level 4
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;  //From priority level 3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; 
	NVIC_Init(&NVIC_InitStructure);  //Initializes the peripheral NVIC register

	TIM_Cmd(TIM3, ENABLE);  //The TIMX peripheral was enabled
							 
}
//Timer 3 interrupt service program
void TIM3_IRQHandler(void)   
{
	if (TIM_GetITStatus(TIM3, TIM_IT_Update) != RESET) //Checks whether the specified TIM interrupt occurred
		{
		TIM_ClearITPendingBit(TIM3, TIM_IT_Update  );  //Clears the interrupt pending bits of TIMX 
		LED1=!LED1;
		}
}


//TIM3 PWM part is initialized
//PWM output initialization
//arr£ºAutomatic loading value
//psc£ºlock predivision frequency
void TIM3_PWM_Init(u16 arr,u16 psc)
{  
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_OCInitTypeDef  TIM_OCInitStructure;

	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);	//The timer 3 clock was enabled
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA  | RCC_APB2Periph_AFIO, ENABLE);  //The clock of the GPIO peripheral and AFIO multiplexing module was enabled
	 
   //Set this pin to the multiplexed output function to output PWM pulse waveform of TIM3 CH1 (GPIOA.7)
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7; 
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  //Reuse push-pull output
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);//Initialize the GPIO
 
   //Initialize TIM3
	TIM_TimeBaseStructure.TIM_Period = arr; 
	TIM_TimeBaseStructure.TIM_Prescaler =psc; 
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1; //Set clock split:TDTS = Tck_tim
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure); 
	
	 
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2; //Select Timer mode, TIM pulse width modulation mode 2
 	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; //Compare output enable
	TIM_OCInitStructure. TIM_Pulse=(arr+1)/2-1;
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High; 

	TIM_OC2Init(TIM3, &TIM_OCInitStructure);  
	TIM_OC2PreloadConfig(TIM3, TIM_OCPreload_Enable);  
  
	TIM_ARRPreloadConfig(TIM3,ENABLE);
	TIM_Cmd(TIM3, ENABLE);  //enable TIM3
	
}
// Enable clock 4 and enable GPIOD.12 as the PEM wave output
void TIM4_PWM_Init(u16 arr,u16 psc)
{
	GPIO_InitTypeDef  GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_OCInitTypeDef TIM_OCInitTypeSture;
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4, ENABLE);
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD | RCC_APB2Periph_AFIO, ENABLE);  
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; 		 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 
  GPIO_Init(GPIOD, &GPIO_InitStructure);					 
	
	GPIO_PinRemapConfig(GPIO_Remap_TIM4,ENABLE);
	
	TIM_TimeBaseStructure.TIM_Period = arr; 
	TIM_TimeBaseStructure.TIM_Prescaler =psc; 
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1; 
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up; 
	TIM_TimeBaseInit(TIM4, &TIM_TimeBaseStructure); 
	
		
	TIM_OCInitTypeSture.TIM_OCMode=TIM_OCMode_PWM2;
	TIM_OCInitTypeSture.TIM_OCPolarity=TIM_OCPolarity_High;
	TIM_OCInitTypeSture.TIM_OutputState=TIM_OutputState_Enable;
	TIM_OCInitTypeSture.TIM_Pulse=(arr+1)/2-1;
	TIM_OC1Init(TIM4,&TIM_OCInitTypeSture);
	TIM_OC1PreloadConfig(TIM4,TIM_OCPreload_Enable);
	
	TIM_ARRPreloadConfig(TIM4,ENABLE);
	
	TIM_Cmd(TIM4,ENABLE);
	
}
