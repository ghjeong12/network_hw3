import socket
import pyaudio
import wave
import threading

#record
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
#RECORD_SECONDS = 4000

#HOST = '127.0.0.1'
#HOST = '141.223.206.86'    # The remote host
HOST = '141.223.204.146'
PORT = 50007              # The same port as used by the server
PORT_CHAT = 33333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_chat.connect((HOST, PORT))

#socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket_chat.connect((HOST, PORT_CHAT))

s.setblocking(0)
#connection setup done and connected to server

##### Text chatting function #####
def sendMsg():
    while True:
        data_text = input()
        #data_text = bytes(data_text, "utf-8")
        data_text = data_text.encode("utf-8")
        #s.send(data_text)
        socket_chat.send(data_text)
    socket_chat.close()
    #s.close()

def getMsg():
    while True:
        data_text = socket_chat.recv(1024)
        #data_text = s.recv(1024)
        print(data_text)
        data_text = str(data_text).split("b'", 1)[1].rsplit("'",1)[0]
        print(data_text)
    socket_chat.close()
    #s.close()
#### end def
threading._start_new_thread(sendMsg, ())
threading._start_new_thread(getMsg, ())

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



print("*recording")

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
