#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-develop}
GIT=ssh://git@git.iter.org/bnd/solps-iter.git
SRC_DIR="${STAGING_DIR}/solps-iter/${SOLPS_VERSION}"
INSTALL_DIR=${SRC_DIR}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --recurse-submodules --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    # Check for hostname
    HOSTNAME=$(hostname)

    case ${HOSTNAME} in
        *.iter.org)
        # Do nothing
        ;;
        *)
        # Local machine or basically an UNKNOWN machine, so patch is required
        # to setup the configuration files for UNKNOWN.gfortran
        PATCH_DIR=${BUILDROOT}/src/patches
        echo "Patching solps-iter root"
        patch -p1 < ${PATCH_DIR}/solps-iter.patch

        echo "Patching solps-iter B2.5"
        cd ${SRC_DIR}/modules/B2.5
        patch -p1 < ${PATCH_DIR}/solps-iter-B2.5.patch

        echo "Patching solps-iter Carre"
        cd ${SRC_DIR}/modules/Carre
        patch -p1 < ${PATCH_DIR}/solps-iter-Carre.patch

        echo "Patching solps-iter DivGeo"
        cd ${SRC_DIR}/modules/DivGeo
        patch -p1 < ${PATCH_DIR}/solps-iter-DivGeo.patch

        echo "Patching solps-iter Eirene"
        cd ${SRC_DIR}/modules/Eirene
        patch -p1 < ${PATCH_DIR}/solps-iter-Eirene.patch

        HOST_NAME=UNKNOWN

        ;;
    esac
    cd ${SRC_DIR}
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    GCC_VERSION=$(gcc -dumpversion)
    echo ${GCC_VERSION}

    # Setup LD_LIBRARY_PATH
    # Debian
    LD_LIBRARY_PATH=usr/lib/x86_64-linux-gnu:/usr/lib/gcc/x86_64-linux-gnu/${GCC_VERSION}:${LD_LIBRARY_PATH}
    # CentOS
    LD_LIBRARY_PATH=/usr/lib64/:/usr/lib/gcc/x86_64-redhat-linux/${GCC_VERSION}:${LD_LIBRARY_PATH}

    # Setup PKG_CONFIG_PATH
    PKG_CONFIG_PATH=/usr/lib/pkgconfig:${PKG_CONFIG_PATH}
    # Debian
    PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:${PKG_CONFIG_PATH}
    # CentOS
    PKG_CONFIG_PATH=/usr/lib64/pkgconfig:${PKG_CONFIG_PATH}
    # SolpsITER
    PKG_CONFIG_PATH=${SRC_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}

    # Package PKG_CONFIG_PATH

    if [ -z ${HOST_NAME+x} ]; then
        command="setenv HOST_NAME ${HOST_NAME}\n"
    fi

    command=${command}$(cat <<-EOL
        cd ${SRC_DIR}
        source ${SRC_DIR}/setup.csh gfortran

        rehash
        make listobj listobj_debug
        make depend depend_debug
        make tags
        make carre divgeo b25 eirene b25eirene uinp triang amds sonnet-light
        # make b25eirene_openmp
        make b25eirene_mpi uinp_mpi amds_mpi
EOL
)

    EBVERSIONGGD=${GGD_VERSION} \
    LD_LIBRARY_PATH=${LD_LIBRARY_PATH} \
    PKG_CONFIG_PATH=${PKG_CONFIG_PATH} \
    NCDIR=${STAGING_DIR}/netcdf/${NETCDF_VERSION} \
    MSCL_ROOT=${STAGING_DIR}/mscl/${MSCL_VERSION} \
    GR_ROOT=${STAGING_DIR}/GR/${GR_VERSION} \
    GLI_HOME=${STAGING_DIR}/GLI/${GLI_VERSION} \
    MDSPLUS_ROOT=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION} \
    NCARG_ROOT=${STAGING_DIR}/ncl/${NCL_VERSION}/lib \
    SOLPS_SRC_DIR=${SRC_DIR} \
    tcsh -c "${command}"
    touch ${SRC_DIR}/.built
fi

# Install
# if [ ! -e ${INSTALL_DIR} ]; then
#     install -d ${INSTALL_DIR}
#     make install
# fi


# Generate Modulefile
if [ ! -d ${MODULE_DIR}/solps-iter ]; then
    install -d ${MODULE_DIR}/solps-iter
fi

cat << EOF > ${MODULE_DIR}/solps-iter/${VERSION}
#%Module1.0###################################################################
##
## \$name modulefile
##
conflict solps-iter
if { ! [ is-loaded imas ] } {
    module load imas/${IMASDD_VERSION}/solps
}
if { ![ is-loaded GR/${GR_VERSION} ] } {
    module load GR/${GR_VERSION}
}

if { ![ is-loaded GLI/${GLI_VERSION} ] } {
    module load GLI/${GLI_VERSION}
}

if { ![ is-loaded GGD/${GGD_VERSION} ] } {
    module load GGD/${GGD_VERSION}
}
if { ![ is-loaded ncl/${NCL_VERSION} ] } {
    module load ncl/${NCL_VERSION}
}
if { ![ is-loaded NetCDF/${NETCDF_VERSION} ] } {
    module load NetCDF/${NETCDF_VERSION}
}
if { ![ is-loaded OpenMPI/${OPENMPI_VERSION} ] } {
    module load OpenMPI/${OPENMPI_VERSION}
}
if { ![ is-loaded motif/${MOTIF_VERSION} ] } {
    module load motif/${MOTIF_VERSION}
}
if { ![ is-loaded OpenBLAS/${OPENBLAS_VERSION} ] } {
    module load OpenBLAS/${OPENBLAS_VERSION}
}
setenv MAKE make
setenv SOLPSTOP ${STAGING_DIR}/solps-iter/${SOLPS_VERSION}
set SOLPSTOP ${STAGING_DIR}/solps-iter/${SOLPS_VERSION}
setenv SOLPSWORK \$SOLPSTOP/runs
setenv HOST_NAME UNKNOWN
set HOST_NAME UNKNOWN
setenv COMPILER gfortran
set COMPILER gfortran
setenv DEVICE solps-iter
set DEVICE solps-iter
set TOOLCHAIN \$HOST_NAME.\$COMPILER

prepend-path PYTHONPATH \$SOLPSTOP/lib/python
setenv SOLPSLIB \$SOLPSTOP/lib/\$HOST_NAME.\$COMPILER

setenv SonnetTopDirectory \$SOLPSTOP/modules/Sonnet-Light
setenv DG \$SOLPSTOP/modules/DivGeo

prepend-path PATH \$SOLPSTOP/scripts
prepend-path PATH \$SOLPSTOP/modules/Carre/builds/\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/DivGeo/builds/\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/Eirene/builds/standalone.\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/Eirene/builds/coupled_SOLPS-ITER.\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/B2.5/builds/standalone.\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/B2.5/builds/coupled_SOLPS-ITER.\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/Uinp/builds/\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/Triang/builds/\$TOOLCHAIN
prepend-path PATH \$SOLPSTOP/modules/amds/builds/\$TOOLCHAIN

set-alias sb2  "cd \$SOLPSTOP/modules/B2.5"
set-alias sbb  "cd \$SOLPSTOP/modules/B2.5"
set-alias sei  "cd \$SOLPSTOP/modules/Eirene"
set-alias ssw  "cd \$SOLPSTOP/modules/Sonnet-light"
set-alias sst  "cd \$SOLPSTOP/modules/Triang"
set-alias ssd  "cd \$SOLPSTOP/modules/DivGeo"
set-alias ssc  "cd \$SOLPSTOP/modules/Carre"
set-alias ssu  "cd \$SOLPSTOP/modules/Uinp"
set-alias slib "cd \$SOLPSTOP/lib/\${HOST_NAME}.\${COMPILER}"
set-alias sbr  "cd \$SOLPSTOP/runs"
set-alias scr  "cd \$SOLPSTOP/scripts"
set-alias stop "cd \$SOLPSTOP"

set-alias sdg "cd \$SOLPSTOP/modules/DivGeo/device/\$DEVICE"
set-alias ssf "cd \$SOLPSTOP/modules/DivGeo/device/\$DEVICE"

set-alias xyplot "plot xyplot"
set-alias xyplot2 "plot xyplot2"
set-alias xyplot3 "plot xyplot3"
set-alias xyplot4 "plot xyplot4"
set-alias xyplot5 "plot xyplot5"
set-alias xyplot6 "plot xyplot6"
set-alias xyplot7 "plot xyplot7"
set-alias xyplot8 "plot xyplot8"
set-alias xyplot8 "plot xyplot8"
set-alias xyplot9 "plot xyplot9"
set-alias xlyplot "plot xlyplot"
set-alias xlyplot2 "plot xlyplot2"
set-alias xlyplot3 "plot xlyplot3"
set-alias xlyplot4 "plot xlyplot4"
set-alias xlyplot5 "plot xlyplot5"
set-alias xlyplot6 "plot xlyplot6"
set-alias xlyplot7 "plot xlyplot7"
set-alias xlyplot8 "plot xlyplot8"
set-alias xlyplot8 "plot xlyplot8"
set-alias xlyplot9 "plot xlyplot9"
set-alias xylplot "plot xylplot"
set-alias xylplot2 "plot xylplot2"
set-alias xylplot3 "plot xylplot3"
set-alias xylplot4 "plot xylplot4"
set-alias xylplot5 "plot xylplot5"
set-alias xylplot6 "plot xylplot6"
set-alias xylplot7 "plot xylplot7"
set-alias xylplot8 "plot xylplot8"
set-alias xylplot8 "plot xylplot8"
set-alias xylplot9 "plot xylplot9"
set-alias xlylplot "plot xlylplot"
set-alias xlylplot2 "plot xlylplot2"
set-alias xlylplot3 "plot xlylplot3"
set-alias xlylplot4 "plot xlylplot4"
set-alias xlylplot5 "plot xlylplot5"
set-alias xlylplot6 "plot xlylplot6"
set-alias xlylplot7 "plot xlylplot7"
set-alias xlylplot8 "plot xlylplot8"
set-alias xlylplot8 "plot xlylplot8"
set-alias xlylplot9 "plot xlylplot9"

set-alias   set_debug  "source \$SOLPSTOP/SETUP/debug"
set-alias unset_debug  "source \$SOLPSTOP/SETUP/nodebug"
set-alias   set_openmp "source \$SOLPSTOP/SETUP/openmp"
set-alias unset_openmp "source \$SOLPSTOP/SETUP/noopenmp"
set-alias   set_mpi    "source \$SOLPSTOP/SETUP/mpi"
set-alias unset_mpi    "source \$SOLPSTOP/SETUP/nompi"
set-alias   set_ig     "source \$SOLPSTOP/SETUP/ig"
set-alias unset_ig     "source \$SOLPSTOP/SETUP/noig"
EOF