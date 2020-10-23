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

	
	def odom_callback(self, msg):
		# Get (x, y, theta) specification from odometry topic
		quarternion = [msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,\
		            msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
		(roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quarternion)

		self.pose.theta = yaw 
		self.pose.x = msg.pose.pose.position.x
		self.pose.y = msg.pose.pose.position.y

	def driver(self):
		pub=rospy.Publisher('cmd_vel', Twist,queue_size=1)
		s=rospy.Subscriber("odom",Odometry,self.odom_callback)
		rospy.init_node('time', anonymous=True)
		d=1
		v=0.1
		s=0.3
		step=0
		plotx=[]
		ploty=[]
		breaking_rate=0.1
		r = rospy.Rate(10)
		t = rospy.Time.now()
		x=self.pose.x
		y=self.pose.y
		theta=self.pose.theta
		fwd=Twist()
		rot=Twist()
		default=Twist()
		fwd.linear.x=v
		rot.angular.z=s
		distance_cumul=0
		spin_cumul=0
		count=0
		'''rospy.Time.now() - t < rospy.Duration(500) and'''
		pub.publish(default)
		while step<4:
			x=self.pose.x
			y=self.pose.y
			while distance_cumul<d:
				distance_cumul=distance_cumul+math.sqrt(pow(self.pose.x-x,2)+pow(self.pose.y-y,2))
	
		     		pub.publish(fwd)
				r.sleep()
				
				plotx.append(self.pose.x)
				ploty.append(self.pose.y)
				if(count%3==0):
			     		x=self.pose.x
					y=self.pose.y
				count=count+1
				"""print(distance_cumul,math.sqrt(pow(self.pose.x-x,2)+pow(self.pose.y-y,2)),self.pose.x)
"""
			distance_cumul=0
			
			
			t_break=rospy.Time.now()
			while(rospy.Time.now()-t_break<rospy.Duration(3)):
				pub.publish(default)		
				r.sleep()
		

			theta=self.pose.theta
			spin_cumul=0
			while spin_cumul<math.pi/2:
				spin_cumul=spin_cumul+(self.pose.theta-theta)%math.pi
				""""print ("angle spin:",spin_cumul,self.pose.theta,theta)
"""				
				theta=self.pose.theta
				pub.publish(rot)
				r.sleep()
					

			
			
			
			t_break=rospy.Time.now()
			while(rospy.Time.now()-t_break<rospy.Duration(3)):
				pub.publish(default)
				r.sleep()	
				"""print("break ang")"""
			plotx.append(self.pose.x)
			ploty.append(self.pose.y)
			step=step+1
		plt.plot(plotx,ploty)
		plt.show()
if __name__ == '__main__':
       try:
	  t=TurtlebotDriving(Pose(0,0,0))			
          t.driver()
	
       except rospy.ROSInterruptException:
          pass
