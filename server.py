# POSTECH 2018 Spring CSED353 Assignment 3
# made by Jeong, Geonhwa / Kim, Junyoung

import socket
import pyaudio
import threading

HOST = '141.223.207.215'    #HOST ip address should be set by the user.
PORT = 23456                #PORT should be set by the user.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("[PROGRAM] WAITING FOR CLIENT CONNECTION")
# The socket will accept twice so that it can handle
# text chatting and voice chatting simultaneously.

conn, addr = sock.accept()
conn_c, addr_c = sock.accept()
print ("[PROGRAM] CONNECTION COMPLETED")

# Functions for text chatting

def send_txt():
    while True:
        try:
            text_data = input()
            text_data = text_data.encode("utf-8")
            conn_c.send(text_data)
        except:
            conn_c.close()

def receive_txt():
    while True:
        try:
            text_data = conn_c.recv(1024)
            if not text_data:
                break

            else:
                # default setting puts b' in the beginning of the text.
                text_len = len(str(text_data))
                text_data = str(text_data)[2:text_len-1]
                print (text_data)
        except:
            conn_c.close()

threading._start_new_thread(send_txt, ())
threading._start_new_thread(receive_txt, ())

# Configuration for pyaudio

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

pyaudio_obj = pyaudio.PyAudio()

rcv_stream = pyaudio_obj.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
		#output_device_index=1,
                frames_per_buffer=CHUNK)

snd_stream = pyaudio_obj.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
		 #input_device_index=0,
                 frames_per_buffer=CHUNK)

def receive_voice():
    voice_receive_data = ' '
    while True:
        try:
            voice_receive_data = conn.recv(1024)
            rcv_stream.write(voice_receive_data)
        except KeyboardInterrupt:
            rcv_stream.stop_stream()
            rcv_stream.close()
            snd_stream.stop_stream()
            snd_stream.close()
            pyaudio_obj.terminate()
            conn.close()
            conn_c.close()
            sock.close()
            print("[PROGRAM] SYSTEM TERMINATED")
            exit()
        except:
            rcv_stream.stop_stream()
            rcv_stream.close()
            snd_stream.stop_stream()
            snd_stream.close()
            pyaudio_obj.terminate()
            conn.close()
            conn_c.close()
            sock.close()
            print("[PROGRAM] SYSTEM TERMINATED")
            exit()

def send_voice():
    voice_send_data = ' '
    while True:
        try:
            voice_send_data = snd_stream.read(CHUNK)
            conn.sendall(voice_send_data)
        except:
            pass

threading._start_new_thread(send_voice, ())

# Main process will receive voice data
receive_voice()

print("[PROGRAM] CONNECTION CLOSED")
