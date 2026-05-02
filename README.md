# ROS2_example

A example of ROS2
这是一个为了示范 cv2 在 ROS_2 框架下例子
功能是使用 C++ 获取图片，用 Python 调整二值化
帧率不高，还有很多可以优化的地方

使用：

打开相机节点：
ros2 launch publish usb_camera.launch.py

打开二值化节点：
ros2 launch subscribe subscribe.launch.py

可视化：
rqt
