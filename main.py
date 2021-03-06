import math
from PIL import Image
import y4m
import  imageReader
import fullSearch
import logsearch
import time
import diamondSearch

__name__='MotionVectorEstimator'
__version__='1.2.0'

def raw_input_with_default(text,default):
    input = raw_input(text+'['+default +']'+ chr(8)*4)
    if not input:
        input = default
    return input

def psnr(orignal_picture,compressed_picture):
#     peak signal-to-noise ratio
    mse =0
    #mean squared error
    for i in range(len(orignal_picture)):
        for j in range(len(orignal_picture[i])):
            mse=mse+(orignal_picture[i][j]-compressed_picture[i][j])*(orignal_picture[i][j]-compressed_picture[i][j])
    mse=mse/(len(orignal_picture)*len(orignal_picture[i]))
    mx_value=0
    for lst in orignal_picture:
        value=max(lst)
        if value > mx_value:
            mx_value=value
    psnr_=10*math.log( mx_value*mx_value/ mse, 10)
    return psnr_

def readStandardSequence(filename):
    # read y4m file from the
    data=raw_input(filename)
    reader =  y4m.Reader(verbose=True)
    reader.decode(data)

current_picture=[]
referenced_picture=[]



print "Welcome to ",__name__," ",__version__

current_picture_path=raw_input_with_default("Path to first(current) picture",'1.jpg')
referenced_picture_path=raw_input_with_default("Path to second(referenced) picture",'2.jpg')
feed_in=raw_input("Choose: Full, Log or Diamond Search")


current_picture=imageReader.loadImage(current_picture_path)
referenced_picture=imageReader.loadImage(referenced_picture_path)
p = 4# len(current_picture)/70 # half of search window
n = 4 # size of macroblock

motion_estimation=None
comparations=None
start = time.time()
end = time.time()
useInterpolation=False


if "full" in feed_in.lower() :
    full_ = fullSearch.FullSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p,useIntrpolation=useInterpolation)
    compressedImage = full_.createCompressedImage()
    end = time.time()

    print full_.motionEstimation()
    comparations=full_.numOfcomparedMacroblocks
elif "diamond" in feed_in.lower():
    if useInterpolation:
        print "---Diamond search doesn't support interpolation---"
    useInterpolation=False
    ds = diamondSearch.DiamondSearch(current_picture, referenced_picture, n, p)
    compressedImage = ds.createCompressedImage()
    end = time.time()
    print ds.motionEstimation()
    comparations=ds.numOfcomparedMacroblocks
elif "log" in feed_in.lower() :
    log = logsearch.LogSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p, useIntrpolation=useInterpolation)
    compressedImage = log.createCompressedImage()
    end = time.time()

    print log.motionEstimation()
    comparations=log.numOfcomparedMacroblocks
else:
    print "Not found"
    exit()

running_time=(end - start)
print "it took: ",running_time, "s"," Number of comparitions: ",comparations

print "psnr= ",psnr(referenced_picture,compressedImage),"[dB] - bigger value is better"

im = Image.new("L", (len(compressedImage[0]), len(compressedImage)), "white")
img_list=[]
for lst in compressedImage:
    img_list=img_list+lst
im.putdata(img_list)
im.show()