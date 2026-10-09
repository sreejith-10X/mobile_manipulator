from launch import LaunchDescription
from launch_ros.actions import Node

import os

from ament_index_python.packages import get_package_share_path

from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable
)

from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    # ============================================================
    # PATHS
    # House world
    world_path = os.path.join(
        get_package_share_path("my_robot_description"),
        "my_house",
        "worlds",
        "house.world"
    )



    # House models
    house_models_path = os.path.join(
        get_package_share_path("my_robot_description"),
        "my_house",
        "models"
    )
    map_path = os.path.join(
    get_package_share_path("my_robot_bringup"),
    "maps",
    "my_world.yaml"
)

    # Robot Xacro
    urdf_path = os.path.join(
        get_package_share_path("my_robot_description"),
        "urdf",
        "my_robot.xacro"
    )

    # RViz configuration
    rviz_path = os.path.join(
        get_package_share_path("my_robot_description"),
        "config",
        "new_config.rviz"
    )

    # Gazebo bridge configuration
    gazebo_config_path = os.path.join(
        get_package_share_path("my_robot_bringup"),
        "config",
        "gazebo_bridge.yaml"
    )

  
    # ============================================================
    # GAZEBO RESOURCE PATH
    # ============================================================

    gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=(
            f"{house_models_path}:"
            f"{os.environ.get('GZ_SIM_RESOURCE_PATH', '')}"
        )
    )

    # Optional old Gazebo/Ignition resource path
    ign_resource_path = SetEnvironmentVariable(
        name="IGN_GAZEBO_RESOURCE_PATH",
        value=(
            # f"{robot_models_path}:"
            f"{house_models_path}:"
            f"{os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')}"
        )
    )

    # ============================================================
    # ROBOT DESCRIPTION
    # ============================================================

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    robot_description_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True
            }
        ]
    )

    # ============================================================
    # RVIZ
    # ============================================================

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_path],
        parameters=[
            {
                "use_sim_time": True
            }
        ]
    )

    # ============================================================
    # GAZEBO HARMONIC
    # ============================================================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_path("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": f"-r {world_path}"
        }.items()
    )

    # ============================================================
    # SPAWN ROBOT
    # ============================================================

    gazebo_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "my_robot",
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2'
        ],
        output="screen"

    )

    # ============================================================
    # GAZEBO <-> ROS 2 BRIDGE
    # ============================================================

    gazebo_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": gazebo_config_path
            }
        ],
        output="screen"
    )

    nav2=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_path("nav2_bringup"),
                         "launch",
                         "bringup_launch.py"),
                         
        ),
        launch_arguments=
            {"use_sim_time":"True",
            "maps":map_path
            }.items()

        
    )

    # ============================================================
    # LAUNCH
    # ============================================================

    return LaunchDescription([
        gz_resource_path,
        ign_resource_path,

        robot_description_node,

        rviz2,

        gazebo,

        gazebo_node,

        gazebo_bridge_node,
        nav2

    ])
