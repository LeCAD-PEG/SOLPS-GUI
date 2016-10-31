s/\\ :sub:`\([0-9A-Za-z ]\)`/-\1/g
s/\\ //g
s/:math:`\([^`]*\)`/``\1``/g
s/\\-/-/g
s/\\_/_/g
s/ / /g
s/“/"/g
s/”/"/g
s/\[Fig. \([a-zA-Z0-9:`_-]\{1,\}\)\]/:numref:`\1`/g
#/\[fig:[a-zA-Z0-9_`:]*/y/:/-/
s/Fig. \[\([a-zA-Z0-9:-]\{1,\}\)\]/:numref:`\1`/g
s/fig:/fig-/g
s/figure:: \(.*\)/figure:: \1.*/
