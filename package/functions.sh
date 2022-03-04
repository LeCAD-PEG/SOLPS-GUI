#!/bin/bash

trap 'ec=$?; ((ec != 0)) && echo -e "\e[31mExited with failure: $ec\e[m"' EXIT

BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}

if [ -z ${PACKAGE+x} ]; then
    >&2 echo "PACKAGE is not set"
    return
fi

export STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
export BUILD_DIR=${BUILD_DIR:-${BUILDROOT}/build}
export SOURCE_DIR=${BUILD_DIR}/source
export DOWNLOAD_DIR=${BUILDROOT}/download
export PACKAGE_DIR=${BUILDROOT}/package
LOG_DIR=${BUILDROOT}/LOGS

LOAD_AVG=$(awk '{print int($2)}' /proc/loadavg)
export MAKE_JOBS=${MAKE_JOBS:-$(nproc --ignore=${LOAD_AVG})}
# Variables that control outputs.
export PACKAGE_INSTALL_DIR=${STAGING_DIR}/${PACKAGE}/${VERSION}
export PACKAGE_SOURCE_DIR=${SOURCE_DIR}/${PACKAGE}-${VERSION}
export PACKAGE_BUILD_DIR=${BUILD_DIR}/${PACKAGE}-${VERSION}
export PACKAGE_LOG_DIR=${LOG_DIR}/${PACKAGE}-${VERSION}

test "$1" == "--prefix" && echo ${PACKAGE_INSTALL_DIR} && exit
test "$1" == "--version" && echo ${VERSION} && exit
test "$1" == "--rebuild" && rm -rf ${PACKAGE_SOURCE_DIR} \
                               ${PACKAGE_BUILD_DIR} ${PACKAGE_INSTALL_DIR}
test "$1" == "--clean" && rm -rf ${PACKAGE_SOURCE_DIR} \
                               ${PACKAGE_BUILD_DIR} ${PACKAGE_INSTALL_DIR}
if test "$1" == "--env" ; then # e.g. eval $(build/python.sh --env)
  echo "export PATH=${PACKAGE_INSTALL_DIR}/bin:\${PATH}"
  echo "export LD_LIBRARY_PATH=${PACKAGE_INSTALL_DIR}/lib:\${LD_LIBRARY_PATH}"
  test "$2" == "--pkg" && echo "export PKG_CONFIG_PATH=${PACKAGE_INSTALL_DIR}/lib/pkgconfig:\${PKG_CONFIG_PATH}"
  exit 0
fi
    

if test "$1" == "--help"
   then cat <<EOF
Usage: [env [VERSION=version]] $0 [options]
   Options:
     --rebuild Clears source, build, install directory and builds from scratch
     --clean   Removes source, build, and install directory
     --env     Echoes instalation environment variables for PATH and LD_LIBRARY_PATH
               Example usage: eval \$($0 --env)
     --env --pkg  Echoes PKG_CONFIG_PATH export in addition
     --version Echoes package build version
     --prefix  Echoes package installation prefix 
EOF
   exit 0
fi

test -d ${PACKAGE_INSTALL_DIR} && echo Using ${PACKAGE}@${VERSION} && exit 0

DOWNLOAD_CMD=${DOWNLOAD_CMD:-wget -q --show-progress}
EXTRACT_COMMAND=${EXTRACT_COMMAND:-tar xf}

_VERBOSE=${_VERBOSE:-1}

function _log {
    if [ ${_VERBOSE} -eq 1 ]; then
        echo $@
    fi
}

function _downloadFileAndUnpack {
    # Download file and unpack it. Downloaded sources should be stored to
    # download and unpacked in source
    # Arguments:
    # 1 - Web link
    # 2 - Output
    # 3 - Extract even if destination directory exists

    cd ${DOWNLOAD_DIR}
    if [ ! -f $2 ]; then
        _log "Downloading $1 to $2"
        ${DOWNLOAD_CMD} -O $2 $1
    fi
    LOCATION_NAME=$(tar tf $2 | head -1 | sed -e 's/\/.*//')

    cd ${SOURCE_DIR}
    if [ ! -d ${PACKAGE_SOURCE_DIR} ]; then
        if [ ! -d ${LOCATION_NAME} ]; then
            _log "Unpacking ${DOWNLOAD_DIR}/$2"
            ${EXTRACT_COMMAND} ${DOWNLOAD_DIR}/$2
        fi
        if [ ! -d ${PACKAGE_SOURCE_DIR} ]; then
            _log "Finally renaming ${LOCATION_NAME} to ${PACKAGE_SOURCE_DIR}"
            mv ${LOCATION_NAME} ${PACKAGE_SOURCE_DIR}
        fi
        _log "Sources for ${PACKAGE} unpacked to ${PACKAGE_SOURCE_DIR}"
    else
        _log "Directory ${PACKAGE_SOURCE_DIR} already exists!"
        _log "Skipping unpacking of ${DOWNLOAD_DIR}/$2"
    fi
}

function _copyLocalDirectory {
    # Copy sources from local directory.
    # Arguments:
    # 1 - location
    cd ${SOURCE_DIR}
    if [ -d ${PACKAGE_SOURCE_DIR} ]; then
        rm -rf ${PACKAGE_SOURCE_DIR}
    fi
    cp -r ${1} ${PACKAGE_SOURCE_DIR}
    _log "Sources for ${PACKAGE} unpacked to ${PACKAGE_SOURCE_DIR}"
}

function _gitCloneSingleBranch {
    # Clone a repository, or if it was cloned checkout the branch
    # Arguments:
    # 1 - remote URL
    # 2 - branch
    # git clone [remote-url] --branch [name] --single-branch [folder]
    if [ ! -d ${PACKAGE_SOURCE_DIR} ]; then
        _log "Cloning ${PACKAGE}, branch ${VERSION},"
        _log "Log file: ${PACKAGE_LOG_DIR}/clone"
#        git clone --branch $2 --recursive $1 ${PACKAGE_SOURCE_DIR} \
        git clone $1 --branch $2 --recursive --single-branch  ${PACKAGE_SOURCE_DIR} \
            &> ${PACKAGE_LOG_DIR}/clone
    fi
}

function _applyPatchIfNecessary {
    # Applies a provided patch if it is necessary
    # Arguments:
    # 1 - Path to patch
    # 2 - Additionally path to directory
    _log "Patching ${PACKAGE} with ${1}"
    if [ -z "${2}" ]; then
        cd ${PACKAGE_SOURCE_DIR}
        _log "Patching in ${PACKAGE_SOURCE_DIR}"
    else
        _log "Patching in $2"
        cd $2
    fi

    if patch -p1 -N --dry-run --silent < ${1} 2>/dev/null; then
        patch -p1 < ${1}
    fi
}

function _autoreconf {
    # Calls autoreconf in source directory.
    _log "Auto-reconf. Log file: ${PACKAGE_LOG_DIR}/autoreconf"
    cd ${PACKAGE_SOURCE_DIR}
    if [ ! -e ${PACKAGE_SOURCE_DIR}/.autoreconfigured ]; then
        autoreconf -i -s &> ${PACKAGE_LOG_DIR}/autoreconf
        touch ${PACKAGE_SOURCE_DIR}/.autoreconfigured
    fi
}

function _prepare_configure {
    # In case of reconfigure call this function.
    if [ ! -e ${PACKAGE_SOURCE_DIR}/configure ]; then
        cd ${PACKAGE_SOURCE_DIR}
        # See if there is autogen.sh
        if [ -e ${PACKAGE_SOURCE_DIR}/autogen.sh ]; then
            _log "Trying to create configure with autogen.sh."
            _log "Log file: ${PACKAGE_LOG_DIR}/autogen.sh.log"
            ./autogen.sh &> ${PACKAGE_LOG_DIR}/autogen.sh.log
        elif [ -e ${PACKAGE_SOURCE_DIR}/autogen.pl ]; then
            _log "Trying to create configure with autogen.pl."
            _log "Log file: ${PACKAGE_LOG_DIR}/autogen.pl.log"
            ./autogen.pl &> ${PACKAGE_LOG_DIR}/autogen.pl.log
        else
            # Last measure
            _log "Trying to create configure with autoreconf."
            _log "Log file: ${PACKAGE_LOG_DIR}/autoreconf.log"
            autoreconf -s -i &> ${PACKAGE_LOG_DIR}/autoreconf.log
        fi
    fi

}

function _configure {
    # Calls configure. Configure should be called form BUILD directory.
    # Arguments:
    # 1 - Configure options
    # 2 - Additional flags before configure
    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/configure"
    _log "$2 ${PACKAGE_SOURCE_DIR}/configure --prefix=${PACKAGE_INSTALL_DIR} $1"

    cd ${PACKAGE_BUILD_DIR}

    if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
        rm -rf ${PACKAGE_BUILD_DIR}/*
        env -v ${2} ${PACKAGE_SOURCE_DIR}/configure \
            --prefix=${PACKAGE_INSTALL_DIR} ${1} &> \
            ${PACKAGE_LOG_DIR}/configure
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
}

function _configure_cmake {
    # Calls configure with cmake.
    # Configure should be called form BUILD directory.
    # Arguments:
    # 1 - Configure options
    # 2 - Additional flags before configure
    
    cd ${PACKAGE_BUILD_DIR}
 
    if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
         export PATH=$(${PACKAGE_DIR}/cmake.sh --prefix)/bin:${PATH}
         _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/configure"
         _log "$2 ${PACKAGE_SOURCE_DIR}/configure --prefix=${PACKAGE_INSTALL_DIR} $1"

         _log "Using $(cmake --version)"
        rm -rf ${PACKAGE_BUILD_DIR}/*
        env -v ${2} ${PACKAGE_SOURCE_DIR}/configure \
            --prefix=${PACKAGE_INSTALL_DIR} ${1} &> \
            ${PACKAGE_LOG_DIR}/configure
        touch ${PACKAGE_BUILD_DIR}/.configured
    else
        _log "Skipping ${PACKAGE} configure."
    fi
}

function _configure_qt {
    # Calls configure with cmake.
    # Configure should be called form BUILD directory.
    # Arguments:
    # 1 - Configure options
    # 2 - Configure type: release/debug
    
    cd ${PACKAGE_BUILD_DIR}

    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/configure"
    _log "PACKAGE_BUILD_DIR: ${PACKAGE_BUILD_DIR}"
    _log "${PACKAGE_SOURCE_DIR}/configure --prefix=${PACKAGE_INSTALL_DIR}/${1} $2"
    _log "Using $(cmake --version)"

    rm -rf ${PACKAGE_BUILD_DIR}/*
    ${PACKAGE_SOURCE_DIR}/configure --prefix=${PACKAGE_INSTALL_DIR}/${1} ${2} \
        &> ${PACKAGE_LOG_DIR}/configure
}

function _configure_custom {
    # Same as _configure, except when the configure script is located somewhere
    # else in the sources. Also runs in the ${PWD} directory so you have
    # change to the directory you wish to call configure.
    # Arguments:
    # 1 - Path to configure
    # 2 - Configure options
    # 3 - Additional flags before configure
    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/configure"
    _log "$3 ${1} --prefix=${PACKAGE_INSTALL_DIR} $2"

    if [ ! -e ${PWD}/.configured ]; then
        env -v ${3} ${1} --prefix=${PACKAGE_INSTALL_DIR} ${2} \
            &> ${PACKAGE_LOG_DIR}/configure
        touch ${PWD}/.configured
    fi
}

function _python_configure {
    # Calls python setup.py configure.
    # Arguments:
    # 1 - configure options
    # 2 - Additional flags before configure

    _log "Configuring ${PACKAGE}."
    _log "Log file: ${PACKAGE_LOG_DIR}/python_configure"
    _log "$2 python3 setup.py config $1"
    cd ${PACKAGE_SOURCE_DIR}
    if [ ! -e ${PACKAGE_SOURCE_DIR}/.configured ]; then
        env -v ${2} python3 setup.py config $1 \
            &> ${PACKAGE_LOG_DIR}/python_configure
        touch ${PACKAGE_SOURCE_DIR}/.configured
    fi
}

function _python_configure2 {
    # Calls python setup.py configure.
    # Arguments:
    # 1 - configure options
    # 2 - Additional flags before configure

    _log "Configuring ${PACKAGE}."
    _log "Log file: ${PACKAGE_LOG_DIR}/python_configure"
    _log "$2 python3 setup.py configure $1"
    cd ${PACKAGE_SOURCE_DIR}
    if [ ! -e ${PACKAGE_SOURCE_DIR}/.configured ]; then
        env -v ${2} python3 setup.py configure ${1} \
            &> ${PACKAGE_LOG_DIR}/python_configure
        touch ${PACKAGE_SOURCE_DIR}/.configured
    fi
}

function _python_configure_custom {
    # Calls python configure.py.
    # Arguments:
    # 1 - python file to call
    # 2 - arguments
    # 3 - Additional flags before configure
    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/python_configure"
    _log "$3 python3 setup.py configure $1 $2"
    cd ${PACKAGE_BUILD_DIR}
    if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
        env -v ${3} python3 ${1} ${2} &> ${PACKAGE_LOG_DIR}/python_configure
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
}

function _cmake_bootstrap {
    # Calls CMake. CMake should be called form BUILD directory.
    # Arguments:
    # 1 - CMake options
    # 2 - PreCMake options
    # 3 - Optional location of CMakeLists.txt
    _log "CMake bootrap for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/cmake"
    _log "$2" ${PACKAGE_SOURCE_DIR}/bootstrap --prefix=${PACKAGE_INSTALL_DIR} $1
    cd ${PACKAGE_BUILD_DIR}
    if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
        env -v ${2} ${PACKAGE_SOURCE_DIR}/bootstrap \
            --prefix=${PACKAGE_INSTALL_DIR} ${1} &> ${PACKAGE_LOG_DIR}/cmake
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
}

function _cmake {
    # Calls CMake. CMake should be called form BUILD directory.
    # Arguments:
    # 1 - CMake options
    # 2 - PreCMake options
    # 3 - Optional location of CMakeLists.txt

    SOURCE_DIR=${PACKAGE_SOURCE_DIR}

    (
        export PATH=$(${PACKAGE_DIR}/cmake.sh --prefix)/bin:${PATH}
        _log "Using CMake version $(cmake --version)"
        _log "CMake configure for ${PACKAGE}"
        _log "Log file: ${PACKAGE_LOG_DIR}/cmake"
        _log "$2" cmake $1 -DCMAKE_INSTALL_PREFIX=${PACKAGE_INSTALL_DIR}
        cd ${PACKAGE_BUILD_DIR}
        if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
            env -v $2 cmake ${SOURCE_DIR} $1 \
                -DCMAKE_INSTALL_PREFIX=${PACKAGE_INSTALL_DIR} \
                &> ${PACKAGE_LOG_DIR}/cmake
            touch ${PACKAGE_BUILD_DIR}/.configured
        fi
    )
}

function _make {
    # Calls make.
    # Arguments
    # 1 - Make options
    # 2 - PreMake Flag

    _log "Calling make for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/build"
    _log "$2 make $1"
    # The reason why PWD is used is because some packages have to be built in
    # source directories as they do not have a build system.
    if [ ! -e ${PWD}/.built ]; then
        # printenv &> ${PACKAGE_LOG_DIR}/build_env
        env -v $2 make $1 &> ${PACKAGE_LOG_DIR}/build
        test $? == 0 && echo Build OK || echo Build failed
        touch ${PWD}/.built
    fi
}

function _cmake_build {
    # Calls cmake to build.
    # Arguments
    # 1 - Make options
    # 2 - PreMake Flag

    if [ ! -e ${PACKAGE_BUILD_DIR}/.built ]; then
      (
          export PATH=$(${PACKAGE_DIR}/cmake.sh --prefix)/bin:${PATH}
          _log "Calling CMake build for ${PACKAGE}."
          _log "Using $(cmake --version)"
          _log "Log file: ${PACKAGE_LOG_DIR}/build"
          _log "$2 cmake --build ${PACKAGE_BUILD_DIR} $1"
          
        # printenv &> ${PACKAGE_LOG_DIR}/build_env
         env -v $2 cmake --build ${PACKAGE_BUILD_DIR} $1 \
             &> ${PACKAGE_LOG_DIR}/build
         test $? == 0 && echo Installed OK || echo Build failed
         touch ${PACKAGE_BUILD_DIR}/.built
      )
    fi
}

function _python_make {
    # Calls python setup.py build
    # Arguments
    # 1 - make options
    # 2 - PreMake flag
    _log "Calling make for ${PACKAGE}."
    _log "Log file: ${PACKAGE_LOG_DIR}/python_build"
    _log "$2 python3 setup.py build $1"

    if [ ! -e ${PWD}/.built ]; then
        env -v $2 python3 setup.py build $1 &> ${PACKAGE_LOG_DIR}/python_build
        test $? == 0 && echo Installed OK || echo Build failed
    fi
}

function _install {
    # Calls make.
    # Arguments
    # 1 - Make options
    # 2 - Pre-make options
    if [ ! -d ${PACKAGE_INSTALL_DIR} ]; then
        _log "Calling make install for ${PACKAGE}."
        _log "Log file: ${PACKAGE_LOG_DIR}/install"
        _log "make install ${1}"
        env -v ${2} make install ${1} &> ${PACKAGE_LOG_DIR}/install
        test $? == 0 && echo Installed OK || echo Installation failed
    fi
}

function _cmake_install {
    # Calls cmake.
    # Arguments
    # 1 - Make options
    # 2 - Pre-make options
    if [ ! -d ${PACKAGE_INSTALL_DIR} ]; then
      (
          _log "Calling cmake install for ${PACKAGE}."
          _log "Log file: ${PACKAGE_LOG_DIR}/install"
          export PATH=$(${PACKAGE_DIR}/cmake.sh --prefix)/bin:${PATH}
          _log "cmake --install ${PACKAGE_BUILD_DIR} ${1}"
          env -v ${2} cmake --install ${PACKAGE_BUILD_DIR} ${1} \
              &> ${PACKAGE_LOG_DIR}/install
          test $? == 0 && echo Installed OK || echo Installation failed
      )
    fi
}

function _python_install {
    # Calls python setup.py install.
    # Arguments
    # 1 - Options
    _log "Calling python setup.py install for ${PACKAGE}."
    _log "Log file: ${PACKAGE_LOG_DIR}/python_install"
    cd ${PACKAGE_SOURCE_DIR}
    env -v python setup.py build install $1 &> ${PACKAGE_LOG_DIR}/python_install
    test $? == 0 && echo Installed OK || echo Build failed
}

function _prerequisites {
    for package in $*
    do ${PACKAGE_DIR}/${package}.sh
    done 
}

function _createDirs {
    # Creates Download, Source, Build and Install directory.
    #_log "Creating directories"
    mkdir -p ${BUILD_DIR} ${SOURCE_DIR} ${DOWNLOAD_DIR} ${LOG_DIR} \
          ${PACKAGE_LOG_DIR} ${PACKAGE_BUILD_DIR}
}

_createDirs
