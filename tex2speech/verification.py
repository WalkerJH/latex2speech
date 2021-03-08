'''
For testing (most of) the tex2speech system against a massive collection
  of tex files.

This is pretty bare-bones and is only useful for our specific setup.
'''

from os import listdir, remove
from os.path import isfile, join
import re
import logging
import traceback
import sys

from TexSoup import TexSoup

from aws_polly_render import start_polly

files_with_begin = []
files_where_parser_started = []
files_where_parser_succeeded = []
files_where_parser_failed = []

def purge(dir, pattern):
    for f in listdir(dir):
        if re.search(pattern, f):
            remove(join(dir, f))

fileDir = '/projects/49x/tex2speech/latex2speech/tex2speech/upload'
files = []
for f in listdir(fileDir):
  fname = join(fileDir, f)
  if isfile(fname):
    files.append(fname)

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


logging.basicConfig(filename="verification.log", level=logging.DEBUG)
log = logging.getLogger('verification')
print(log)

main = []
inputList = []
bibContents = []

discoveredFiles = len(files)
openedFiles = 0
workingParses = 0

def getFileList(files):
  s = "["
  for f in files:
    s += f.rsplit('/')[-1]
  s += "]"
  return s

def getCurFiles(inputFile):
  return inputFile.rsplit('/')[-1] + ' Input: ' + getFileList(inputList) + ' Bib: ' + getFileList(bibContents)

for inputFile in files:
  try:
    with open(inputFile, 'r') as input:
      openedFiles += 1
      input = input.read()
      if r"\begin{document}" in input:
        files_with_begin.append(getCurFiles(inputFile))
        main.append(f)
        pat = r'\\input{(.*)}|\\include{(.*)}|\bibliography{(.*)}'
        matchIter = re.finditer(pat, input)
        for match in matchIter:
          # lol
          count = (1 if match.group(1) else 0) + \
                  (1 if match.group(2) else 0) + \
                  (1 if match.group(3) else 0)
          if not count == 1:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.exception("FILES:: " + getCurFiles(inputFile))
            logging.debug(repr(traceback.format_tb(exc_traceback)))
            logging.debug(repr(traceback.extract_stack().format()))
          else:
            i = 1
            while not match.group(i):
              i += 1
            inputFile = match.group(i)

            targetList = input 
            fileType = '.tex'
            if i == 3:
              targetList = bibContents
              fileType = '.bib'
            if not fileType in inputFile[-4:]:
              inputFile += fileType
            
            if inputFile in files:
              targetList.append(inputFile)
        # Start start_polly here
        # TODO: Make this a function at very least
        try:
          files_where_parser_started.append(getCurFiles(inputFile))
          start_polly(main, inputList, bibContents)
          files_where_parser_succeeded.append(getCurFiles(inputFile))
          workingParses += 1
        except Exception as e:
          files_where_parser_failed.append(getCurFiles(inputFile))
          exc_type, exc_value, exc_traceback = sys.exc_info()
          logging.exception("FILES:: " + getCurFiles(inputFile))
          logging.debug(repr(traceback.format_tb(exc_traceback)))
          logging.debug(repr(traceback.extract_stack().format()))
  except FileNotFoundError as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.exception("FILES:: " + getCurFiles(inputFile))
    logging.debug(repr(traceback.format_tb(exc_traceback)))
    logging.debug(repr(traceback.extract_stack().format()))
  except UnicodeDecodeError as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.exception("FILES:: " + getCurFiles(inputFile))
    logging.debug(repr(traceback.format_tb(exc_traceback)))
    logging.debug(repr(traceback.extract_stack().format()))
  except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.exception("FILES:: " + getCurFiles(inputFile))
    logging.debug(repr(traceback.format_tb(exc_traceback)))
    logging.debug(repr(traceback.extract_stack().format()))
  #purge('/projects/49x/tex2speech/latex2speech/tex2speech/', 'final.*\.tex')

logging.debug("RESULTS::")
logging.debug("files_with_begin:")
logging.debug("\tLength: " + str(len(files_with_begin)))
logging.debug("\tNames: " + repr(files_with_begin))
logging.debug("files_where_parser_started:")
logging.debug("\tLength: " + str(len(files_where_parser_started)))
logging.debug("\tNames: " + repr(files_where_parser_started))
logging.debug("files_where_parser_succeeded:")
logging.debug("\tLength: " + str(len(files_where_parser_succeeded)))
logging.debug("\tNames: " + repr(files_where_parser_succeeded))
logging.debug("files_where_parser_failed:")
logging.debug("\tLength: " + str(len(files_where_parser_failed)))
logging.debug("\tNames: " + repr(files_where_parser_failed))
