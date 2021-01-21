"""
REST service.

Usage:
python rest_service.py --help

RESTful API:
run:  python rest_service.py
URL: http://localhost:5000/api
"""

import module
from specification import SPEC
from amodule.rest import Service

if __name__ == '__main__':
    Service(SPEC, module).run()
