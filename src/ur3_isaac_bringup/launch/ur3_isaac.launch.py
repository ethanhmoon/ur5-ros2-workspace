from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare("ur3_isaac_bringup")

    xacro_file = PathJoinSubstitution([pkg, "urdf", "ur3_isaac.urdf.xacro"])
    controllers_yaml = PathJoinSubstitution([pkg, "config", "controllers.yaml"])

    robot_description = {"robot_description": Command(["xacro ", xacro_file])}

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": True}],
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controllers_yaml, {"use_sim_time": True}],
        output="screen",
    )

    jsb_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    jtc_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
    )

    delayed_jtc = RegisterEventHandler(
        OnProcessExit(target_action=jsb_spawner, on_exit=[jtc_spawner])
    )

    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("ur_moveit_config"), "/launch/ur_moveit.launch.py"
        ]),
        launch_arguments={
            "ur_type": "ur3",
            "use_sim_time": "true",
            "use_fake_hardware": "false",
            "launch_rviz": "true",
        }.items(),
    )

    return LaunchDescription([rsp, control_node, jsb_spawner, delayed_jtc, moveit])
