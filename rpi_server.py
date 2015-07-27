# Import socket module
import socket               
import sys  #for exit
import RPi.GPIO as gpio

a = 37 # Gate Open
b = 29 # forward
c = 31 # Backward
d = 32 # Right
e = 33 # Left

gpio.setmode(gpio.BOARD)
gpio.setup(a,gpio.OUT)
gpio.setup(b,gpio.OUT)
gpio.setup(c,gpio.OUT)
gpio.setup(d,gpio.OUT)
gpio.setup(e,gpio.OUT)

gpio.output(a, False)
gpio.output(b, False)
gpio.output(c, False)
gpio.output(d, False)
gpio.output(e, False)

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
host = '127.0.0.1'
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
  c.send('Thank you for connecting')
  while True:
    key = c.recv(1024)
    print key
    if(key=='0'):
      break
    if(key=='1'):
      gpio.output(b, False)
      gpio.output(c, False)
      gpio.output(d, False)
      gpio.output(e, False)
      gpio.output(a, True)
    else:
      gpio.output(a, False)
      if(key=='3'):
        gpio.output(b, True)
        gpio.output(c, False)
        gpio.output(d, True)
        gpio.output(e, False)
      elif(key=='4'):
        gpio.output(b, True)
        gpio.output(c, False)
        gpio.output(d, False)
        gpio.output(e, True)
      elif(key=='5'):
        gpio.output(b, True)
        gpio.output(c, False)
        gpio.output(d, False)
        gpio.output(e, False)
      elif(key=='6'):
        gpio.output(b, False)
        gpio.output(c, True)
        gpio.output(d, True)
        gpio.output(e, False)
      elif(key=='7'):
        gpio.output(b, False)
        gpio.output(c, True)
        gpio.output(d, False)
        gpio.output(e, True)
      elif(key=='8'):
        gpio.output(b, False)
        gpio.output(c, True)
        gpio.output(d, False)
        gpio.output(e, False)
      elif(key=='9'):
        gpio.output(b, False)
        gpio.output(c, False)
        gpio.output(d, False)
        gpio.output(e, False)
  c.close()                # Close the connection
  gpio.output(a, False)
  gpio.output(b, False)
  gpio.output(c, False)
  gpio.output(d, False)
  gpio.output(e, False)
s.close 
