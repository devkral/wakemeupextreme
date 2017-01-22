#! /usr/bin/env python3

from wakemeupextreme import WakeMeUpExtreme
from wakemeupextreme import LED

import sys
import os

def main():
    if len(sys.argv) == 1:
        import appdirs
        udir = appdirs.user_config_dir()
        os.makedirs(udir, 0o770, exist_ok=True)
        uconfig = os.path.join(udir, "WakeMeUpExtreme.ini")
        ret = WakeMeUpExtreme.create(uconfig)
    else:
        ret = WakeMeUpExtreme.create(sys.argv[1])
    ret.gui.run()
main()
