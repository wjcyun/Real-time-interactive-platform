# Real-time-interactive-platform
Predatory pursuit in rodents.
## Background

` Technical summary：Spyder python C# STM32 Keil`

### Overview
 **A real-time interactive platform** for studying the predatory pursuit of rodents. The software includes the main program written in Python and the hardware control written in C. The hardware consists of three parts: the arena, the control unit for the two-dimensional slides, and the webcam for data acquisition. 
 
Here, we will describe how to install and use the software and hardware modules of the platform.

### Overview of the workflow
The following figure illustrates the hardware connections of the real-time interactive platform.

<div align="center">
<p align="center">
<img src="https://i.postimg.cc/dVkxKxkk/1.png" height="400">
</div>


The following figure shows the the escape strategy for artificial prey.

<div align="center">
<p align="center">
<img src="https://i.postimg.cc/L8DwD11v/2.png" height="300">
</div>


There are three python files in the Spyder folder:
* Escape strategy.py
* Pixel-to-distance conversion.py
* Recognizing HSV.py

The hardware driver compiled by C has six main files in the Control folder (They should be downloaded together): 
* CORE
* HARDWARE
* OBJ
* STM32F10x_FWLib
* SYSTEM
* USER
## Installation
### Step 1: Install Python via Anaconda
The python program can be run in any software that can compile a python environment, here we recommend using Spyder from Anaconda. Spyder (Python ≥ 3.7) is a powerful Python IDE (Integrated Development Environment) that combines writing, running and debugging Python programs.
 It can be downloaded from: [Anaconda](https://www.anaconda.com/).
 It is worth noting that when using the program, you can install the appropriate extension packages using the following statement:
 

```
// opencv
pip install opencv-python
```
```
// numpy
pip install numpy
```
```
// serial
pip install serial
```
### Step 2: Install Keil
The C program needs to be compiled on Keil5, which you can download via [Keil](https://www.keil.com/download/).
### Step 3: Write the program to STM32 via XCOM
After successful compilation, we need to burn the compiled file (CONTROL.hex file in the OBJ folder) into the STM32 microcontroller via the serial port. Serial debugging software and information can be downloaded through [XCOM](http://47.111.11.73/docs/index.html).

## User Guides
You can download the python program and run directly in Spyder. The main function of this program is to acquire video frames from the camera and identify the mice and artificial prey, then determine the escape direction of the artificial prey and send the speed and direction information to the microcontroller.
>Escape strategy.py.

If you want to determine the conversion between distances in an image and actual distances, you can obtain the distances between pixel points using the following program.
>Pixel-to-distance conversion.py

You can also use the following program to get the HSV gamut range of the target object.
> Recognizing HSV.py


If you want to get the C program, you can open CONTROL.uvprojx in the USER folder from Keil. It can receive speed and direction information from python and decode it into an analog signal to drive servo motors.
> **USER**
>CONTROL.uvprojx

> **Other codes descriptions**
>Main function: USER\main.c
> 
>Serial communication: HARDWARE\serial\serial.c
> 
>Pid control: HARDWARE\PID\pid.c
> 
>PWM wave: HARDWARE\TIMER\timer.c

## Hardware
If you want to control the servo motor driver from STM32, you can refer to the following circuit design.

<div align="center">
<p align="center">
<img src="https://i.postimg.cc/Mp3Hs9RP/3.png" height="300">
</div>
Ports PE6 and PE7 in the STM32 give direction and velocity signal, respectively, which are passed through an amplifier circuit to ports 43 and 39 of the servo motor driver.

## Other files
>Data
>
>difficulty of 15cms
>
>difficulty of 22.5cms
>
>difficulty of 30cms
>
>Hardware-configuration
>

