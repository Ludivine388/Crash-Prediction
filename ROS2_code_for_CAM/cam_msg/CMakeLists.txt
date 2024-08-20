cmake_minimum_required(VERSION 3.8)
project(cam_msg)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Set the path to the 'msg' directory
set(msg_dir "${CMAKE_CURRENT_SOURCE_DIR}/msg")

# List all .msg files in the 'msg' directory
file(GLOB msg_files "${msg_dir}/*.msg")

# Convert to relative paths relative to the package directory
set(relative_msg_files "")
foreach(msg_file ${msg_files})
  string(REPLACE "${CMAKE_CURRENT_SOURCE_DIR}/" "" relative_msg_file "${msg_file}")
  list(APPEND relative_msg_files "${relative_msg_file}")
endforeach()

# Generate messages
rosidl_generate_interfaces(${PROJECT_NAME}
  ${relative_msg_files}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()