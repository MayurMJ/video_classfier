cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(coram_task)

find_package(Torch REQUIRED)
find_package(cppzmq)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_executable(producer_main producer_main.cc)
target_link_libraries(producer_main "${TORCH_LIBRARIES}" cppzmq)
set_property(TARGET producer_main PROPERTY CXX_STANDARD 17)

add_executable(image_processor_main image_processor_main.cc)
target_link_libraries(image_processor_main "${TORCH_LIBRARIES}" cppzmq)
set_property(TARGET image_processor_main PROPERTY CXX_STANDARD 17)

add_executable(stats_reporting_main stats_reporting_main.cc)
target_link_libraries(stats_reporting_main "${TORCH_LIBRARIES}" cppzmq)
set_property(TARGET stats_reporting_main PROPERTY CXX_STANDARD 17)

# The following code block is suggested to be used on Windows.
# According to https://github.com/pytorch/pytorch/issues/25457,
# the DLLs need to be copied to avoid memory errors.
if (MSVC)
  file(GLOB TORCH_DLLS "${TORCH_INSTALL_PREFIX}/lib/*.dll")
  add_custom_command(TARGET producer_main
                     POST_BUILD
                     COMMAND ${CMAKE_COMMAND} -E copy_if_different
                     ${TORCH_DLLS}
                     $<TARGET_FILE_DIR:producer_main>)

  file(GLOB TORCH_DLLS "${TORCH_INSTALL_PREFIX}/lib/*.dll")
  add_custom_command(TARGET image_processor_main
                     POST_BUILD
                     COMMAND ${CMAKE_COMMAND} -E copy_if_different
                     ${TORCH_DLLS}
                     $<TARGET_FILE_DIR:image_processor_main>)

  file(GLOB TORCH_DLLS "${TORCH_INSTALL_PREFIX}/lib/*.dll")
  add_custom_command(TARGET stats_reporting_main
                     POST_BUILD
                     COMMAND ${CMAKE_COMMAND} -E copy_if_different
                     ${TORCH_DLLS}
                     $<TARGET_FILE_DIR:stats_reporting_main>)
endif (MSVC)
