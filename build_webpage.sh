#!/bin/sh

if [ $# -ne 1 -o "$1" != "Debug" -a "$1" != "Release" ]; then
  echo "Usage: $0 <Debug|Release>" >&2
  exit 1
fi

function dropout_include_quiet_if_exist ()
{
  if [ -e "$1" ]; then
    source "$1" >/dev/null 2>/dev/null
  fi
}

dropout_include_quiet_if_exist /opt/qt6-wasm/qtwasm_env.sh

dropout_deps=('cmake' 'ninja' 'emcmake' 'qtpaths')

for dropout_dep in "${dropout_deps[@]}"; do
  if ! command -v "$dropout_dep" >/dev/null 2>&1; then
    echo "Cannot find program in PATH: ${dropout_dep}" >&2
    exit 1
  fi
done

if [ ! -e CMakeCache.txt -o "$0" -nt CMakeCache.txt -o "$(sed -E -n 's/^CMAKE_BUILD_TYPE:STRING=(.*)$/\1/p' CMakeCache.txt 2>/dev/null)" != "$1" ]; then
  dropout_qt_pfx="$(qtpaths --query QT_INSTALL_PREFIX)"
  if [ -z "$dropout_qt_pfx" -o ! -d "$dropout_qt_pfx" ]; then
    echo 'Unable to locate Qt 6 installation' >&2
    exit 1
  fi

  emcmake cmake -S . --fresh -G Ninja -DCMAKE_BUILD_TYPE="$1" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_TOOLCHAIN_FILE="${dropout_qt_pfx}/lib/cmake/Qt6/qt.toolchain.cmake"
  if [ $? -ne 0 ]; then
    rm -f CMakeCache.txt
    exit 1
  fi
fi

ninja
