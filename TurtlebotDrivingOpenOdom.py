#!/usr/bin/env python
import rospy
import matplotlib.pyplot as plt
import tf
import math
from std_msgs.msg import String
import  geometry_msgs
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
class Pose():
	def __init__(self,x,y,theta):
		self.x=x
		self.y=y
		self.theta=theta

class TurtlebotDriving():

	def __init__(self,pose):
		self.pose=pose
		self.pub=rospy.Publisher('cmd_vel', Twist,queue_size=1)
		rospy.on_shutdown(self.shutdown)
	def odom_callback(self, msg):
		# Get (x, y, theta) specification from odometry topic
		quarternion = [msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,\
		            msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
		(roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quarternion)

		self.pose.theta = yaw 
		self.pose.x = msg.pose.pose.position.x
		self.pose.y = msg.pose.pose.position.y
	def shutdown(self):
		self.pub.publish(Twist())
	def driver(self):
		pub=rospy.Publisher('cmd_vel', Twist,queue_size=1)
		s=rospy.Subscriber("odom",Odometry,self.odom_callback)
		rospy.init_node('time', anonymous=True)
		d=1
		v=0.1
		s=0.1
		step=0
		plotx=[]
		ploty=[]
		r = rospy.Rate(10)
		t = rospy.Time.now()
		fwd=Twist()
		rot=Twist()
		default=Twist()
		fwd.linear.x=v
		rot.angular.z=s
		count=0
		pub.publish(default)
		while count<5:
	
		     		
				t2=rospy.Time.now()
				while rospy.Time.now()-t2< rospy.Duration(d/v):
					pub.publish(fwd)
					plotx.append(self.pose.x)
					ploty.append(self.pose.y)
					r.sleep()
				pub.publish(default)
				t2=rospy.Time.now()
				while rospy.Time.now()-t2< rospy.Duration(math.pi/2/s):
					pub.publish(rot)
					r.sleep()
				pub.publish(default)
				count=count+1	

		plt.plot(plotx,ploty)
		plt.show()	
			
			
if __name__ == '__main__':
       try:
	  t=TurtlebotDriving(Pose(0,0,0))			
          t.driver()
	
       except rospy.ROSInterruptException:
          pass
