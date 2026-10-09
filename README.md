# 🤖 Autonomous Mobile Manipulator using ROS 2

A simulated autonomous mobile manipulator featuring a differential-drive mobile base and a two-joint robotic arm operating in a custom indoor environment designed using Blender.

The project integrates **ROS 2 Jazzy, Gazebo Harmonic, URDF/Xacro, SLAM Toolbox, and Nav2** to demonstrate robot modeling, sensor integration, environment mapping, and autonomous navigation. Python-based navigation is implemented using the Nav2 Simple Commander API.

## 🚀 Features

- **Custom Environment:** Indoor environment designed in Blender and imported into Gazebo using visual and collision meshes.
- **Modular Robot Design:** Differential-drive mobile base and two-joint manipulator modeled using URDF/Xacro.
- **Sensor Integration:** Simulated camera and 2D LiDAR for environmental perception.
- **ROS 2–Gazebo Integration:** Sensor data and robot communication through `ros_gz_bridge`.
- **SLAM Mapping:** 2D occupancy grid map generated using SLAM Toolbox and saved for reuse.
- **Autonomous Navigation:** Nav2-based path planning and obstacle avoidance using the saved map.
- **Python Navigation:** Programmatic goal execution and waypoint navigation using the Nav2 Simple Commander API.

## 🛠 Technologies

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Blender
- URDF / Xacro
- RViz 2
- SLAM Toolbox
- Nav2
- Nav2 Simple Commander
- Python

## 📁 Repository Structure

```text
mobile_manipulator/
│
├── README.md
│
├── my_robot_bringup/
│   ├── config/
│   │   ├── gazebo_bridge.yaml
│   │   └── slam_config.yaml
│   ├── launch/
│   │   ├── my_robot_gazebo.launch.py
│   │   └── my_robot_gazebo_cc.launch.py
│   └── maps/
│       ├── my_world.yaml
│       └── my_world.pgm
│
└── my_robot_description/
    ├── config/
    │   └── new_config.rviz
    ├── launch/
    │   └── display.launch.py
    ├── my_house/
    │   ├── models/
    │   │   └── house/
    │   │       ├── visual.glb
    │   │       ├── collision.glb
    │   │       ├── model.sdf
    │   │       └── model.config
    │   └── worlds/
    │       └── house.world
    └── urdf/
        ├── arm.xacro
        ├── mobile_base_gazebo.xacro
        ├── mobile_robot.xacro
        ├── my_robot.xacro
        └── properties.xacro
```

*The tree shows the intended structure. Ensure the filenames match your actual repository.*

## ⚙️ Installation

### 1. Prerequisites

Install and configure:

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Required ROS 2 packages for Nav2, SLAM Toolbox, Xacro, RViz, and Gazebo integration.

### 2. Clone the Repository

```bash
mkdir -p ~/ros2-ws/src
cd ~/ros2-ws/src

git clone https://github.com/sreejith-10X/mobile_manipulator.git
```

### 3. Install Dependencies

```bash
source /opt/ros/jazzy/setup.bash

sudo apt update
rosdep update

cd ~/ros2-ws

rosdep install --from-paths src --ignore-src -r -y
```

### 4. Build the Workspace

```bash
cd ~/ros2-ws

colcon build --symlink-install
source install/setup.bash
```

## ▶️ Running the Project

### 1. Visualize the Robot

To inspect the robot model and its kinematic structure in RViz:

```bash
ros2 launch my_robot_description display.launch.py
```

### 2. Launch the Simulation and Navigation

Start the main launch file:

```bash
ros2 launch my_robot_bringup my_robot_gazebo.launch.py
```

This launch file initializes:

- Gazebo Harmonic and the custom indoor environment.
- The robot description and robot spawning process.
- RViz for visualization.
- ROS 2–Gazebo communication using `ros_gz_bridge`.
- Nav2 autonomous navigation using the previously generated map.

### 3. Programmatic Navigation

Once the simulation and Nav2 are running, execute your Python navigation script:

```bash
python3 path/to/your_commander_script.py
```

The script can use the Nav2 Simple Commander API to send navigation goals, execute waypoint sequences, and monitor navigation feedback.

Replace the example path with the location of your actual Python script.

## 🗺️ Mapping

The indoor environment was mapped using **SLAM Toolbox**, producing a 2D occupancy grid map.

The saved map consists of:

- `my_world.yaml` — map metadata and configuration.
- `my_world.pgm` — occupancy grid image.

The saved map is loaded by Nav2 during normal autonomous navigation, so SLAM does not need to run every time the robot starts.

To generate or update the map, launch SLAM Toolbox separately:

```bash
ros2 launch slam_toolbox online_async_launch.py \
  params_file:=$(ros2 pkg prefix my_robot_bringup)/share/my_robot_bringup/config/slam_config.yaml \
  use_sim_time:=True
```

Drive the robot through the environment and save the map when mapping is complete.

## 🔧 Future Improvements

- Integrate MoveIt 2 for manipulator motion planning.
- Coordinate mobile navigation with arm movements.
- Implement object detection and localization using computer vision.
- Develop autonomous pick-and-place tasks.

## 👤 Author

**Sreejith Raju**

GitHub: [@sreejith-10X](https://github.com/sreejith-10X)

---

If you find this project useful, consider giving the repository a ⭐.