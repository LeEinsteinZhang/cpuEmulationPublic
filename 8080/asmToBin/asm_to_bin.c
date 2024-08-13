#include <stdio.h>

int main() {
    char str1[100], str2[100];
    char buffer[100];
    int intValue;
    char charValue;

    while (1) {
        printf("Enter input (str str int/char/str int/char/str): ");
        if (scanf("%s %s", str1, str2) != 2) break;

        // 读取第三个值
        scanf("%s", buffer);
        if (sscanf(buffer, "%d", &intValue) == 1) {
            // 输入是整数
            printf("Third value is an integer: %d\n", intValue);
        } else {
            // 输入是字符串
            printf("Third value is a string: %s\n", buffer);
        }

        // 读取第四个值
        scanf("%s", buffer);
        if (sscanf(buffer, "%d", &intValue) == 1) {
            // 输入是整数
            printf("Fourth value is an integer: %d\n", intValue);
        } else if (sscanf(buffer, "%c", &charValue) == 1) {
            // 输入是字符
            printf("Fourth value is a character: %c\n", charValue);
        } else {
            // 输入是字符串
            printf("Fourth value is a string: %s\n", buffer);
        }
    }

    return 0;
}