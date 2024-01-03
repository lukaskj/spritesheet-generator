from PIL import Image
from typing import List, AnyStr
import os
import math
import getopt
import sys
import re

Image.MAX_IMAGE_PIXELS = None

# USAGE
#   $ python spritesheet.py --imagesPerRow 20 --generateFullSpritesheet --only idle,walk swordsman <input folder>

def absoluteFilePaths(directory):
  if not os.path.isdir(directory):
    raise Exception(f"Directory '{directory}' not found.")
  result = []
  for dirpath,_,filenames in os.walk(directory):
    for f in filenames:
      result.append(os.path.abspath(os.path.join(dirpath, f)))
      # yield os.path.abspath(os.path.join(dirpath, f))
  return result


def loopFolders(baseDir, imagesPerRow, onlyAnimations, generateFullSpritesheet=False):
  spritesheetsOutputFolder = 'output'
  spritesheetsOutputFolderFull = os.path.join(baseDir, spritesheetsOutputFolder)
  if not os.path.exists(spritesheetsOutputFolderFull):
    os.mkdir(spritesheetsOutputFolderFull)

  allAnimations = len(onlyAnimations) == 0 or onlyAnimations == None
  
  folders_to_output = []
  for fdir in os.listdir(baseDir):
    fullDir = os.path.join(baseDir, fdir)
    if not os.path.isdir(fullDir) or fdir == spritesheetsOutputFolder:
      continue
    if not allAnimations and (fdir not in onlyAnimations):
      continue
    outputPartialSheet = os.path.join(spritesheetsOutputFolderFull, re.sub(r'[^a-zA-Z0-9]', '-', fullDir) + ".png")
    folders_to_output.append((fullDir, outputPartialSheet))
  
  for inputDir, outputFile in folders_to_output:
    print(f"[+] Animation '{inputDir}' to '{outputFile}'")
    handleImages(inputDir, imagesPerRow, outputFile)
  
  if len(folders_to_output) > 1 and generateFullSpritesheet:
    fullSpritesheetFile = os.path.join(baseDir, re.sub(r'[^a-zA-Z0-9]', '-', baseDir) + "-full.png")
    print(f"[+] Generating full spritesheet at '{fullSpritesheetFile}'")
    handleImages(spritesheetsOutputFolderFull, 1, fullSpritesheetFile)
  else:
    print("[-] Not generating full spritesheet.")

def handleImages(baseDir, imagesPerRow, outputFile):
  imageObjs: List[Image.Image] = []
  imagesList = absoluteFilePaths(baseDir)
  for filename in imagesList:
    imageObj = Image.open(filename)
    imageObjs.append(imageObj)
  
  maxWidth = 0
  maxHeight = 0
  # get largest width and height
  for image in imageObjs:
    size = image.size
    if size[0] > maxWidth:
      maxWidth = size[0]
    if size[1] > maxHeight:
      maxHeight = size[1]
  
  totalWidth = imagesPerRow * maxWidth
  totalRows = math.ceil(len(imageObjs) / imagesPerRow)
  totalHeight = totalRows * maxHeight
  spriteSheet = Image.new('RGBA', (totalWidth, totalHeight), (255,255,255,1))
  
  try:
    for i, image in enumerate(imageObjs):
      col = i % imagesPerRow
      row = math.floor(i / imagesPerRow)
      spriteW = col * maxWidth
      spriteH = row * maxHeight
      spriteSheet.paste(image, (spriteW, spriteH))
      image.close()
    spriteSheet.save(outputFile, 'PNG')
  finally:
    spriteSheet.close()
    closeAllImages(imageObjs)


def closeAllImages(images):
  for image in images:
      image.close()

def parseOpts():
  # global outputFile, imagesFolder, imagesPerRow
  result = {
    'imagesPerRow': 5,
    'imagesFolder': 'images',
    'generateFullSpritesheet': False,
    'only': []
  }
  options, arguments = getopt.getopt(sys.argv[1:], 'go:i:',["generateFullSpritesheet", "only=", "imagesPerRow="])
  
  for o, a in options:
    if o in ("-o", "--only"):
      result['only'] = a.split(",")
    if o in ("-i", "--imagesPerRow"):
      result['imagesPerRow'] = int(a)
    if o in ("-g", "--generateFullSpritesheet"):
      result['generateFullSpritesheet'] = True
  if len(arguments) > 0:
    result['imagesFolder'] = arguments[0]

  return result

if __name__ == '__main__':
  opts = parseOpts()
  loopFolders(opts['imagesFolder'], opts['imagesPerRow'], opts['only'], opts['generateFullSpritesheet'])