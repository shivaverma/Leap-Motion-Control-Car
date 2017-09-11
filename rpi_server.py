# This is rpi_server.py file, which will be running on raspberry pi

# Import socket module
import socket               
import sys  #for exit
import RPi.GPIO as gpio
'''
pin assignment on raspberry pi
pin no. -> action
37      = Gate Open
29      = forward
31      = Backward
32      = Right
33      = Left
'''

# to setup these pins 
gpio.setmode(gpio.BOARD)
gpio.setup(37,gpio.OUT)
gpio.setup(29,gpio.OUT)
gpio.setup(31,gpio.OUT)
gpio.setup(32,gpio.OUT)
gpio.setup(33,gpio.OUT)

# to initialize these pins to off
gpio.output(37, False)
gpio.output(29, False)
gpio.output(31, False)
gpio.output(32, False)
gpio.output(33, False)

# Create a socket object
# Address Family : AF_INET (this is IP version 4 or IPv4)
# Type : SOCK_STREAM (this means connection oriented TCP protocol)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket is created.'

# setup a server host name and port to listen from client
host = '192.168.137.16' # put IP address of raspberry pi as a host (you can find if by using command: ifconfig)
port = 12345    
try:
    # Bind to the porttry:
    s.bind((host, port))

except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print "Binding completed"

# Now wait for client connection
s.listen(5)                 # 5 shows howmany clients can wait in a queue
print "listening.."


while True:
  c, addr = s.accept()     # Establish connection with client.
  print 'Got connection from '+ addr[0] + ':' + str(addr[1])
  c.send('Thank you for connecting') # conformation msg to client 
  while True:
    # recieve msg as 0,1,2....9
    key = c.recv(1024)
    print key
    # if client program is terminated
    if(key=='0'):
      break
    # 1 - to open the door
    if(key=='1'):
      gpio.output(29, False)
      gpio.output(31, False)
      gpio.output(32, False)
      gpio.output(33, False)
      gpio.output(37, True)
    else:
      gpio.output(37, False)
      '''
      3 - to move car in forward - right direction
      4 - to move car in forward - left direction
      5 - to move car in forward direction
      6 - to move car in backward - right direction
      7 - to move car in backward - left direction
      8 - to move car in backward direction
      9 - to stop car
      '''
      if(key=='3'):
        gpio.output(29, True)
        gpio.output(31, False)
        gpio.output(32, True)
        gpio.output(33, False)
      elif(key=='4'):
        gpio.output(29, True)
        gpio.output(31, False)
        gpio.output(32, False)
        gpio.output(33, True)
      elif(key=='5'):
        gpio.output(29, True)
        gpio.output(31, False)
        gpio.output(32, False)
        gpio.output(33, False)
      elif(key=='6'):
        gpio.output(29, False)
        gpio.output(31, True)
        gpio.output(32, True)
        gpio.output(33, False)
      elif(key=='7'):
        gpio.output(29, False)
        gpio.output(31, True)
        gpio.output(32, False)
        gpio.output(33, True)
      elif(key=='8'):
        gpio.output(29, False)
        gpio.output(31, True)
        gpio.output(32, False)
        gpio.output(33, False)
      elif(key=='9'):
        gpio.output(29, False)
        gpio.output(31, False)
        gpio.output(32, False)
        gpio.output(33, False)
  c.close()                # Close the connection
  gpio.output(37, False)
  gpio.output(29, False)
  gpio.output(31, False)
  gpio.output(32, False)
  gpio.output(33, False)
s.close 
