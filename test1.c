#include <stdio.h>
#include <stdlib.h>

struct dummy{
    int value;
}

void main(int argc, char* argv[]){

    int i = rand() % 10;

    struct dummy* dummy = malloc(sizeof(struct dummy));

    // path 1
    if(i < 5){
        free(dummy);
        if(i > 6){
            printf("more than 6");
        }
    }
    // path 2 - memory leak
    // else{ 
    //     dummy->value = i;
    // }

    // if(i) free(dummy); else (printf("a")); fun test case
}