'''
For testing (most of) the tex2speech system against a massive collection
  of tex files.

This is pretty bare-bones and is only useful for our specific setup.
'''

from os import listdir
from os.path import isfile, join

from TexSoup import TexSoup

rootDir = '.'

files = [f for f in listdir(rootDir) if isfile(join(rootDir, f))]

'''
OPTION 1:
-Manually create main, input and bib file lists
-Call startpolly WITHOUT UPLOADING TO BUCKET

OPTION 2 (more epic but more hard):
-Use webbot to click links?
-Epic???

All options will possibly need to remove the file deletion step, 
or manually delete them itself.

Two levels of errors: Runtime and semantic. Clearly runtime are
1000 times easier to check for, so we'll start with that.
'''
import urllib3
# TODO: IF NO PROGRESS SOON, SWITCH TO RUNNING start_aws_polly DIRECTLY

