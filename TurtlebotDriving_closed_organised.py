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
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        
class TurtlebotDriving():
    def __init__(self, pose, plotx=[], ploty=[]):
        self.pose = pose
        self.plotx = plotx
        self.ploty = ploty
        
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        
        rospy.init_node('time', anonymous=True)
        
        self.r = rospy.Rate(10)
        
        rospy.on_shutdown(self.shutdown)
        
    
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
        
        # get pose info from method odom_callback to plot
        rospy.Subscriber("odom",Odometry,self.odom_callback)
        
        distance = 1
        linear_speed = 0.075
        angular_speed = 0.1
        step = 0
        
        r = rospy.Rate(10)
        t = rospy.Time.now()
        
        # go straight msg
        fwd = Twist()
        fwd.linear.x = linear_speed
        # turn around msg
        rot = Twist()
        rot.angular.z = angular_speed
        # still
        default = Twist()
        
        distance_cumul = 0
        spin_cumul = 0
        count = 0
        self.pub.publish(default)
        
        while step < 4:
            ori_x = self.pose.x
            ori_y = self.pose.y
            while distance_cumul < distance:
                distance_cumul=distance_cumul+math.sqrt(pow(self.pose.x-ori_x,2)+pow(self.pose.y-ori_y,2))
                self.pub.publish(fwd)
                self.r.sleep()
                self.plotx.append(self.pose.x)
                self.ploty.append(self.pose.y)
                if (count % 3 == 0):
                    ori_x = self.pose.x
                    ori_y = self.pose.y
                count += 1
                
            distance_cumul = 0
            t_break = rospy.Time.now()
            
            while rospy.Time.now() - t_break < rospy.Duration(3):
                self.pub.publish(default)
                self.r.sleep()
                
            ori_theta = self.pose.theta
            spin_cumul = 0
            while spin_cumul < math.pi/2:
                spin_cumul = spin_cumul + (self.pose.theta - ori_theta) % math.pi
                ori_theta = self.pose.theta
                self.pub.publish(rot)
                self.r.sleep()
              
            t_break = rospy.Time.now()
            
            while(rospy.Time.now()-t_break<rospy.Duration(3)):
                self.pub.publish(default)
                self.r.sleep()  
                
            self.plotx.append(self.pose.x)
            self.ploty.append(self.pose.y)
            step += 1
            
        self.plot_trajectory()
        
           
    def shutdown(self):
        rospy.loginfo('stopping turtlebot')
        self.pub.publish(Twist())
        rospy.sleep(1)
        
        
if __name__ == '__main__':
    try:
        t=TurtlebotDriving(Pose(0,0,0), [], [])			
        t.driver()
	
    except rospy.ROSInterruptException:
        pass
