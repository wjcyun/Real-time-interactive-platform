#include "sys.h"
//////////////////////////////////////////////////////////////////////////////////	 
 
//The THUMB instruction does not support assembly

void WFI_SET(void)
{
	__ASM volatile("wfi");		  
}
void INTX_DISABLE(void)
{		  
	__ASM volatile("cpsid i");
}
//开启所有中断
void INTX_ENABLE(void)
{
	__ASM volatile("cpsie i");		  
}
//Set the top stack address
//addr:
__asm void MSR_MSP(u32 addr) 
{
    MSR MSP, r0 			//set Main Stack value
    BX r14
}
