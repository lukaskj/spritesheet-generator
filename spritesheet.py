from PIL import Image
from typing import List, AnyStr
import os
import math
import getopt
import sys

images: List[Image.Image] = []
imagesFolder: AnyStr = 'images'
outputFile: AnyStr = "spritesheet.png"
imagesPerRow = 5

def absoluteFilePaths(directory):
  if not os.path.isdir(directory):
    raise Exception(f"Directory '{directory}' not found.")
  result = []
  for dirpath,_,filenames in os.walk(directory):
    for f in filenames:
      result.append(os.path.abspath(os.path.join(dirpath, f)))
      # yield os.path.abspath(os.path.join(dirpath, f))
  return result

def main():
  imagesFilename = absoluteFilePaths(imagesFolder)
  print("Total images", len(imagesFilename))

  try:
    for filename in imagesFilename:
      imageObj = Image.open(filename)
      images.append(imageObj)
      
    handleImages(images)
  finally:
    closeAllImages()


def handleImages(imageObjs: List[Image.Image]):
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
    spriteSheet.save(outputFile, 'PNG')
  finally:
    spriteSheet.close()


def parseOpts():
  global outputFile, imagesFolder, imagesPerRow
  options, arguments = getopt.getopt(sys.argv[1:], 'o:i:',["output=", "imagesPerRow="])
  for o, a in options:
    if o in ("-o", "--output"):
      outputFile = a
    if o in ("-i", "--imagesPerRow"):
      imagesPerRow = int(a)
  if len(arguments) > 0:
    imagesFolder = arguments[0]



def closeAllImages():
  print("Closing all images")
  for image in images:
      image.close()
  
  # for filename in imagesFilename:
  #   print(filename)

if __name__ == '__main__':
  parseOpts()
  main()