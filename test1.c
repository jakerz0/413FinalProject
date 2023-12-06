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
        else{
            printf("less than 6");
        }
    }
    else if(i > 10){
        printf("do funny stuff");
        printf("do funny stuff again");
        printf("do funny stuff one more time");
    }
    // path 2 - memory leak
    else{ 
        dummy->value = i;
    }

    for(j = 0; j < i; j++){
        printf("im doing a loop!");
        if(j == 2) {
            printf("Checking this enter");
            // literally nothing
        }
    }

    // if(i) free(dummy); else (printf("a")); fun test case
    return;
}