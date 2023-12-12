#include <stdio.h>
#include <stdlib.h>

// test case with no mem leaks
int main() {
    int *array;
    int n, i;


    printf("Enter the number of elements: ");
    scanf("%d", &n);

    array = (int*) malloc(n * sizeof(int));
    if (array == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    for (i = 0; i < n; i++) {
        array[i] = i;
    }

    printf("Array elements: ");
    for (i = 0; i < n; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");

    free(array);

    return 0;
}