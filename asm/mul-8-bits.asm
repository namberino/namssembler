;8085 Program to multiply 2 8-bit numbers

MVI C, 0000H  ;Store 00 in C 

LDA 5000H    ;1st value, Load A from memory location 5000
MOV B, A     ;copy content of A to B
DCR B        ;Decrement B
ORA A        ;Check is value in A (or B) is 0 or not
JNZ END      ;if Zero, jump to exit

LDA 5001H    ;2nd value, Load A from memory location 5001
MOV D, A     ;copy content of A to D
ORA A        ;Check if value of A (or D) is 0 or not

LOOP: 
JZ END      ;if Zero, jump to exit
ADD D        ;Add D to A
JNC NOCARRY  ;if carry is not generated, jump to label NOCARRY
INR C        ;if carry is generated, increment C

NOCARRY: 
DCR B        ;decrement B
JMP LOOP     ;Jump to label LOOP

END: 
STA 5003H    ;store content of A (lower order of result) at memory location 5003
MOV A, C     ;copy content of C to A
STA 5002H    ;store content of A(higher order of resut) at memory location 5002
HLT          ;Halt program
