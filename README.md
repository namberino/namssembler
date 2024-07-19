# namssembler: A simple assembler for the 8085 ISA

This is a simple Intel 8085 ISA assembler written in python. 

Usage: `python asm85.py <filename>.asm`

This assembler will read the assembly file (found in the [asm](asm) directory) from the command-line argument and translate it into byte-level representation in the [out](out) directory.

This was made for my [nam85 computer](https://github.com/namberino/nam85)

References: 
- [Opcodes table of Intel 8085](http://www.eazynotes.com/notes/microprocessor/notes/opcodes-table-of-intel-8085.pdf)
- [Instruction set of 8085 by Government Polytechnic, Barkot Uttarkashi](https://gpbarkot.org.in/download/file/ihoN4LlRHP.pdf)
- [Intel 8085 instruction set table](https://pastraiser.com/cpu/i8085/i8085_opcodes.html)
