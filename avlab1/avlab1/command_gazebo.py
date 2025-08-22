#!/usr/bin/env python3
import rclpy
import threading
import numpy as np
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import *
from rclpy.action import ActionClient
from builtin_interfaces.msg import Duration

def main():

  rclpy.init()
  node = rclpy.create_node('command')
  robot_client = ActionClient(node, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')
    
  thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
  thread.start()
 
  print("Waiting for server...")
  robot_client.wait_for_server()
  print("Connected to server")
 
  # Joint names
  jnames = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint','wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
  # Joint Configuration
  Q0  = [0.0, -np.pi/4, np.pi/4, 0.0, 0.0, 0.0]
 
  g = FollowJointTrajectory.Goal()
  g.trajectory = JointTrajectory()
  g.trajectory.joint_names = jnames
 
  #point = JointTrajectoryPoint()
  #point.positions = Q0
  #point.velocities = [0.0] * len(jnames)
  #point.time_from_start = Duration(sec=2)
 
  #goal.trajectory.points.append(point)
  g.trajectory.points = [JointTrajectoryPoint(positions=Q0, velocities=[0]*6, time_from_start=rclpy.duration.Duration(seconds=2).to_msg())]
  robot_client.send_goal_async(g)
    
  # Loop rate (in Hz)
  rate = node.create_rate(10)
  # Continuous execution loop
  while rclpy.ok():

    # Modification of the motion
    Q0[0] = Q0[0]-0.005

    g.trajectory.points = [ JointTrajectoryPoint(positions=Q0, velocities=[0]*6, time_from_start=rclpy.duration.Duration(seconds=0.05).to_msg())]
    robot_client.send_goal_async(g)
    
    # Wait for the next iteration
    rate.sleep()
  
  node.destroy_node()
  rclpy.shutdown()
if __name__ == '__main__':
  main()
  
