#include <stdio.h>
#include <stdlib.h>

struct dummy{
    int value;
}

void main(int argc, char* argv[]){

    int i = rand() % 10;
    int j;
    struct dummy* dummy = malloc(sizeof(struct dummy));

    // path 1
    if(i < 5){
        free(dummy);
        if(i > 6){
            printf("more than 6");
        }
    }
    // path 2 - memory leak
    else{ 
        dummy->value = i;
    }
    
    for(j = 0; j < i; j++){
        printf("im doing a loop!");
    }

    // if(i) free(dummy); else (printf("a")); fun test case
}