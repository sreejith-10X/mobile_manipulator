from launch_ros.actions import Node
from launch import LaunchDescription
import os 
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command






def generate_launch_description():
    urdf_path=os.path.join(get_package_share_path("my_robot_description"),'urdf','my_robot.xacro')
    rviz_path=os.path.join(get_package_share_path('my_robot_description'),'config','new_config.rviz')

    robot_descrption=ParameterValue(Command(['xacro ' , urdf_path]), value_type=str)
    robot_descrption_node=Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_descrption}]
    )
    joint_state_publisher_node=Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"

    )
    rviz2=Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d',rviz_path])

    return LaunchDescription([
        robot_descrption_node,
        joint_state_publisher_node,
        rviz2
    ])