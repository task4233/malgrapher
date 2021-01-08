$ gcc -o ./test ./test.c 
./test.c: In function ‘main’:
./test.c:4:5: warning: implicit declaration of function ‘puts’ [-Wimplicit-function-declaration]
     puts("true");
     ^~~~
$ ls
test  test.c
$ gdb -q ./test
Reading symbols from ./test...(no debugging symbols found)...done.
gdb-peda$ b main
Breakpoint 1 at 0x63e
gdb-peda$ s
The program is not being run.
gdb-peda$ r
Starting program: /home/al17111/work/research/playground/gdb/test 
[----------------------------------registers-----------------------------------]
RAX: 0x55555555463a (<main>:	push   rbp)
RBX: 0x0 
RCX: 0x555555554670 (<__libc_csu_init>:	push   r15)
RDX: 0x7fffffffe128 --> 0x7fffffffe4fa ("CLUTTER_IM_MODULE=xim")
RSI: 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
RDI: 0x1 
RBP: 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
RIP: 0x55555555463e (<main+4>:	sub    rsp,0x10)
R8 : 0x7ffff7dced80 --> 0x0 
R9 : 0x7ffff7dced80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554530 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe110 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555554635 <frame_dummy+5>:	jmp    0x5555555545a0 <register_tm_clones>
   0x55555555463a <main>:	push   rbp
   0x55555555463b <main+1>:	mov    rbp,rsp
=> 0x55555555463e <main+4>:	sub    rsp,0x10
   0x555555554642 <main+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555554649 <main+15>:	cmp    DWORD PTR [rbp-0x4],0x0
   0x55555555464d <main+19>:	je     0x55555555465d <main+35>
   0x55555555464f <main+21>:	lea    rdi,[rip+0x9e]        # 0x5555555546f4
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
0008| 0x7fffffffe038 --> 0x7ffff7a03bf7 (<__libc_start_main+231>:	mov    edi,eax)
0016| 0x7fffffffe040 --> 0x1 
0024| 0x7fffffffe048 --> 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
0032| 0x7fffffffe050 --> 0x100008000 
0040| 0x7fffffffe058 --> 0x55555555463a (<main>:	push   rbp)
0048| 0x7fffffffe060 --> 0x0 
0056| 0x7fffffffe068 --> 0x6485c366122c11a9 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x000055555555463e in main ()
gdb-peda$ s
[----------------------------------registers-----------------------------------]
RAX: 0x55555555463a (<main>:	push   rbp)
RBX: 0x0 
RCX: 0x555555554670 (<__libc_csu_init>:	push   r15)
RDX: 0x7fffffffe128 --> 0x7fffffffe4fa ("CLUTTER_IM_MODULE=xim")
RSI: 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
RDI: 0x1 
RBP: 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
RIP: 0x555555554642 (<main+8>:	mov    DWORD PTR [rbp-0x4],0x0)
R8 : 0x7ffff7dced80 --> 0x0 
R9 : 0x7ffff7dced80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554530 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe110 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x55555555463a <main>:	push   rbp
   0x55555555463b <main+1>:	mov    rbp,rsp
   0x55555555463e <main+4>:	sub    rsp,0x10
=> 0x555555554642 <main+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555554649 <main+15>:	cmp    DWORD PTR [rbp-0x4],0x0
   0x55555555464d <main+19>:	je     0x55555555465d <main+35>
   0x55555555464f <main+21>:	lea    rdi,[rip+0x9e]        # 0x5555555546f4
   0x555555554656 <main+28>:	call   0x555555554510 <puts@plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
0008| 0x7fffffffe028 --> 0x0 
0016| 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
0024| 0x7fffffffe038 --> 0x7ffff7a03bf7 (<__libc_start_main+231>:	mov    edi,eax)
0032| 0x7fffffffe040 --> 0x1 
0040| 0x7fffffffe048 --> 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
0048| 0x7fffffffe050 --> 0x100008000 
0056| 0x7fffffffe058 --> 0x55555555463a (<main>:	push   rbp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x0000555555554642 in main ()
gdb-peda$ s
[----------------------------------registers-----------------------------------]
RAX: 0x55555555463a (<main>:	push   rbp)
RBX: 0x0 
RCX: 0x555555554670 (<__libc_csu_init>:	push   r15)
RDX: 0x7fffffffe128 --> 0x7fffffffe4fa ("CLUTTER_IM_MODULE=xim")
RSI: 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
RDI: 0x1 
RBP: 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
RIP: 0x555555554649 (<main+15>:	cmp    DWORD PTR [rbp-0x4],0x0)
R8 : 0x7ffff7dced80 --> 0x0 
R9 : 0x7ffff7dced80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554530 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe110 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x55555555463b <main+1>:	mov    rbp,rsp
   0x55555555463e <main+4>:	sub    rsp,0x10
   0x555555554642 <main+8>:	mov    DWORD PTR [rbp-0x4],0x0
=> 0x555555554649 <main+15>:	cmp    DWORD PTR [rbp-0x4],0x0
   0x55555555464d <main+19>:	je     0x55555555465d <main+35>
   0x55555555464f <main+21>:	lea    rdi,[rip+0x9e]        # 0x5555555546f4
   0x555555554656 <main+28>:	call   0x555555554510 <puts@plt>
   0x55555555465b <main+33>:	jmp    0x555555554669 <main+47>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
0008| 0x7fffffffe028 --> 0x0 
0016| 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
0024| 0x7fffffffe038 --> 0x7ffff7a03bf7 (<__libc_start_main+231>:	mov    edi,eax)
0032| 0x7fffffffe040 --> 0x1 
0040| 0x7fffffffe048 --> 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
0048| 0x7fffffffe050 --> 0x100008000 
0056| 0x7fffffffe058 --> 0x55555555463a (<main>:	push   rbp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x0000555555554649 in main ()
gdb-peda$ s
[----------------------------------registers-----------------------------------]
RAX: 0x55555555463a (<main>:	push   rbp)
RBX: 0x0 
RCX: 0x555555554670 (<__libc_csu_init>:	push   r15)
RDX: 0x7fffffffe128 --> 0x7fffffffe4fa ("CLUTTER_IM_MODULE=xim")
RSI: 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
RDI: 0x1 
RBP: 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
RIP: 0x55555555464d (<main+19>:	je     0x55555555465d <main+35>)
R8 : 0x7ffff7dced80 --> 0x0 
R9 : 0x7ffff7dced80 --> 0x0 
R10: 0x0 
R11: 0x0 
R12: 0x555555554530 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe110 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x55555555463e <main+4>:	sub    rsp,0x10
   0x555555554642 <main+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555554649 <main+15>:	cmp    DWORD PTR [rbp-0x4],0x0
=> 0x55555555464d <main+19>:	je     0x55555555465d <main+35>
 | 0x55555555464f <main+21>:	lea    rdi,[rip+0x9e]        # 0x5555555546f4
 | 0x555555554656 <main+28>:	call   0x555555554510 <puts@plt>
 | 0x55555555465b <main+33>:	jmp    0x555555554669 <main+47>
 | 0x55555555465d <main+35>:	lea    rdi,[rip+0x95]        # 0x5555555546f9
 |->   0x55555555465d <main+35>:	lea    rdi,[rip+0x95]        # 0x5555555546f9
       0x555555554664 <main+42>:	call   0x555555554510 <puts@plt>
       0x555555554669 <main+47>:	mov    eax,0x0
       0x55555555466e <main+52>:	leave
                                                                  JUMP is taken
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe020 --> 0x7fffffffe110 --> 0x1 
0008| 0x7fffffffe028 --> 0x0 
0016| 0x7fffffffe030 --> 0x555555554670 (<__libc_csu_init>:	push   r15)
0024| 0x7fffffffe038 --> 0x7ffff7a03bf7 (<__libc_start_main+231>:	mov    edi,eax)
0032| 0x7fffffffe040 --> 0x1 
0040| 0x7fffffffe048 --> 0x7fffffffe118 --> 0x7fffffffe4ca ("/home/al17111/work/research/playground/gdb/test")
0048| 0x7fffffffe050 --> 0x100008000 
0056| 0x7fffffffe058 --> 0x55555555463a (<main>:	push   rbp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x000055555555464d in main ()
gdb-peda$ 
ここでjeが来ているので, flagの状態を理解する
記憶しておくのは, `0x000055555555464d`と`$eflagsの状態($2 = [ PF ZF IF ] )`
今回はjeなのでZFを両方確認すれば良い

