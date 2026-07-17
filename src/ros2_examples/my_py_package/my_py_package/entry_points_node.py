import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from pymoveit2 import MoveIt2
from threading import Thread
import time




class entryPointsNode(Node):
    def __init__(self):
        super().__init__('move_to_coordinate_node')
        self.moveit2 = MoveIt2(
            node=self,
            joint_names=["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"],
            base_link_name="base_link",
            end_effector_name="wrist_3_link",
            group_name="ur5_arm",
            callback_group=ReentrantCallbackGroup(),
        )
        self.moveit2.add_collision_box(
            id="ground_plane",
            size=[2.0, 2.0, 0.02],
            position=[0.0, 0.0, -0.01],
            quat_xyzw=[0.0, 0.0, 0.0, 1.0],
        )
        self.moveit2.planner_id = "RRTstarkConfigDefault"
        self.moveit2.allowed_planning_time = 10.0
        self.moveit2.num_planning_attempts = 5

    def move_to(self, x, y, z):
       self.moveit2.move_to_pose(
           position=[x, y, z],
           quat_xyzw=[0.0, 0.0, 0.0, 1.0],
       )
       success = self.moveit2.wait_until_executed()


       if success:
           self.get_logger().info(f"Moved to ({x}, {y}, {z})")
       else:
           self.get_logger().warn(f"Failed to move to ({x}, {y}, {z})")


       return success


#    def draw_square_from_corner(self, x, y, z, side=0.1):
#        corners = [
#            (x, y, z),
#            (x + side, y, z),
#            (x + side, y + side, z),
#            (x, y + side, z),
#            (x, y, z),
#        ]


#        for corner_x, corner_y, corner_z in corners:
#            success = self.move_to(corner_x, corner_y, corner_z)
#            if not success:
#                self.get_logger().warn(
#                    f"draw_square_from_corner stopped early at ({corner_x}, {corner_y}, {corner_z})"
#                )
#                return False
#            time.sleep(2.5)  # give real physical execution time to genuinely finish


#        self.get_logger().info("Finished drawing square from corner")
#        return True
   
    def draw_square_from_corner(self, x, y, z, side=0.1):
       corners = [
           (x , y, z+ side),
           (x , y + side, z+ side),
           (x, y + side, z),
           (x, y, z),
       ]


       for corner_x, corner_y, corner_z in corners:
           success = self.move_to(corner_x, corner_y, corner_z)
           if not success:
               self.get_logger().warn(
                   f"draw_square_from_corner stopped early at ({corner_x}, {corner_y}, {corner_z})"
               )
               return False
           time.sleep(2.5)  # give real physical execution time to genuinely finish


       self.get_logger().info("Finished drawing square from corner")
       return True




def main(args=None):
   rclpy.init(args=args)
   node = entryPointsNode()


   executor = MultiThreadedExecutor(2)
   executor.add_node(node)
   spin_thread = Thread(target=executor.spin, daemon=True)
   spin_thread.start()


   node.get_logger().info("Waiting for move_group services...")
   node.moveit2._MoveIt2__move_action_client.wait_for_server(timeout_sec=15.0)


   node.moveit2.move_to_configuration([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
   node.moveit2.wait_until_executed()
   time.sleep(1.0)  # let it fully settle before planning the next move




   node.draw_square_from_corner(0.3, 0.0, 0.6, side=0.3)


   executor.shutdown()
   node.destroy_node()
   rclpy.shutdown()




if __name__ == '__main__':
   main()
