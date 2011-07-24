from distutils.core import setup
import sys
import py2exe

sys.argv.append('py2exe')
sys.argv.append('-q')
code_file = 'xlparse.pyw'
setup(windows = [{'script': code_file}])
