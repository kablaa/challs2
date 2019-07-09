#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
#define MESSAGE_SIZE 61

extern int encrypt(char *message);



char *correctBytes = "\xb5\x10\x18\x96\x2d\xb\xcc\x42\x34\x8c\x2a\x1a\xc1\xb1\x24\x1f\x96\x27\xb\xb5\x4c\x2c\x8f\x24\x2a\xd3\xb8\x2a\x13\x4d\x2f\x18\xb4\x4a\x3a\x94\x7b\x2a\xc8\xb0\x10\xd\x5d\x1c\xb\xa1\x42\x1e\x86\x24\xd\xbe\xab\x20\x4\x90\x79\x10\xb8\x7e\x3c";

int main(int argc, const char *argv[])
{
    
    int i;
    int wrong = 0;
    char * buf = malloc(MESSAGE_SIZE+1);
    memset(buf,0,MESSAGE_SIZE+1);
    memcpy(buf,argv[1],MESSAGE_SIZE+1);
    encrypt(buf);
    /* printf("%s",buf); */
    for(i = 1; i < MESSAGE_SIZE+1; i++){
        wrong += buf[i] ^ correctBytes[i-1];
        /* printf("%d: %x ^ %x = %x\n", i, buf[i],correctBytes[i-1],wrong); */
    }
    if(!wrong){
        puts("WIN");
    }
    return 0;
}


