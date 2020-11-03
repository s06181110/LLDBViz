#include <stdio.h>

int add (int a, int b) {
    int result = a + b;
    return result;
}

int main(int argc, const char * argv[]) {
    char hoge[10] = "hogehoge";
    int a = 123;
    int b = 456;
    int total = 0;
    int *ap = &a;
    int (* functionPointer)(int, int);
    functionPointer = &add;
    total = add(a, b);
    int totalByPointer = functionPointer(a, b);
    printf("%d\n", total);
    return 0;
}
 