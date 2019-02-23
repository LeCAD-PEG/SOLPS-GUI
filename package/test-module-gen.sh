STAGING_DIR=/test/dir
INSTALL_DIR=/test/install/dir

cat << EOF > test
#%Module1.0#####################################################################
##
## \$name modulefile
##
set ver [lrange [split [ module-info name ] / ] 1 1 ]
set name [lrange [split [ module-info name ] / ] 0 0 ]
set imas_home ${STAGING_DIR}
set loading [module-info mode load]
set desc [join [read [ open "\$imas_home/etc/modulefiles/\$name/.desc" ] ] ]

conflict blitz
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
EOF