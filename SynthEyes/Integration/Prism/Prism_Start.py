# ; Start Prism


import os

import SyPy3


print("Prism Test")                                 #   TESTING


if "PRISM_ROOT" in os.environ:
    PRISMROOT = os.environ["PRISM_ROOT"]

    print(f"PRISM ROOT IN ENVIRON: {PRISMROOT}")
    if not PRISMROOT:
        print("PRISM_ROOT is not set")
    
#   Gets set during Integration installation
else:
    print("PRISM_ROOT is not set")
    PRISMROOT = r@PRISMROOTREPLACE@

print(f"*** PRISMROOT:  {PRISMROOT}")                #   TESTING

PLUGINROOT = r@PLUGINROOTREPLACE@

print(f"*** PLUGINROOT: {PLUGINROOT}")               #    TESTING

input("Press Enter to exit...")









# hlev = SyPy.SyLevel()
# hlev.OpenExisting()

