# This is client.py file which will be running on Windows

# Import socket module
import socket               
import sys  #for exit
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

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
host = '127.0.0.1'
port = 12345

#Connect to remote server
s.connect((host , port))	
print 'Socket Connected to ' + host 
print s.recv(1024)


class MainListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
     
        for hand in frame.hands:
	        hand_dir = hand.direction
	        ang = hand_dir.pitch
	        ang_yaw = hand_dir.yaw
	        
	        #For opening and closing of door
	        strength = hand.grab_strength
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

	print "Press ENTER to stop process.."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		s.close
		s.send('0')
		controller.remove_listener(listener)



if __name__ == "__main__":
    main()