#!/var/www/html/FlaskApp/cs2080fileshare/.venv/bin python
#activate_this = '/var/www/html/FlaskApp/cs2080fileshare/.venv/bin/activate_this.py'
#exec(open(activate_this).read(), dict(__file__=activate_this))
#import runpy
#runpy.run_path("/var/www/html/FlaskApp/cs2080fileshare/.venv/bin/activate_this.py")
import sys
sys.path.insert(0,"/var/www/html/FlaskApp/cs2080fileshare/.venv/lib/python3.12/site-packages")

#import sys
#sys.prefix = "/var/www/html/FlaskApp/cs2080fileshare"

help("modules")

import sys
import logging
logging.basicConfig(stream=sys.stderr)
project_home = "/var/www/html/FlaskApp"
if project_home not in sys.path:
	sys.path = [project_home] + sys.path
#sys.path.insert(0,"/var/www/html/FlaskApp/")


from cs2080fileshare.__init import app as application
application.secret_key = 'askjfahfbakjdbfkbj'
