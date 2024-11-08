#include <stdio.h>
#include <string.h>

void get_user_name() {
    char name[5];
    printf("Enter your name: ");
    gets(name);
    printf("Hello, %s!\n", name);
}

int main() {
    get_user_name();
    return 0;
}