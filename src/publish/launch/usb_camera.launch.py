import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. 动态获取配置文件的绝对路径
    config_file = os.path.join(
        get_package_share_directory('publish'), # 确保这里是 publish
        'config',
        'camera_config.yaml'
    )

    # 2. 定义节点
    node = Node(
        package='publish',          # 必须与 CMakeLists.txt 中的项目名一致 
        executable='usb_camera_node',
        name='usb_camera_node',
        output='screen',
        # 3. 加载外部 YAML 配置文件，使设置生效
        parameters=[config_file] 
    )

    return LaunchDescription([node])