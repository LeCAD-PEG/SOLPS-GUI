#!/bin/sh
#
# This script creates IMAS single Python2 and Python3 virtual environment in
# user's file space. User can then manage Python packages with pip2 and pip3
# commands.
#
# Use source ~/imas-python/setupenv.sh
#
# Instead of default symlinks one can choose to copy Pythons completely.
#
# By setting the PYTHONHOME environment variable many versions of Python
# can be used at the same time. For that all Pythons need to be rebased
# into the same --prefix=${PYTHONHOME}
# For multiple versions sys.prefix and sys.base_prefix needs to be the same!
# See https://docs.python.org/3/library/sys.html#sys.prefix

if [ -n "$1" ]; then 
    VENV=$1 
    if [ -n "${VENV##/*}" ]; then
        echo "Absolute path required (e.g. $0 \$PWD/myvenv)"
        exit 1
    fi
else
    VENV=${HOME}/imas-python
fi
USE_SYMLINKS_INSTEAD_OF_COPY=yes

module purge
module use -a ~kosl/imas/etc/modulefiles
module load imas/3.7.3/ual/develop pyqt/5.7-qt-5.7.0-python-3.5.2 

if [ "${PYTHONHOME}" = "${VENV}" ]; then # we can not rebase itself
    export -n PYTHONHOME # therefore we try to rebase from system again
fi

set -e

rebase_python() # major, minor
{
    PREFIX=$(python$1.$2 -c 'import sys; print(sys.prefix)')

    if [ ${USE_SYMLINKS_INSTEAD_OF_COPY} = yes ]
        then ln -sf ${PREFIX}/bin/python$1.$2 ${VENV}/bin
        else cp -a ${PREFIX}/bin/python$1.$2 ${VENV}/bin
    fi
    ln -sf python$1.$2 ${VENV}/bin/python$1
    ln -sf python$1 ${VENV}/bin/python
    # Change shebang for pip and easy_install scripts
    for script in ${PREFIX}/bin/pip* ${PREFIX}/bin/easy_install* ; do
      cmd=${script##*/}
      sed -e "1c#!${VENV}/bin/python$1.$2" ${script} > \
          ${VENV}/bin/${cmd}
      chmod 755 ${VENV}/bin/${cmd}
    done

    # Symlink or copy includes, share, system libraries and site packages
    install -d ${VENV}/lib
    install -d ${VENV}/include
    install -d ${VENV}/share
    find ${PREFIX}/lib ${PREFIX}/include ${PREFIX}/share -print0 | \
    while IFS= read -r -d '' file
      do
        without_prefix="${file#${PREFIX}/}"
        if test -d "${file}"
            then install -d "${VENV}/${without_prefix}/"
        elif test -L "${file}"; then
            link=$(readlink "${file}")
            link_without_prefix="${link#${PREFIX}/}"
            ln -sf "${link_without_prefix}" "${VENV}/${without_prefix}"
        else
            if [ ${USE_SYMLINKS_INSTEAD_OF_COPY} = yes ]
                then ln -sf "${file}" "${VENV}/${without_prefix}"
                else cp --archive "${file}" "${VENV}/${without_prefix}"
            fi
        fi
    done
    if test -d ${PREFIX}/qt
        then ln -sf ${PREFIX}/qt ${VENV}
    fi
}

rebase_imas()
{
  if [ ${USE_SYMLINKS_INSTEAD_OF_COPY} = yes ]; then
    ln -sf ${IMAS_PREFIX}/python2.7 ${VENV}/lib/python2.7/site-packages/imas
    ln -sf ${IMAS_PREFIX}/python3.5 ${VENV}/lib/python3.5/site-packages/imas
  else
    install -d ${VENV}/lib/python2.7/site-packages/imas
    install -d ${VENV}/lib/python3.5/site-packages/imas
    cp -a ${IMAS_PREFIX}/python2.7/* ${VENV}/lib/python2.7/site-packages/imas
    cp -a ${IMAS_PREFIX}/python3.5/* ${VENV}/lib/python3.5/site-packages/imas
  fi
}

rm -rf ${VENV}
install -d ${VENV}/bin
cat  > ${VENV}/setupenv.sh <<EOF
# Source this in bash to enable IMAS Python 2 and 3 in user space
module use -a ~kosl/imas/etc/modulefiles
module load imas/3.7.3/ual/develop # ENV for Python3 w/ PyQt5 is explicit below
export PYTHONHOME=${VENV}
export QTDIR=\${PYTHONHOME}/qt/5.7.0
export PATH=\${PYTHONHOME}/bin:\${QTDIR}/bin:\${PATH}
export LD_LIBRARY_PATH=\${PYTHONHOME}/lib:\${QTDIR}/lib:\${LD_LIBRARY_PATH}
export MANPATH=\${PYTHONHOME}/share/man:\${MANPATH}
export PKG_CONFIG_PATH=\${PYTHONHOME}/lin/pkgconfig:\${QTDIR}/lib/pkgconfig:\${PKG_CONFIG_PATH}
export CPATH=\${PYTHONHOME}/include:\${QTDIR}/include:\${CPATH}
# Remove PYTHONPATH from IMAS and use it only for custom Python3 widgets
# that will never clash with Python2
export PYTHONPATH=/home/ITER/kosl/solps-gui/src/widgets
EOF

# Last rebase is also default for python, pip, and easy_install commands
rebase_python 3 5
rebase_python 2 7
#set -ex
rebase_imas # must have all above ${IMAS_PREFIX}/pythonX.Y IMAS libraries
