import socket
import pyaudio
import wave
import threading

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
#RECORD_SECONDS = 4000

#HOST = '141.223.206.86'    # The remote host
HOST = '141.223.207.215'    #HOST ip address should be set by the user.
PORT = 23456                #PORT should be set by the user.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_chat.connect((HOST, PORT))

s.setblocking(0)
print("[PROGRAM] CONNECTION COMPLETED]")

##### Text chatting function #####
def send_txt():
    while True:
        text_data = input()
        text_data = text_data.encode("utf-8")
        socket_chat.send(text_data)
    socket_chat.close()

def receive_txt():
    while True:
        text_data = socket_chat.recv(1024)
        text_len = len(str(text_data))
        #data_text = str(data_text).split("b'", 1)[1].rsplit("'",1)[0]
        text_data = str(text_data)[2:text_len-1]
        print(text_data)
    socket_chat.close()

threading._start_new_thread(send_txt, ())
threading._start_new_thread(receive_txt, ())


p = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()


# for sending data
stream = p2.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                #input_device_index=0,
                frames_per_buffer=CHUNK)


# for receiving data
stream2 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                #output_device_index=1,
                frames_per_buffer=CHUNK)

# Functions for voice chatting
def receive_voice():
    voice_receive_data = ' '

data2='a'
data = 'a'

i=0
while data2 != '':

 try:		# sending data
     data  = stream.read(CHUNK)
     s.sendall(data)
 except KeyboardInterrupt:
     break
 except :
     pass

 try:       	# receiving data
     data2 = s.recv(1024)
     stream2.write(data2)
 except KeyboardInterrupt:
     break
 except:
     #print ("receive except")
     pass

print("*done recording")





stream.stop_stream()
stream.close()
stream2.stop_stream()
stream2.close()
p.terminate()
s.close()
socket_chat.close()
print("[SYSTEM] Connections closed")
