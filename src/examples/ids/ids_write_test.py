#! /usr/bin/env python

import imas
#import numpy
import os
import sys
import pwd

def write_ids():
    time = 1
    interp = 1
    treeName = 'ids'

    imas_obj = imas.ids(shot, run, shot, run)


    #imas_obj.create() #Create the data entry
    imas_obj.create_env(user, tokamak, version)

    if imas_obj.isConnected():
        print 'Creation of data entry OK!'
    else:
        print 'Creation of data entry FAILED!'

        sys.exit()

    imas_obj.edge_profiles.profiles_1d.resize(1)
    imas_obj.edge_profiles.ggd.resize(1)
    imas_obj.edge_profiles.putNonTimed()

    imas_obj.close()

if __name__ == '__main__':

    user = pwd.getpwuid( os.getuid() )[ 0 ]
    shot, run, tokamak, version = 16151, 1001, "aug", "3.4.0"

    write_ids()

