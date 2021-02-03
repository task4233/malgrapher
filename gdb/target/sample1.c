#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  argc = 2;
  argv[1] = "1";
  argv[2] = "0";
  if (argc < 2) {
    puts("lacked arguments");
  }
  int flag1 = atoi(argv[1]);
  int flag2 = atoi(argv[2]);
  if (flag1) {
    if (flag2) {
        puts("True & True");
    } else {
        puts("True & False");
    }
  } else {
    if (flag2) {
        puts("False & True");
    } else {
        puts("False & False");
    }
  }
}
