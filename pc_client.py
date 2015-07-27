# This is pc_client.py file, which will be running on Windows pc

# Import socket module
import socket # for socket programming functions               
import sys # for exit
import Leap

# Create a socket object
# Address Family : AF_INET (this is IP version 4 or IPv4)
# Type : SOCK_STREAM (this means connection oriented TCP protocol)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket is created.'

# connect to host by remote_ip and port
host = '192.168.137.16' # put IP address of raspberry pi as a host (you can find if by using command: ipconfig)
port = 12345

#Connect to remote server
s.connect((host , port))	
print 'Socket Connected to ' + host 
print s.recv(1024) # just conformation msg from rpi_server.py program running on Raspberry pi

# Listener function which is called by every frame given by Leap Motion Sensor
class MainListener(Leap.Listener):
    # To check initialized or not 
    def on_init(self, controller):
        print "Initialized"
    
    # To check LM Sensor is connected or not 
    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"
        
    # This function will be executed when "Enter" is pressed means program will be terminated
    def on_exit(self, controller):
        print "Exited"
    # called by our frames 
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
     	
     	'''
     	meaning of msg which is sent according to hand movements
     	0 - when program will be ened by user 
     	1 - to open the door
     	2 - to close the door
     	3 - to move car in forward - right direction
     	4 - to move car in forward - left direction
     	5 - to move car in forward direction
     	6 - to move car in backward - right direction
     	7 - to move car in backward - left direction
     	8 - to move car in backward direction
     	9 - to stop car
     	'''
        for hand in frame.hands:
	        hand_dir = hand.direction # go to this link... https://developer.leapmotion.com/documentation/python/api/Leap.Hand.html#Leap.Hand.direction
	        ang = hand_dir.pitch # go to thi link... https://developer.leapmotion.com/documentation/python/api/Leap.Vector.html#Leap.Vector.pitch
	        ang_yaw = hand_dir.yaw # go to this link... https://developer.leapmotion.com/documentation/python/api/Leap.Vector.html#Leap.Vector.yaw
	        
	        #For opening and closing of door in car
	        strength = hand.grab_strength # if hand is completely grabed strength=1 else 0<=strength<1
	        if(strength==1):
	        	print "Door opened"
	        	s.send('1')
	        else:
	        	print "Door Closed..."
	        	s.send('2')
	        	if(ang <= -0.25):
	        		if(ang_yaw>=0.20):
	        			print "forward-Right"
	        			s.send('3')
	        		elif(ang_yaw<=-0.20):
	        			print "Forward-Left"
	        			s.send('4')
	        		else:
	        			print "Forward"
	        			s.send('5')
	        	elif(ang >= 0.25):
	        		if(ang_yaw>=0.30):
	        			print "Backward-Right"
	        			s.send('6')
	       		 	elif(ang_yaw<=-0.50):
	        			print "Backward-Left"
	        			s.send('7')
	        		else:
		        		print "Backward"
		        		s.send('8')
	        	else:
	        		print "Stop"
	        		s.send('9')


def  main():
	#code for leap motion listener
	listener = MainListener()
	controller = Leap.Controller()
	controller.add_listener(listener)	 
	
	# we can stop program using "Enter" button 
	print "Press ENTER to stop process.."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# it will send '0' which stands for stopping connection from this client
		s.send('0')
		s.close
		controller.remove_listener(listener)



if __name__ == "__main__":
    main()
