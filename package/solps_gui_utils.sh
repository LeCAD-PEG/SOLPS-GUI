#!/bin/sh
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}

if [ -z ${PACKAGE+x} ]; then
    echo "PACKAGE is not set"
    return
else
    echo "PACKAGE: ${PACKAGE}"
fi

export STAGING_DIR=${BUILDROOT}/staging

PKG_DIRS=${PKG_DIRS:-3rd_packages}
export BUILD_DIR=${BUILDROOT}/${PKG_DIRS}/build
export SOURCE_DIR=${BUILDROOT}/${PKG_DIRS}/source
export DOWNLOAD_DIR=${BUILDROOT}/${PKG_DIRS}/download
LOG_DIR=${BUILDROOT}/LOGS

export MAKE_JOBS=${MAKE_JOBS:-$(nproc)}
# Variables that control outputs.
export PACKAGE_INSTALL_DIR=${STAGING_DIR}/${PACKAGE}/${VERSION}
export PACKAGE_SOURCE_DIR=${SOURCE_DIR}/${PACKAGE}-${VERSION}
export PACKAGE_BUILD_DIR=${BUILD_DIR}/${PACKAGE}-${VERSION}
export PACKAGE_LOG_DIR=${LOG_DIR}/${PACKAGE}-${VERSION}

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
    fi
    _log "Sources for ${PACKAGE} unpacked to ${PACKAGE_SOURCE_DIR}"
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
    # 1 - git link
    # 2 - branch
    _log "Cloning ${PACKAGE}, branch ${VERSION}. Log file: ${PACKAGE_LOG_DIR}/clone"
    if [ ! -d ${PACKAGE_SOURCE_DIR} ]; then
        git clone $1 --single-branch --branch $2 ${PACKAGE_SOURCE_DIR} &> ${PACKAGE_LOG_DIR}/clone
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
            _log "Trying to create configure with autogen.sh. Log file: ${PACKAGE_LOG_DIR}/autogen.sh.log"
            ./autogen.sh &> ${PACKAGE_LOG_DIR}/autogen.sh.log
        elif [ -e ${PACKAGE_SOURCE_DIR}/autogen.pl ]; then
            _log "Trying to create configure with autogen.pl. Log file: ${PACKAGE_LOG_DIR}/autogen.pl.log"
            ./autogen.pl &> ${PACKAGE_LOG_DIR}/autogen.pl.log
        else
            # Last measure
            _log "Trying to create configure with autoreconf. Log file: ${PACKAGE_LOG_DIR}/autoreconf.log"
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
        env -v ${2} ${PACKAGE_SOURCE_DIR}/configure --prefix=${PACKAGE_INSTALL_DIR} ${1} &> ${PACKAGE_LOG_DIR}/configure
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
}

function _configure_custom {
    # Same as _configure, except when the configure script is located somewhere
    # else in the sources. Also runs in the ${PWD} directory so you have change to
    # the directory you wish to call configure.
    # Arguments:
    # 1 - Path to configure
    # 2 - Configure options
    # 3 - Additional flags before configure
    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/configure"
    _log "$3 ${1} --prefix=${PACKAGE_INSTALL_DIR} $2"

    if [ ! -e ${PWD}/.configured ]; then
        env -v ${3} ${1} --prefix=${PACKAGE_INSTALL_DIR} ${2} &> ${PACKAGE_LOG_DIR}/configure
        touch ${PWD}/.configured
    fi
}

function _python_configure {
    # Calls python setup.py configure.
    # Arguments:
    # 1 - configure options
    # 2 - Additional flags before configure

    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/python_configure"
    _log "$2 python3 setup.py config $1"
    cd ${PACKAGE_SOURCE_DIR}
    if [ ! -e ${PACKAGE_SOURCE_DIR}/.configured ]; then
        env -v ${2} python3 setup.py config $1 &> ${PACKAGE_LOG_DIR}/python_configure
        touch ${PACKAGE_SOURCE_DIR}/.configured
    fi
}

function _python_configure2 {
    # Calls python setup.py configure.
    # Arguments:
    # 1 - configure options
    # 2 - Additional flags before configure

    _log "Configuring ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/python_configure"
    _log "$2 python3 setup.py configure $1"
    cd ${PACKAGE_SOURCE_DIR}
    if [ ! -e ${PACKAGE_SOURCE_DIR}/.configured ]; then
        env -v ${2} python3 setup.py configure ${1} &> ${PACKAGE_LOG_DIR}/python_configure
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
        env -v ${2} ${PACKAGE_SOURCE_DIR}/bootstrap --prefix=${PACKAGE_INSTALL_DIR} ${1} &> ${PACKAGE_LOG_DIR}/cmake
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
}

function _cmake {
    # Calls CMake. CMake should be called form BUILD directory.
    # Arguments:
    # 1 - CMake options
    # 2 - PreCMake options
    # 3 - Optional location of CMakeLists.txt

    if [ -z "${3}" ]; then
        SOURCE_DIR=${PACKAGE_SOURCE_DIR}
    else
        SOURCE_DIR=${3}
    fi

    _log "CMake configure for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/cmake"
    _log "$2" cmake $1 -DCMAKE_INSTALL_PREFIX=${PACKAGE_INSTALL_DIR}
    cd ${PACKAGE_BUILD_DIR}
    if [ ! -e ${PACKAGE_BUILD_DIR}/.configured ]; then
        env -v $2 cmake ${SOURCE_DIR} $1 -DCMAKE_INSTALL_PREFIX=${PACKAGE_INSTALL_DIR} &> ${PACKAGE_LOG_DIR}/cmake
        touch ${PACKAGE_BUILD_DIR}/.configured
    fi
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
        touch ${PWD}/.built
    fi
}

function _python_make {
    # Calls python setup.py build
    # Arguments
    # 1 - make options
    # 2 - PreMake flag
    _log "Calling make for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/python_build"
    _log "$2 python3 setup.py build $1"

    if [ ! -e ${PWD}/.built ]; then
        env -v $2 python3 setup.py build $1 &> ${PACKAGE_LOG_DIR}/python_build
    fi
}

function _install {
    # Calls make.
    # Arguments
    # 1 - Make options
    # 2 - Pre-make options
    _log "Calling make install for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/install"
    if [ ! -d ${PACKAGE_INSTALL_DIR} ]; then
        _log "make install ${1}"
        env -v ${2} make install ${1} &> ${PACKAGE_LOG_DIR}/install
    fi
}

function _install_custom {
    # Calls custom script to install.
    # Arguments
    # 1 - Path to executable
    # 2 - Options for executable
    # 3 - Pre-options
    _log "Calling custom install for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/install_custom"
    if [ ! -d ${PACKAGE_INSTALL_DIR} ]; then
        _log "${3} ${1} ${2}"
        env -v ${3} ${1} ${2} &> ${PACKAGE_LOG_DIR}/install_custom
    fi
}

function _python_install {
    # Calls python setup.py install.
    # Arguments
    # 1 - Options
    _log "Calling python setup.py install for ${PACKAGE}. Log file: ${PACKAGE_LOG_DIR}/python_install"
    cd ${PACKAGE_SOURCE_DIR}
    env -v python setup.py build install $1 &> ${PACKAGE_LOG_DIR}/python_install
}

function _createDirs {
    # Creates Download, Source, Build and Install directory.
    _log "Creating directories"
    mkdir -p ${BUILD_DIR} ${SOURCE_DIR} ${DOWNLOAD_DIR} ${LOG_DIR} ${PACKAGE_LOG_DIR} ${PACKAGE_BUILD_DIR}
}

_createDirs
