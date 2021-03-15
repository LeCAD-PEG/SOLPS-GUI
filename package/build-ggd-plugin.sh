#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="ggd_plugin"
VERSION=${VERSION:-refactor_for_ParaView_5.8.0}
GIT_LINK="ssh://git@git.iter.org/vis/paraview-ggd-plugin.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} ${VERSION}

IMAS_VERSION_DIGIT=$(echo "$IMAS_VERSION" | sed "s/\.//g")
CMAKE_FLAGS="-DIMAS_VERSION_DIGIT:INT=${IMAS_VERSION_DIGIT}"
# CMAKE_FLAGS="${CMAKE_FLAGS} -DOVERRIDE_MODULES_DIR=${STAGING_DIR}"
CMAKE_FLAGS="${CMAKE_FLAGS} -DCMAKE_C_FLAGS:STRING=-m64"
CMAKE_FLAGS="${CMAKE_FLAGS} -DCMAKE_BUILD_TYPE=DEBUG"
# Export CXXFLAGS as variable with strings are not propely handled with env.
export CXXFLAGS="-fpermissive"
_cmake "${CMAKE_FLAGS}" "" "${PACKAGE_SOURCE_DIR}/ReadUALGGD_source"
_make "-j${MAKE_JOBS} VERBOSE=1"
_install
