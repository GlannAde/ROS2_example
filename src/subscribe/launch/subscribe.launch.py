import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # 动态获取安装后的配置文件路径
    config_file = os.path.join(
        get_package_share_directory("subscribe"), "config", "config.yaml"
    )

    return LaunchDescription(
        [
            Node(
                package="subscribe",
                executable="subscribe_node",  # <--- 必须改成与 setup.py 一致
                name="subscribe_node",
                output="screen",
                # 建议使用动态路径加载参数，不要写死 src/
                parameters=[config_file],
            )
        ]
    )
