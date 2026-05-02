#!/usr/bin/env python3
import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data  # 导入传感器专用QoS
from sensor_msgs.msg import Image


class ImageProcessor(Node):
    def __init__(self):
        super().__init__("subscribe_node")
        self.bridge = CvBridge()

        # 声明动态参数
        self.declare_parameter("threshold", 127)

        # 使用 qos_profile_sensor_data：只处理最新的画面，丢弃积压的旧帧
        # 这是解决“画面延迟”和“看起来帧率低”的关键配置
        self.subscription = self.create_subscription(
            Image, "image_raw", self.listener_callback, qos_profile_sensor_data
        )

        self.publisher_ = self.create_publisher(Image, "img_threshold", 1)
        self.get_logger().info("图像处理节点已启动 (QoS: Sensor Data)，等待数据...")

    def listener_callback(self, data):
        try:
            # 1. 转换图像
            cv_img = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

            # 2. 获取参数
            thresh_val = (
                self.get_parameter("threshold").get_parameter_value().integer_value
            )

            # 3. 极简处理 (减少计算开销)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            _, processed_img = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

            # 4. 发布结果
            out_msg = self.bridge.cv2_to_imgmsg(processed_img, encoding="mono8")
            out_msg.header = data.header
            self.publisher_.publish(out_msg)

        except Exception as e:
            self.get_logger().error(f"处理失败: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    node = ImageProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
