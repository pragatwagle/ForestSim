import os
import random
import os.path

# the folder contain all of the segmentation images
dir = '/Users/pragatwagle/Desktop/VailResearch/VailRepos/VailNav-2/data/vail_all'
folders = os.walk(dir + "/unconverted_annotations")

# the total number of images
total = 2094

# percentage of train split
train = round(total * .9)

# percentage of test split
test = round(total * .1)
filesRandom = []

# all images in the folder 
for f in folders:
    filesRandom = filesRandom + f[2] 
    
# randomize the images
random.shuffle(filesRandom)

# get the splits
testFiles = filesRandom[0:test]
trainfiles = filesRandom[test+1:total+1]

#
def split(dir, textfile, filesNames):
    currCount = 0
    for x in filesNames:
        with open(f'{dir}/{textfile}', 'a') as f:
            # directory containing all of the segmentation images
            curSegDir = dir + "/unconverted_annotations/" + x
            
            # directory containing all of the rgb images
            curImgDir = dir + "/images_all/" + x
            
            if os.path.isfile(curSegDir) or os.path.isfile(curImgDir):
                f.write(x)
                f.write('\n')  
                print(currCount)       
            else:
                print("one doesn't exists")
            currCount = currCount + 1

#test: the main directory, the text file to write the test iamges to, the test iamges
split('/Users/pragatwagle/Desktop/VailResearch/VailRepos/VailNav-2/data/vail_all', 
        'test.txt', testFiles)
#train: the main directory, the text file to write the train iamges to, the train iamges
split('/Users/pragatwagle/Desktop/VailResearch/VailRepos/VailNav-2/data/vail_all', 
        'train.txt', trainfiles)