#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class Rotator():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)


    def handle_text_input(self, data):
        
        move_data = data.data 
        self.twist = Twist()
        dir={'F': [1, 0],'R': [0, -1],'L': [0, 1],'S': [0, 0],'B': [-1, 0],}
        
        if move_data =="forward":
            arg = "F"
        elif move_data =="right":
            arg = "R"
        elif move_data == "left":
            arg ="L"
        elif move_data == "stop":
            arg = "S"
            
        r = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            self.twist.linear.x ,self.twist.angular.z =dir[arg]
            self._cmd_pub.publish(self.twist)
            rospy.loginfo("Rotating robot: %s", self.twist)
            r.sleep()

        #rospy.loginfo(rospy.get_caller_id() + "Command received: %s", data.data)
        
    
    def listening(self):
        print("listening")
        rospy.Subscriber("bulldog", String, self.handle_text_input)
        rospy.spin()
        


def main():
    rospy.init_node('lex_conv')
    try:
        rotator = Rotator()
        rotator.listening()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
    
