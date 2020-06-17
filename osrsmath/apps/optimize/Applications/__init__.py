# Prevent pdoc from trying to gen documentation for Application builds.

#import osrsmath.apps.optimize.Applications as app
#import inspect
#rint(inspect.getmembers(app, inspect.ismodule))

import glob

__pdoc__ = {}
for f in glob.glob('**', recursive=True):
    print(f)
#    if any(f.endswith(str(i)) for i in range(0, 10)):
 #       print('---')
    __pdoc__[f.replace('/', '.')] = False

#__pdoc__ = {
#    'osrsmath.apps.optimize.Applications': False,
#}
