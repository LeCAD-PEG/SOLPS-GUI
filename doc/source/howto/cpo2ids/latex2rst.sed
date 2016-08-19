/\[fig:[a-zA-Z0-9_]*/y/_/-/
s/:math:`\([^`]*\)`/``\1``/g
s/\\-/-/g
s/\\_/_/g
s/\[fig:\([a-zA-z_-]\{1,\}\)\]/:num:`Fig. #\1`/g
s/Fig. :num:/:num:/g
s/figure:: \(.*\)/figure:: images\/\1.png/
