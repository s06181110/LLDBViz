#include <stdio.h>

int addByPointers(int* firstPointer, int* secondPointer) {
	int resultValue = *firstPointer + *secondPointer;
	return resultValue;
}

int addByValues(int firstValue, int secondValue) {
	int resultValue = firstValue + secondValue;
	return resultValue;
}

int main(int argc, const char * argv[]) {
    int firstValue = 123, *firstPointer = &firstValue;
    int secondValue = 456, *secondPointer = &secondValue;
    int resultByValue, resultByPointer;
    int (* functionPointer)(int, int);
    functionPointer = &addByValues;

    resultByValue = addByValues(firstValue, secondValue);
    resultByPointer = addByPointers(firstPointer, secondPointer);
    printf("result ...    byValue: %d,    byPointer: %d\n", resultByValue, resultByPointer);
    return 0;
}
 