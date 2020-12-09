#include <stdio.h>
#include <stdlib.h>

int zzz = 100;

int add2 (int a, int b) {
    int result = a + b;
    return result;
}

int add (int a, int b) {
    int result = a + b;
    return result;
}


int main(int argc, const char * argv[]) {
    char hoge[10] = "hogehoge";
    register int r = 999;
    int a = 123;
    int *ap = &a;
    int b = 456;
    int *bp = &b;
    int total = 0;
    int (* functionPointer)(int, int);
    functionPointer = &add;
    total = add(a, b);
    zzz = 789;
    int totalByPointer = functionPointer(a, b);
    printf("%d\n", total);
    return 0;
}
 