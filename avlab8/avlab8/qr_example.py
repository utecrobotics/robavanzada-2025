import cv2
import rclpy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo

global K; global dist; global bridge; global detector; global qr_size
K = 0; dist = 0; qr_size = 0.10
bridge = CvBridge()
detector = cv2.QRCodeDetector()

def img_callback(msg): 
  global K; global dist; global bridge; global detector;
  #print(K)
  #print(dist)
  #if K == 0 or dist == 0:
  #  pass
  #else:
  frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
  data, bbox, _ = detector.detectAndDecode(frame)
  
  if bbox is not None and len(bbox) > 0:
    bbox = np.array(bbox[0], dtype=np.float32)
    obj_points = np.array([
                 [-qr_size/2,  qr_size/2, 0],
                 [ qr_size/2,  qr_size/2, 0],
                 [ qr_size/2, -qr_size/2, 0],
                 [-qr_size/2, -qr_size/2, 0]
               ], dtype=np.float32)
    
    success, rvec, tvec = cv2.solvePnP(obj_points, bbox, K, dist)
    if success:
      pos3d = tvec.flatten()
                
      K = np.array([[476.7, 0, 400.5],
                    [0, 476.7, 400.5],
                    [0,  0,  1]])

      p = K @ pos3d

      u = (p[0] / p[2])          
      v = (p[1] / p[2])
      print(str(u) + " " + str(v))
            
      #Posicion en pixeles 
      qr_pos = np.array([u,  v])
      Z = tvec[2]
      qr_detected = True

      #DIbujo QR
      cv2.drawFrameAxes(frame, K, dist, rvec, tvec, qr_size)
      cv2.polylines(frame, [bbox.astype(int)], True, (0,255,0), 2)

    cv2.imshow("IBVS QR Tracking", frame)
    cv2.waitKey(1)


def info_callback(msg):
  global K; global dist;
  K = np.array(msg.k).reshape(3, 3)
  dist = np.array(msg.d)
  

def main():
  rclpy.init()

  node = rclpy.create_node('qr_detector')
  node.create_subscription(Image, '/gripper_camera/image_raw', img_callback, 10)
  node.create_subscription(CameraInfo, '/gripper_camera/camera_info', info_callback, 10)
  print("hola")
  
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Subscriber stopped by user')

  node.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()
