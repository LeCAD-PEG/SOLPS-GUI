#!/bin/bash


APPDIR=staging
DIST_NAME=$(lsb_release -si)
log () {
    # echo "$1"
    #echo -n .
    true
}

if [ ${DIST_NAME} == Debian ]; then
    MPI_COMMAND=mpirun.openmpi
    OPAL_PREFIX=\${DIR}/usr/share/openmpi
    PACKAGES=''
    while IFS='' read -r line || [[ -n "$line" ]]; do
        if [[ "${line}" =~ '#' ]]; then
            continue
        else
            package=$(dpkg-query --show -f '${binary:Package}\n' ${line} \
                        | grep -v i386)
            PACKAGES="${PACKAGES} ${package}"
        fi
    done < appimage/db9_dep_sys_debs.txt
    for package in ${PACKAGES}; do
        # 
        log "Installing ${package}"
        package_list=$(dpkg -L ${package})
        for path in  ${package_list}; do
            if test -d ${path}; then
                log "Installing directory ${APPDIR}${path}"
                install -d ${APPDIR}${path}
            else
                log "Installing file ${APPDIR}${path}"
                cp -a ${path} ${APPDIR}${path}
            fi
        done
    done

elif [ ${DIST_NAME} == CentOS ]; then
    MPI_COMMAND=mpirun
    OPAL_PREFIX=\${DIR}/usr/lib64/openmpi
    while IFS='' read -r line || [[ -n "$line" ]]; do
        if [[ "${line}" =~ '#' ]] ; then
            continue
        else
                package=$(echo ${line})
                PACKAGES="${PACKAGES} ${package}"
        fi
    done < appimage/co7_dep_sys_rpms.txt
    for package in ${PACKAGES}; do
        # 
        package_list=$(rpm -ql ${package})
        if [ $? != 0 ]; then 
        echo "Package ${package} not found"
        continue
        fi
        log "Installing ${package}"
        for path in  ${package_list}; do
            if test -d ${path}; then
                log "Installing directory ${APPDIR}${path}"
                install -d ${APPDIR}${path}
            else
                log "Installing file ${APPDIR}${path}"
                mkdir -p $(dirname ${APPDIR}${path})
                cp -a ${path} ${APPDIR}${path}
            fi
        done
    done    
    
else
    echo "Non supported Linux platform"
    exit 1
fi

# Copy SOLPS-GUI
rm -rf ${APPDIR}/solps-gui
mkdir ${APPDIR}/solps-gui
# Coppy solps.py
cp src/gui/solps.py ${APPDIR}/solps-gui
cp src/gui/solps.ui ${APPDIR}/solps-gui
cp src/gui/preferences.ui ${APPDIR}/solps-gui
cp src/widgets/*.py ${APPDIR}/solps-gui

cp setupenv.sh ${APPDIR}/setupenv.sh
sed -i -e "s|ROOT_DIR=.*|ROOT_DIR=\${DIR}|" \
       -e "s|PYTHONPATH=\${ROOT_DIR}/src/widgets|PYTHONPATH=\${ROOT_DIR}/solps-gui|" \
       -e "s|INSTALL_DIR=.*/staging|INSTALL_DIR=\${ROOT_DIR}|" \
    ${APPDIR}/setupenv.sh
cp ${APPDIR}/setupenv.sh /tmp/test.sh

TMP=/tmp/${USER}

mkdir -p ${TMP}

test -x ${TMP}/appimagetool-x86_64.AppImage || wget -P ${TMP} https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage

chmod +x ${TMP}/*.AppImage

# Preparing AppImage startup file, icon, desktop

LD_DIRS=$(cd ${APPDIR} ; find lib lib64 usr -name \*.so\* | \
          xargs dirname | sort | uniq )

for path in ${LD_DIRS}
    do LD_LIB_PATHS=${LD_LIB_PATHS}:\${DIR}/${path}
done

version=$(git describe)
glibc=$(ldd --version | sed -n "1s/.*\([1-3]\.[0-9][0-9]\).*/\1/p")
APPIMAGE=SOLPS-GUI-${version}-glibc${glibc}-x86_64.AppImage

cat > ${APPDIR}/AppRun <<EOF
#!/bin/bash
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo "Preparing to run SOLPS-GUI \$1 from \${DIR}"

mkdir -p /tmp/\${USER}

export LD_LIBRARY_PATH=${LD_LIB_PATHS}:\${LD_LIBRARY_PATH}

DIR=\${DIR} . \${DIR}/setupenv.sh
python3 \${DIR}/solps-gui/solps.py
EOF

chmod +x ${APPDIR}/AppRun

# Icon
cp src/gui/app_icon.png ${APPDIR}/solps-gui.png

cat > ${APPDIR}/solps-gui.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=SOLPS-GUI
Comment=SOLPS Environment
GenericName=ITER Application
Exec=solps %F
Terminal=false
Type=Application
Icon=solps-gui
Categories=Graphics;Science;Engineering;
StartupNotify=true
X-AppImage-Version=${version}-glibc${glibc}
EOF

ARCH=x86_64 ${TMP}/appimagetool-x86_64.AppImage --no-appstream --comp gzip \
    ${APPDIR} ${TMP}/${APPIMAGE}