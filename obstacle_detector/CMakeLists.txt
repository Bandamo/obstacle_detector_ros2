cmake_minimum_required(VERSION 3.5)
project(obstacle_detector)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake_auto REQUIRED)
find_package(Armadillo REQUIRED)
find_package(Boost 1.54.0 REQUIRED system)
ament_auto_find_build_dependencies()

set(TARGET scans_merger)
ament_auto_add_library(${TARGET} SHARED
  src/${TARGET}.cpp
)
target_link_libraries(${TARGET} ${ARMADILLO_LIBRARIES})
rclcpp_components_register_node(${TARGET}
  PLUGIN "obstacle_detector::ScansMerger"
  EXECUTABLE ${TARGET}_node
)

set(TARGET obstacle_extractor)
ament_auto_add_library(${TARGET} SHARED
  src/${TARGET}.cpp
)
target_link_libraries(${TARGET} ${ARMADILLO_LIBRARIES})
rclcpp_components_register_node(${TARGET}
  PLUGIN "obstacle_detector::ObstacleExtractor"
  EXECUTABLE ${TARGET}_node
)

set(TARGET obstacle_tracker)
ament_auto_add_library(${TARGET} SHARED
  src/${TARGET}.cpp
)
target_link_libraries(${TARGET} ${ARMADILLO_LIBRARIES})
rclcpp_components_register_node(${TARGET}
  PLUGIN "obstacle_detector::ObstacleTracker"
  EXECUTABLE ${TARGET}_node
)

set(TARGET obstacle_publisher)
ament_auto_add_library(${TARGET} SHARED
  src/${TARGET}.cpp
)
target_link_libraries(${TARGET} ${ARMADILLO_LIBRARIES})
rclcpp_components_register_node(${TARGET}
  PLUGIN "obstacle_detector::ObstaclePublisher"
  EXECUTABLE ${TARGET}_node
)


# Build rviz plugins
#
# set(CMAKE_AUTOMOC ON)

# if(rviz_QT_VERSION VERSION_LESS "5")
#   message(STATUS "Using Qt4 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
#   find_package(Qt4 ${rviz_QT_VERSION} EXACT REQUIRED QtCore QtGui)
#   include(${QT_USE_FILE})
# else()
#   message(STATUS "Using Qt5 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
#   find_package(Qt5 ${rviz_QT_VERSION} EXACT REQUIRED Core Widgets)
#   set(QT_LIBRARIES Qt5::Widgets)
# endif()

# add_definitions(-DQT_NO_KEYWORDS)

# add_library(${PROJECT_NAME}_gui
#   src/displays/obstacles_display.cpp include/${PROJECT_NAME}/displays/obstacles_display.h
#   src/displays/circle_visual.cpp include/${PROJECT_NAME}/displays/circle_visual.h
#   src/displays/segment_visual.cpp include/${PROJECT_NAME}/displays/segment_visual.h
#   #
#   src/panels/scans_merger_panel.cpp include/${PROJECT_NAME}/panels/scans_merger_panel.h
#   src/panels/obstacle_extractor_panel.cpp include/${PROJECT_NAME}/panels/obstacle_extractor_panel.h
#   src/panels/obstacle_tracker_panel.cpp include/${PROJECT_NAME}/panels/obstacle_tracker_panel.h
#   src/panels/obstacle_publisher_panel.cpp include/${PROJECT_NAME}/panels/obstacle_publisher_panel.h)
# target_link_libraries(${PROJECT_NAME}_gui ${QT_LIBRARIES} ${catkin_LIBRARIES})
# add_dependencies(${PROJECT_NAME}_gui ${catkin_EXPORTED_TARGETS})

#
# Install libraries
#
# install(TARGETS scans_merger obstacle_extractor obstacle_tracker obstacle_publisher ${PROJECT_NAME}_nodelets ${PROJECT_NAME}_gui
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION})

#
# Install nodelet and rviz plugins description
#
# install(FILES nodelet_plugins.xml rviz_plugins.xml
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

#
# Install launch files
#
# install(DIRECTORY launch/
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

#
# Create folders and copy resources
#
# file(MAKE_DIRECTORY $ENV{HOME}/.local/share/icons/robor)
# file(COPY resources/play.png resources/stop.png DESTINATION $ENV{HOME}/.local/share/icons/robor)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_auto_package(INSTALL_TO_SHARE
  launch
)
