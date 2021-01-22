#include <stdio.h>
#include <unistd.h>

void func(int x);

void func(int x)
{
  printf("hello, world: %d\n", x);
}

int main(int argc, char *argv[])
{
  int i = 0;

  for (i = 1; i <= 100; i++)
  {
    sleep(1);
    func(i);
  }
  return 0;
}