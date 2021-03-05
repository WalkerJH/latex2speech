'''
For testing (most of) the tex2speech system against a massive collection
  of tex files.

This is pretty bare-bones and is only useful for our specific setup.
'''

from os import listdir
from os.path import isfile, join

from TexSoup import TexSoup

fileDir = 'Documentation/sample_input_files/'

files = [f for f in listdir(fileDir) if isfile(join(fileDir, f))]

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

from aws_polly_render import start_polly
import re
import logging

log = logging.basicConfig(filename="verfication.log", encoding="utf-8", level=logging.DEBUG)

master = []
inputList = []
bibContents = []

discoveredFiles = len(files)
openedFiles = 0
workingParses = 0

print('Batch of files: ' + files)
for inputFile in files:
  try :
    with open(inputFile, 'r') as input:
      openedFiles += 1
      input = input.read()
      if r"\begin{document}" in input:
        master.append(f)
        pat = r'\input{(.*)}|\include{(.*)}|\bibliography{(.*)}'
        matchIter = re.finditer(pat, input)
        for match in matchIter:
          # lol
          count = (1 if match.group(1) else 0) + \
                  (1 if match.group(2) else 0) + \
                  (1 if match.group(3) else 0)
          if not count == 1:
            logging.error("More than one file found, either regex or me is dumb.")
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
          start_polly(main, inputList, bibContents)
          workingParses += 1
        except Exception as e:
          logging.error('An error occurred while parsing')
          logging.error('Message: ' + str(e))

  except FileNotFoundError as e:
    logging.exception("File " + inputFile + " could not be found.")
    logging.exception("Message: " + str(e))

print('Out of ' + str(discoveredFiles) + ' discovered files, ' + str(openedFiles) + ' could be opened and ' + str(workingParses) + ' succesfully parsed.')