import sys
import os

sys.path.insert(0, '/var/www/html/risyu')
sys.path.insert(0, os.path.expanduser('~/risyu'))
print(sys.path)

from app import app as application
