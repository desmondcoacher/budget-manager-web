# wsgi.py
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/<your-project-name>")  # adjust this to your project directory

from app import app as application
