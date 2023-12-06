#include <stdio.h>
#include <stdlib.h>

struct dummy{
    int value;
}

void main(int argc, char* argv[]){

    int i = rand() % 10;
    int j;
    struct dummy* dummy = malloc(sizeof(struct dummy));

    for(j = 0; j < i; j++){
        while(i < 100){
            if(j == 9){
                free(dummy);
            }
            if(i < j){
                free(dummy);
            }
        }
        if(j){
            printf("deez");
        }
    }

    // if(i) free(dummy); else (printf("a")); fun test case
    return;
}