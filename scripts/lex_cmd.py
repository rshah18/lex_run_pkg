#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import boto3
import json 

lex = boto3.client('lex-runtime', region_name='us-east-1')


class lex_bot_fun():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('/bulldog', String, queue_size=1)

    def command_handler(self, arg):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self._cmd_pub.publish(arg)
            r.sleep()

    
    def get_lex(self,text):
        lex_response = lex.post_text(
            botName='rosbot',
            botAlias='bulldog',
            userId='bot01',
            sessionAttributes={},
            requestAttributes={},
            inputText=text
            )
        move_cmd = lex_response['slots']["move_direction"]
        rospy.loginfo(move_cmd)
        self.command_handler(move_cmd)
        
        
        
        
        
def main():
    rospy.init_node('lex_cmd')
    try:
        rotator = lex_bot_fun()
        #rotator.command_handler("forward")
        rotator.get_lex("move forward")
        
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()