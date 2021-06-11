# RealMode-x86-asm-QEMU-Debugger-frontend
A debugger frontend for assembly x86 code runing in Real Mode (tested inside QEMU) (based on gdb).

## How to use
1. (install dependencies) --> run "pip install -r requirements.txt" inside the 'Debugger files' folder
2. (run QEMU emulation)   --> run "make" inside the 'QEMU files' folder
3. (run the debugger)     --> run "python3 main.py" inside the 'Debugger files' folder
4. press ENTER or click the 'Step' button at the bottom of the screen to step to the next instruction.
   or write gdb commands in the input area, click to send it to gdb and get the output on the rightmost bottom window
6. have fun :)

![output](https://user-images.githubusercontent.com/43099047/121617839-2571de00-ca3c-11eb-9dc9-2770249d78ef.gif)

