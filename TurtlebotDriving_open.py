#!/usr/bin/env python
import rospy
import matplotlib.pyplot as plt
import tf
from math import pi
from std_msgs.msg import String
import  geometry_msgs
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Pose():
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

class open_loop():
    def __init__(self, pose, plotx=[], ploty=[]):
        rospy.init_node('square', anonymous=False)
        rospy.on_shutdown(self.shutdown)

        self.pose = pose
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)


        self.plotx = plotx
        self.ploty = ploty
        				
    def odom_callback(self, msg):
	   # Get (x, y, theta) specification from odometry topic
        quarternion = [msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,\
                    msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quarternion)
								
        self.pose.theta = yaw 
        self.pose.x = msg.pose.pose.position.x
        self.pose.y = msg.pose.pose.position.y	
								
    def plot_trajectory(self):
        plt.plot(self.plotx,self.ploty)
        plt.show()   
        
    def driver(self):
        rospy.Subscriber("odom",Odometry,self.odom_callback)
        step = 0

        rate = 50
        r = rospy.Rate(rate)

        linear_speed = 0.2
        distance = 1

        fwd = Twist()
        fwd.linear.x = linear_speed

        angular_speed = 1.0
        goal_angle = pi/2

        linear_duration = distance / linear_speed
        angular_duration = goal_angle / angular_speed
        
        ticks_str = int(linear_duration * rate)
        ticks_ang = int(goal_angle *rate)
             
        while step < 4:    
   	        # (1 / 0.2) * 50 = 250
	        # command should run 250 times

            for t in range(ticks_str):
                self.pub.publish(fwd)
                r.sleep()
                self.plotx.append(self.pose.x)
                self.ploty.append(self.pose.y)
                
            vel_info = Twist()
            self.pub.publish(vel_info)
            rospy.sleep(1)
           # stop robot before turn around
            
            vel_info.angular.z = angular_speed
            for t in range(ticks_ang):
                self.pub.publish(vel_info)
                r.sleep()
            
            vel_info = Twist()
            self.pub.publish(vel_info)
            rospy.sleep(1)
            
            step += 1
            
        self.plot_trajectory()
            
            
    def shutdown(self):
        rospy.loginfo('stopping turtlebot')
        self.pub.publish(Twist())
        rospy.sleep(1)
        
if __name__ == '__main__':
    try:
        t = open_loop(Pose(0,0,0), [], [])
        t.driver()
    except rospy.ROSInterruptException:
        pass
