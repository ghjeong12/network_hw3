# POSTECH 2018 Spring CSED353 Assignment 3
# made by Jeong, Geonhwa / Kim, Junyoung

import socket
import pyaudio
import threading

HOST = '141.223.207.215'    #HOST ip address should be set by the user.
PORT = 23456                #PORT should be set by the user.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_chat.connect((HOST, PORT))

sock.settimeout(1)
print("[PROGRAM] CONNECTION COMPLETED")

# Functions for text chatting

def send_txt():
    while True:
        try:
            text_data = input()
            text_data = text_data.encode("utf-8")
            socket_chat.send(text_data)
        except:
            exit()

def receive_txt():
    while True:
        try:
            text_data = socket_chat.recv(1024)
            text_len = len(str(text_data))
            text_data = str(text_data)[2:text_len-1]
            print(text_data)
        except:
            exit()

threading._start_new_thread(send_txt, ())
threading._start_new_thread(receive_txt, ())

# Configuration for pyaudio

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

pyaudio_obj = pyaudio.PyAudio()

snd_stream = pyaudio_obj.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                #input_device_index=0,
                frames_per_buffer=CHUNK)

rcv_stream = pyaudio_obj.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                #output_device_index=1,
                frames_per_buffer=CHUNK)

# Functions for voice chatting
def receive_voice():
    voice_receive_data = ' '
    while True:
        try:
            voice_receive_data = sock.recv(1024)
            rcv_stream.write(voice_receive_data)
        except KeyboardInterrupt:
            rcv_stream.stop_stream()
            rcv_stream.close()
            snd_stream.stop_stream()
            snd_stream.close()
            pyaudio_obj.terminate()
            sock.close()
            socket_chat.close()
            print("[PROGRAM] SYSTEM TERMINATED")
            exit()
        except:
            rcv_stream.stop_stream()
            rcv_stream.close()
            snd_stream.stop_stream()
            snd_stream.close()
            pyaudio_obj.terminate()
            sock.close()
            socket_chat.close()
            print("[PROGRAM] SYSTEM TERMINATED")
            exit()

def send_voice():
    voice_send_data = ' '
    while True:
        try:
            voice_send_data = snd_stream.read(CHUNK)
            sock.sendall(voice_send_data)
        except:
            pass

threading._start_new_thread(send_voice, ())

# Main process will receive voice data
receive_voice()

print("[PROGRAM] CONNECTION CLOSED")
