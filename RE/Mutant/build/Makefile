ALL: main clean
	
main: encrypt		
	gcc -c main.c -o main.o		
	gcc -o main encrypt.o main.o		
	strip main		
encrypt:		
	nasm -f elf64 -o encrypt.o encrypt.asm		
clean:
	rm *.o
	mv main ../mutant
 	
