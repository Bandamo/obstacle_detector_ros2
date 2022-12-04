import os
import sys
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import Node

# scans_merger
# obstacle_extractor
# obstacle_tracker
# obstacle_publisher

def generate_launch_description():
    nodes = [
        ComposableNodeContainer(
            name='obstacle_detector_container',
            namespace='',
            package='rclcpp_components',
            executable='component_container',
            composable_node_descriptions=[
                ComposableNode(
                    package='urg_node',
                    plugin='urg_node::UrgNode',
                    name='urg_node_driver',
                    parameters=[
                        {'ip_address': '192.168.10.10'}
                    ],
                    remappings=[
                        ('scan', 'front_scan')
                    ]
                ),
                ComposableNode(
                    package='obstacle_detector',
                    plugin='obstacle_detector::ScansMerger',
                    name='scans_merger',
                    parameters=[
                        {'active': True},
                        {'publish_scan': False},
                        {'publish_pc;': True},
                        {'min_scanner_range': 0.05},
                        {'max_scanner_range': 10.0},
                        {'min_x_range': -10.0},
                        {'max_x_range': 10.0},
                        {'min_y_range': -10.0},
                        {'max_y_range': 10.0},
                        {'fixed_frame_id': 'map'},
                        {'target_frame_id': 'robot'},
                    ],
                ),
                ComposableNode(
                    package='obstacle_detector',
                    plugin='obstacle_detector::ObstacleExtractor',
                    name='obstacle_extractor',
                    parameters=[
                        {'active': True},
                        {'use_scan': False},
                        {'use_pcl': True},
                        {'use_split_and_merge': True},
                        {'circles_from_visibles': True},
                        {'discard_converted_segments': True},
                        {'transform_coordinates': True},
                        {'min_group_points': 5},
                        {'max_group_distance': 0.1},
                        {'distance_proportion': 0.00628},
                        {'max_split_distance': 0.2},
                        {'max_merge_separation': 0.2},
                        {'max_merge_spread': 0.2},
                        {'max_circle_radius': 0.6},
                        {'radius_enlargement': 0.3},
                        {'frame_id': 'map'},
                    ],
                ),
                # ComposableNode(
                #     package='obstacle_detector',
                #     plugin='obstacle_detector::ObstacleTracker',
                #     name='obstacle_tracker',
                #     parameters=[
                #         {'active': True},
                #         {'loop_rate': 100.0},
                #         {'tracking_duration': 2.0},
                #         {'min_correspondence_cost': 0.6},
                #         {'std_correspondence_dev': 0.15},
                #         {'process_variance': 0.1},
                #         {'process_rate_variance': 0.1},
                #         {'measurement_variance': 1.0},
                #         {'frame_id': 'map'},
                #     ],
                # ),
                # ComposableNode(
                #     package='obstacle_detector',
                #     plugin='obstacle_detector::ObstaclePublisher',
                #     name='obstacle_publisher',
                #     parameters=[
                #         {'active': True},
                #         {'reset': False},
                #         {'fusion_example': False},
                #         {'fission_example': False},
                #         {'loop_rate': 10.0},
                #         {'radius_margin': 0.25},
                #         {'x_vector': [-3.0, -2.5, -2.5, -1.0, -1.0, -0.5, 2.5, 0.2, 2.0, 4.5, 4.0, 1.5]},
                #         {'y_vector': [1.5, 0.0, -2.5, 3.0, 1.0, -4.0, -3.0, -0.9, 0.0, 0.0, 2.0, 2.0]},
                #         {'r_vector': [0.5, 0.5, 1.5, 0.5, 0.7, 0.5, 1.5, 0.7, 0.7, 1.0, 0.5, 1.0]},
                #         {'vx_vector': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
                #         {'vy_vector': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
                #         {'frame_id': 'map'},
                #     ],
                # ),
            ],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_scanner_base',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'map', 'scanner_base'],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='scanner_base_to_robot',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'scanner_base', 'robot'],
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='robot_to_laser',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'robot', 'laser'],
        )
    ]

    return launch.LaunchDescription(nodes)
