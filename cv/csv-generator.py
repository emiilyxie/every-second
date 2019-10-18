import os

for root, dirs, files in os.walk("."):
    for filename in files:
        if filename[-4:] == '.jpg':
            print(filename)

imgList = []

for root, dirs, files in os.walk("."):
    for filename in files:
        if filename[-4:] == ".jpg":
            imgList.append(filename)

urlList = []

for img in imgList:
    url = 'gs://my-first-bucket-yay123456/20190929_food/' + img
    urlList.append(url)

goodFormat = []

for link in urlList:
    newLink = "UNASSIGNED," + link + ",,,,,,,,,"
    goodFormat.append(newLink)

import csv

with open("food_test_imgs.csv", "w") as outfile:
    for lines in goodFormat:
        outfile.write(lines)
        outfile.write("\n")
