import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(levelname)-8s %(message)s')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if 'unittest' in sys.modules.keys():
    INPUT_DIR = os.path.join(ROOT_DIR, '../test/input')
else:
    INPUT_DIR = os.path.join(ROOT_DIR, 'input')
