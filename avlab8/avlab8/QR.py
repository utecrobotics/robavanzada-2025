#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from cv_bridge import CvBridge
import cv2
import numpy as np
from simple_actions import SimpleActionClient


class IBVSController(Node):
    def __init__(self):
        super().__init__('ibvs_controller')

        # Parámetros de cámara
        self.bridge = CvBridge()
        self.K = None
        self.dist = None
        self.qr_size = 0.10
        self.detector = cv2.QRCodeDetector()

        # Suscriptores
        self.create_subscription(Image, '/gripper_camera/image_raw', self.image_callback, 10)
        self.create_subscription(CameraInfo, '/gripper_camera/camera_info', self.info_callback, 10)

        # Punto deseado
        self.desired_pos = np.array([400.0, 400.0]) 
        
        # Variables de QR
        self.qr_detected = False
       
        self.get_logger().info("Nodo IBVS inicializado correctamente.")

    # --- Callback de cámara info ---
    def info_callback(self, msg):
        self.K = np.array(msg.k).reshape(3, 3)
        self.dist = np.array(msg.d)

    # --- Callback de imagen ---
    def image_callback(self, msg):
        if self.K is None or self.dist is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        data, bbox, _ = self.detector.detectAndDecode(frame)

        if bbox is not None and len(bbox) > 0:
            bbox = np.array(bbox[0], dtype=np.float32)
            obj_points = np.array([
                [-self.qr_size/2,  self.qr_size/2, 0],
                [ self.qr_size/2,  self.qr_size/2, 0],
                [ self.qr_size/2, -self.qr_size/2, 0],
                [-self.qr_size/2, -self.qr_size/2, 0]
            ], dtype=np.float32)

            success, rvec, tvec = cv2.solvePnP(obj_points, bbox, self.K, self.dist)
            if success:
                pos3d = tvec.flatten()
                
                K = np.array([[476.7, 0, 400.5],
              [0, 476.7, 400.5],
              [0,  0,  1]])


                p = K @ pos3d

                u = (p[0] / p[2])          
                v = (p[1] / p[2])
                
            
                #Posicion en pixeles 
                self.qr_pos = np.array([u,  v])
                self.Z = tvec[2]
                self.qr_detected = True

                #DIbujo QR
                cv2.drawFrameAxes(frame, self.K, self.dist, rvec, tvec, self.qr_size)
                cv2.polylines(frame, [bbox.astype(int)], True, (0,255,0), 2)

        cv2.imshow("IBVS QR Tracking", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = IBVSController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

