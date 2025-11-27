cmake_minimum_required(VERSION 4.2.0)
project(Animecho)

# required by Qt 6
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(INIParser REQUIRED IMPORTED_TARGET iniparser)
find_package(X11)
pkg_check_modules(LibVLC IMPORTED_TARGET libvlc)
find_package(Qt6 REQUIRED COMPONENTS WebChannel Widgets WebEngineWidgets)

qt_wrap_cpp(QT_MOC_SRCS
  first.h)

add_executable(animecho
  ${QT_MOC_SRCS}
  first.cc
  animecho.cc)

if(X11_FOUND)
  target_compile_definitions(animecho PRIVATE -DBACKEND_IS_X11)
  target_link_libraries(animecho PRIVATE X11::X11)
endif()

if(LibVLC_FOUND)
  target_compile_definitions(animecho PRIVATE -DBACKEND_IS_LIBVLC)
  target_link_libraries(animecho PRIVATE PkgConfig::LibVLC)
endif()

target_link_libraries(animecho PRIVATE
  PkgConfig::INIParser
  Qt6::WebChannel
  Qt6::Widgets
  Qt6::WebEngineWidgets)
