import subprocess
import sys
import time

def package_installer(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    time.sleep(5) #if your system can install this quicker, change the value. 
    #this is developed on an i3 from 2016, so yes, it takes this long.
package = "pygame","tk","matplotlib","mutagen,pyqt5"

for package in package:
    package_installer(package)
