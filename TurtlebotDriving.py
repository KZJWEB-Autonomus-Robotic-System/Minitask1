#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import pi

class open_loop():
    def __init__(self):
        rospy.init_node('square', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        rate = 50
        r = rospy.Rate(rate)
        
        linear_speed = 0.2
        distance = 1
        
        angular_speed = 1.0
        goal_angle = pi/2
        
        linear_duration = distance / linear_speed
        angular_duration = goal_angle / angular_speed
        
        ticks_str = int(linear_duration * rate)
        ticks_ang = int(goal_angle *rate)
        
        while not rospy.is_shutdown():
            vel_info = Twist()
            vel_info.linear.x = linear_speed
            
            # (1 / 0.2) * 50 = 100
            # command should run 50 times
            
            for t in range(ticks_str):
                self.pub.publish(vel_info)
                r.sleep()
                
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
            
            
    def shutdown(self):
        rospy.loginfo('stopping turtlebot')
        self.pub.publish(Twist())
        rospy.sleep(1)
        
if __name__ == '__main__':
    try:
        open_loop()
    except rospy.ROSInterruptException:
        pass
