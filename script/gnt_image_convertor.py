# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 10:08:34 2018

@author: 10984
"""
import os
import struct
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

GNT_FILE_HEADER_LEN = 10
GNT_FILE_HEADER_SAMPLE_SIZE_OFFSET = 4
GNT_FILE_HEADER_TAG_CODE_OFFSET = 6
GNT_FILE_HEADER_WIDTH_OFFSET = 8
GNT_FILE_HEADER_HEIGHT_OFFSET = 10

def parseAGntFile(gntFilePath):
    if gntFilePath == "":
        return
    if not gntFilePath.endswith(".gnt"):
        return
    with open(gntFilePath, "r") as gntFile:
        while True:
            gntHeader = np.fromfile(gntFile, dtype = "uint8", count = GNT_FILE_HEADER_LEN)
            if not gntHeader.size:
                break
            byteIndex = 1
            # header->sample_size 
            sampleSize = gntHeader[0]
            while byteIndex < GNT_FILE_HEADER_SAMPLE_SIZE_OFFSET:
                sampleSize += gntHeader[byteIndex] << (8 * byteIndex)
                byteIndex += 1
            # header->tag_code
            tagCode = gntHeader[GNT_FILE_HEADER_TAG_CODE_OFFSET - 1] + (gntHeader[GNT_FILE_HEADER_TAG_CODE_OFFSET - 2] << 8)
            # header->width
            width = gntHeader[GNT_FILE_HEADER_WIDTH_OFFSET - 2] + (gntHeader[GNT_FILE_HEADER_WIDTH_OFFSET - 1] << 8)
            print("width: {width}".format(width = width))
            # header->height
            height = gntHeader[GNT_FILE_HEADER_HEIGHT_OFFSET - 2] + (gntHeader[GNT_FILE_HEADER_HEIGHT_OFFSET - 1] << 8)
            print("height: {height}".format(height = height))
            if not GNT_FILE_HEADER_LEN + width * height == sampleSize:
                break
            bitMap = np.fromfile(gntFile, dtype = "uint8", count = width * height).reshape((height, width))
            yield bitMap, tagCode

def convertFromGntContainDir(gntDirPath):
    if gntDirPath == "":
        return
    if not os.path.isdir(gntDirPath):
        return
    for root, dirs, files in os.walk(gntDirPath):
        imageCount = 0
        for file in files:
            if file.endswith(".gnt"):
                imageCount = 0
                gntFilePath = os.path.join(root, file)
                print("Convert " + gntFilePath)
                (fileName, extension) = os.path.splitext(file)
                relativeDir = os.path.join(root, fileName)
                if not os.path.exists(relativeDir):
                    os.makedirs(relativeDir)
                for bitMap, tagCode in parseAGntFile(gntFilePath):
                    tagCodeUnicode = struct.pack('>H', tagCode).decode('gb2312')
                    imageFilePath = os.path.join(root, "{reldir}\\{fileName}_{tag}_{index}.jpg".format(reldir = fileName, fileName = fileName, tag = tagCodeUnicode, index = imageCount)) 
                    print("To " + imageFilePath)
                    print("Tag code: {tag}".format(tag = tagCodeUnicode))
                    image = Image.fromarray(bitMap)
                    image.convert("RGB").save(imageFilePath)
                    imageCount += 1
                    plt.figure(imageFilePath)
                    plt.imshow(image)
                    plt.show()
                    #image.show()
                    #time.sleep(1)

if __name__ == "__main__":
    convertFromGntContainDir("D:\\Git_repository_HWCR\\HWCR\\tmp")
    
        
        