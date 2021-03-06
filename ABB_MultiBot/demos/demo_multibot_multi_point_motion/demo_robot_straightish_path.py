#!/usr/bin/env python

import ast
import rospy
from rospy import Duration
import std_msgs.msg
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryActionGoal
import time

def functional(commanded_trajectory):
    pub_gary = rospy.Publisher('/gary/joint_trajectory_action/goal',
     FollowJointTrajectoryActionGoal, queue_size=10)
    pub_rosey = rospy.Publisher('/rosey/joint_trajectory_action/goal',
     FollowJointTrajectoryActionGoal, queue_size=10)
    rospy.init_node('traj_maker', anonymous=True)
    time.sleep(4)

    rate = rospy.Rate(0.01)
    i = 0
    while not rospy.is_shutdown():
       for command in commanded_trajectory:
           i += 1
           if i == 2:
               return
           
           #  first way to define a point
           traj_waypoint_1_gary = JointTrajectoryPoint()
           traj_waypoint_1_rosey = JointTrajectoryPoint()

           traj_waypoint_1_gary.positions = command          
           traj_waypoint_1_rosey.positions = [0,0,0,0,0,0]#[-1*elem for elem in command]
           traj_waypoint_1_rosey.time_from_start = Duration(2)

           traj_waypoint_1_rosey.time_from_start.secs = 0 + 2*i #first move slow
           
           #  second way to define a point
           traj_waypoint_2_gary = JointTrajectoryPoint(positions=[0,0,0,0,0,0],
            time_from_start = Duration(4))
           traj_waypoint_3_gary = JointTrajectoryPoint(positions=[-.4,-.2,-.3,-.1,0,0],
            time_from_start = Duration(6))
           traj_waypoint_4_gary = JointTrajectoryPoint(positions=[.5,.5,.5,.5,.5,.5],
            time_from_start = Duration(8))
           traj_waypoint_2_rosey = JointTrajectoryPoint(positions=[.31, -.051, .33, -.55, .28, .60],
            time_from_start = Duration(4))
           traj_waypoint_3_rosey = JointTrajectoryPoint(positions=[.14726, -.014151, .166507, -.33571, .395997, .38657],
            time_from_start = Duration(6))
           traj_waypoint_4_rosey = JointTrajectoryPoint(positions=[-.09309, .003150, .003559, .16149, .524427, -.1867],
            time_from_start = Duration(8))
           traj_waypoint_5_rosey = JointTrajectoryPoint(positions=[-.27752, .077886, -.1828, .38563, .682589, -.44665],
            time_from_start = Duration(10))   
                                            
           #debug in terminal
           #print traj_waypoint_1_gary.positions
           #print traj_waypoint_2_gary.positions
           #print traj_waypoint_1_rosey.positions
           #print traj_waypoint_2_rosey.positions
           
           #  making message
           message_gary = FollowJointTrajectoryActionGoal()
           message_rosey = FollowJointTrajectoryActionGoal()
           
           #  required headers
           header_gary = std_msgs.msg.Header(stamp=rospy.Time.now())
           header_rosey = std_msgs.msg.Header(stamp=rospy.Time.now())
           message_gary.goal.trajectory.header = header_gary
           message_rosey.goal.trajectory.header = header_rosey
           message_gary.header = header_gary
           message_rosey.header = header_rosey
           
           #  adding in joints
           joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', \
                          'joint_5', 'joint_6']
           message_gary.goal.trajectory.joint_names = joint_names
           message_rosey.goal.trajectory.joint_names = joint_names
           
           #  appending up to 100 points
           # ex. for i in enumerate(len(waypoints)): append(waypoints[i])
           message_gary.goal.trajectory.points.append(traj_waypoint_1_gary)
           message_gary.goal.trajectory.points.append(traj_waypoint_2_gary)
           message_gary.goal.trajectory.points.append(traj_waypoint_3_gary)
           message_gary.goal.trajectory.points.append(traj_waypoint_4_gary)
           #message_rosey.goal.trajectory.points.append(traj_waypoint_1_rosey)
           message_rosey.goal.trajectory.points.append(traj_waypoint_2_rosey)
           message_rosey.goal.trajectory.points.append(traj_waypoint_3_rosey)
           message_rosey.goal.trajectory.points.append(traj_waypoint_4_rosey)
           message_rosey.goal.trajectory.points.append(traj_waypoint_5_rosey)
          
           #  publishing to ROS node
           #pub_gary.publish(message_gary)
           pub_rosey.publish(message_rosey)
         
           rate.sleep()
           
           if rospy.is_shutdown():
               break
               

if __name__ == '__main__':
    commandL = []
    f = open('traj.txt','r')
    for line in f:
        parse_line = line.replace('\n','')
        parse_line = parse_line.replace(
        "{joint_names: {'joint_1', 'joint_2', 'joint_3' 'joint_4' 'joint_5', 'joint_6'}, points: ",'')
        positions_position = parse_line.find('positions')
        velocities_position = parse_line.find('velocities')
        
        position_command = parse_line[positions_position+10:velocities_position-2]

        commandL.append(ast.literal_eval(position_command))

    try:
        functional(commandL)
    except rospy.ROSInterruptException:
        pass
