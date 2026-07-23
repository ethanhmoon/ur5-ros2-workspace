# UR ROS 2 Workspace

A ROS 2 Humble workspace for controlling a simulated UR3 and ur5 arm in Gazebo via MoveIt2, running in Docker on Ubuntu 20.04.

Built on top of [mehmet-engineer/ros2_examples](https://github.com/mehmet-engineer/ros2_examples).

## Packages
- `my_package`, `py_srvcli`, `tutorial_interfaces`, `more_interfaces` — ROS 2 learning exercises
- `my_py_package` — `entry_points_node`, commands the UR5 to XYZ positions via pymoveit2
- `ur5_moveit_config` — generated MoveIt2 configuration
