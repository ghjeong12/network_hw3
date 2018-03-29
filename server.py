# POSTECH 2018 Spring CSED353 Assignment 3
# made by Jeong, Geonhwa / Kim, Junyoung

import socket
import pyaudio
import wave
import time
import threading

HOST = '141.223.207.215'    #HOST ip address should be set by the user.
PORT = 23456                #PORT should be set by the user.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# The socket will accept twice so that it can handle
# text chatting and voice chatting simultaneously.

conn, addr = s.accept()
conn_c, addr_c = s.accept()
s.setblocking(0)
print ("[PROGRAM] CONNECTION COMPLETED")

# Functions for text chatting

def send_txt():
    while True:
        text_data = input()
        text_data = text_data.encode("utf-8")
        conn_c.send(text_data)
    conn_c.close()

def receive_txt():
    while True:
        text_data = conn_c.recv(1024)
        if not text_data:
            break

        else:
            print (text_data)
            data = str(text_data).split("b'", 1)[1].rsplit("'", 1)[0]
            print (text_data)
    conn_c.close()

threading._start_new_thread(send_txt, ())
threading._start_new_thread(receive_txt, ())

# Configuration for pyaudio

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 4000

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
		output_device_index=1,
                frames_per_buffer=CHUNK)

stream2 = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
		 input_device_index=0,
                 frames_per_buffer=CHUNK)



data=' '
i=0
while data != '':
    try:			# receiving data
        data = conn.recv(1024)
        stream.write(data)
    except KeyboardInterrupt:
     	break
    except:
        pass

    try:		# sending data
        data2  = stream2.read(CHUNK)
        conn.sendall(data2)
    except KeyboardInterrupt:
     	break
    except:
        pass

stream.stop_stream()
stream.close()
stream2.stop_stream()
stream2.close()
p.terminate()
conn.close()
conn_c.close()
