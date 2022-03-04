#!/bin/bash -e
# Prints environment for creating shell source

PACKAGE=environment
source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

${PACKAGE_DIR}/python.sh --env
${PACKAGE_DIR}/pyqt.sh --env
${PACKAGE_DIR}/qt5.sh --env
${PACKAGE_DIR}/gnuplot.sh --env
${PACKAGE_DIR}/pyside6.sh --env

PYTHON_VERSION=$(${PACKAGE_DIR}/python.sh --version)
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
PyQt_VERSION=$(${PACKAGE_DIR}/pyqt.sh --version)
SIP_VERSION=$(${PACKAGE_DIR}/sip.sh --version)
GNUPLOT_WIDGET_VERSION=(${PACKAGE_DIR}/gnuplot-widget.sh --version)

cat <<EOF
SOLPS_GUI_PREFIX=${BUILDROOT}
INSTALL_DIR=\${SOLPS_GUI_PREFIX}/staging

# Setting PYTHONPATH:
PYTHONPATH=\${SOLPS_GUI_PREFIX}/src/widgets:\${PYTHONPATH}
PYTHONPATH=\${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/python/lib.linux-x86_64-${PYTHON_MAINVERSION}:\${PYTHONPATH}
PYTHONPATH=\${INSTALL_DIR}/pyqt5/${PyQt_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages:\${PYTHONPATH}
PYTHONPATH=\${INSTALL_DIR}/sip/${SIP_VERSION}/lib:\${PYTHONPATH}
PYTHONPATH=\${INSTALL_DIR}/gnuplot-widget/${GNUPLOT_WIDGET_VERSION}:\${PYTHONPATH}

# Exporting variables
export PYTHONPATH
export QTDIR=$(${PACKAGE_DIR}/python.sh --prefix)
export QT_QPA_FONTDIR=/usr/share/fonts/dejavu
export QT_QPA_PLATFORM_PLUGIN_PATH=\${QTDIR}/plugins
export PARAVIEW_PREFIX=${BUILDROOT}/staging/paraview/5.4.1
export ids_path=\${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/models/mdsplus
export SOLPSGUI=${BUILDROOT}/src/gui
export PYQTDESIGNERPATH=${BUILDROOT}/src/plugins/designer:\${PYQTDESIGNERPATH}
export IMAS_VERSION=${IMASDD_VERSION}
export UAL_VERSION=${IMASUAL_VERSION}
export PV_PLUGIN_PATH=\${INSTALL_DIR}/ggd_plugin/${GGD_PLUGIN_VERSION}/lib64/paraview-5.8/plugins/ReadUALGGD/

# Setting aliases
alias solps='python3 \${SOLPS_GUI_PREFIX}/src/gui/solps.py'
alias solps_doc='xdg-open \${SOLPS_GUI_PREFIX}/doc/build/html/index.html'
alias solps_help='assistant -collectionFile \${SOLPS_GUI_PREFIX}/doc/build/qthelp/SOLPSGUI.qhc'
alias eirene='python3 \${SOLPS_GUI_PREFIX}/src/widgets/eirene.py'
alias b2='python3 \${SOLPS_GUI_PREFIX}/src/widgets/b2.py'
EOF
