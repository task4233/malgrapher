#include <stdio.h>      /* printf */
#include <string.h>     /* memset */
#include <sys/ptrace.h> /* ptrace */
#include <sys/reg.h>    /* RIP */
#include <sys/types.h>  /* waitpid, stat */
#include <sys/wait.h>   /* waitpid */
#include <stdlib.h>     /* atoi, strtol, exit */
#include <sys/user.h> /* user_regs_struct */
#include <sys/stat.h>   /* stat */
#include <unistd.h>     /* stat */

void my_command(pid_t pid)
{
  struct user_regs_struct regs;

  memset(&regs, 0, sizeof(regs));

  ptrace(PTRACE_GETREGS, pid, 0, &regs);
  printf("arg 1: %ld\n", regs.rdi);
}

void p_attach(pid_t pid)
{
  int status;

  ptrace(PTRACE_ATTACH, pid, NULL, NULL);
  waitpid(pid, &status, 0);
}

long p_break(pid_t pid, void *addr)
{
  long original_text;

  original_text = ptrace(PTRACE_PEEKTEXT, pid, addr, NULL);
  ptrace(PTRACE_POKETEXT, pid, addr, ((original_text & 0xFFFFFFFFFFFFFF00) | 0xCC));
  printf("Breakpoint at %p.\n", addr);

  return original_text;
}

void p_delete(pid_t pid, void *addr, long original_text)
{
  ptrace(PTRACE_POKEUSER, pid, sizeof(long) * RIP, addr);
  ptrace(PTRACE_POKETEXT, pid, addr, original_text);
}

void p_continue(pid_t pid)
{
  int status;

  ptrace(PTRACE_CONT, pid, NULL, NULL);
  printf("Continuing.\n");

  waitpid(pid, &status, 0);

  if (WIFEXITED(status))
  {
    printf("Program exited normally.\n");
    exit(0);
  }

  if (WIFSTOPPED(status))
    printf("Breakpoint.\n");
  else
    exit(1);
}

void p_stepi(pid_t pid)
{
  int status;

  ptrace(PTRACE_SINGLESTEP, pid, NULL, NULL);
  waitpid(pid, &status, 0);
}

void p_quit(pid_t pid)
{
  ptrace(PTRACE_DETACH, pid, NULL, NULL);
}

int main(int argc, char *argv[])
{
  pid_t pid;
  void *addr;
  long original_text;
  struct stat buf;

  if (argc < 2)
  {
    printf("Usage: ptrace_demo <pid> <addr>\n");
    printf("Example: ptrace_demo 1234 0xabcdef0123456789\n");
    exit(1);
  }

  pid = atoi(argv[1]);
  addr = (void *)strtol(argv[2], NULL, 0);

  p_attach(pid);
  original_text = p_break(pid, addr);
  while (1)
  {
    p_continue(pid);
    p_delete(pid, addr, original_text);

    if (stat("./quit", &buf) == 0)
      break;

    /* do stuff */
    my_command(pid);

    p_stepi(pid);
    original_text = p_break(pid, addr);
  }

  p_quit(pid);

  return 0;
}