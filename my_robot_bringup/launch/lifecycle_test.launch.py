from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

def generate_launch_description():
    id = LaunchDescription()
    number_node_name="count_server"

    number_node=LifecycleNode(
        package="action_py",
        executable="count_server",
        name="count_server",
        namespace=""

    )

    lifecycle_node_manager=Node(
        package="action_py",
        executable="Lifecylemanager",
        parameters=[
            {
                "node_name": number_node_name
            }
        ]
    )

    number_server=Node(
        package="action_py",
        executable="count_client",

    )


    id.add_action(number_node)
    id.add_action(lifecycle_node_manager)
    id.add_action(number_server)
    return id