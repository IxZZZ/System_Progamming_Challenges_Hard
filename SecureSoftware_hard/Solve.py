import socket
import getpass

# get username
username = getpass.getuser()

# get pc name
pcname = socket.gethostname()

print('Username: ',username)
print('PcName: ',pcname)

# Generate key from username and pcname
for i in (username+pcname):
    hex_value = ord(i)%16
    print(hex(hex_value)[2:].upper(),end='')