#include <stdio.h>
#include <stdlib.h>

int zzz = 100;

int add (int a, int b) {
    static int count = 0;
    int result = a + b;
    count++;
    return result;
}

int main() {
    int a = 1;
    short int b = 2;
    long int c = 3;
    register int d = 4;
    int intv[] = {5, 6, 7};

    char str1[] = "abc";
    char *str2;
    str2 = (char *)malloc(sizeof(char) * 32);
    sprintf(str2, "%s", "def");
    
    // breakpoint line
    c = add(a, b);
    return 0;
}