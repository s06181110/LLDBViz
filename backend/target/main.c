#include <stdio.h>

int add (int a, int b) {
    int result = a + b;
    return result;
}

int main(int argc, const char * argv[]) {
    char hoge[10] = "hogehoge";
    int a = 123;
    int *ap = &a;
    int b = 456;
    int total = 0;
    total = add(a, b);
    printf("%d\n", total);
    return 0;
}
