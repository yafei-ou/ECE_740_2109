import socket
import time
import numpy as np
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.0.3', 8005)
# x=[0.2, 0.4]
# message = struct.pack('<2d', *x)

# try:
#     while 1:
#         sent = sock.sendto(message, server_address)
#         time.sleep(1)

# finally:
#     print("stop")
#     sock.close()

# while True:
#     try:
#         msg=input("input:")
#         sock.sendto(bytes(msg, 'utf-8'), server_address)
#     finally:
#         sock.close()

# while True:
#     send_data = input("input")
#     if send_data=="exit":
#         break
#     elif send_data == "s":
#         sock.sendto(message, server_address)
#     else:
#         sock.sendto(send_data, server_address)
    

for i in range(10):
    x=np.array([0.2*i, 0.4*i])
    message = struct.pack('<2d', *x)
    sock.sendto(message, server_address)
    time.sleep(0.02)

sock.close()