// strutils.c
#include "strutils.h"

int strlen_c(const char *s) {
    int len = 0;
    while (*s++) len++;
    return len;
}
