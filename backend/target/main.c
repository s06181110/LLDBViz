#include <stdio.h>

int add (int a, int b) {
    char hoge[10] = "hogehoge";
    int result = a + b;
    return result;
}

int main(int argc, const char * argv[]) {
    char hoge[10] = "hogehoge";
    int a = 123;
    int *ap = &a;
    int b = 456;
    int *bp = &b;
    int total = 0;
    int (* functionPointer)(int, int);
    functionPointer = &add;
    total = add(a, b);
    int totalByPointer = functionPointer(a, b);
    printf("%d\n", total);
    return 0;
}
 