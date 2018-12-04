# -*- coding: utf-8 -*-
#
# Resources for appCompat:
# https://github.com/aosp-mirror/platform_frameworks_support.git
#
#  Configuration parameters
# --hasargs --package TestActivity --activity FragmentTest

if __name__ == "__main__":
    from SystemManager.AppStart import AppStart
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package', action='store', dest='package', help='Package name')
    parser.add_argument('-a', '--activity', action='store', dest='activity', help='Activity name')
    parser.add_argument('--hasargs', action='store_true', default=False)
    args = parser.parse_args()
    component = ('SystemManager', 'SystemLauncher')
    if args.hasargs and args.package and args.activity:
        component = (args.package, args.activity)

    app = AppStart(starterComponent=component)
    app.mainloop()
