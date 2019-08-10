import argparse
import os
import os.path
import numpy as np
import cv2 as cv
import time

parser = argparse.ArgumentParser()
dir = '/Users/datagridlangus/Desktop/img'
outdir = '/Users/datagridlangus/Desktop/trash/'
res = 256
scal = 1.3
parser.add_argument('-i', '--input_dir', type=str, help="Directory of input images")
parser.add_argument('-o', '--output_dir', type=str, help='Directory of output images')
parser.add_argument('-res', '--resolution', type=int, help='The dimensions of resizing')
parser.add_argument('-resize', '--resize_only', action='store_true', help='Resize only')
parser.add_argument('-s', '--scale', type=float, help='increases scales factor')
parser.add_argument('-delete', '--delete_orig', action='store_true', help='delete originals')
args = parser.parse_args()
if args.input_dir is not None:
	dir = args.input_dir
if args.output_dir is not None:
	outdir = args.output_dir
if args.resolution is not None:
	res = args.resolution
if args.scale is not None:
	scal = args.scale
global nums
nums = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
print(nums)
def crop(dir, outdir, res, scal, de):
	numLs = 0
	n = 0
	for file in os.listdir(dir):
		if file[-3:] != 'png' and file[-3:] != 'jpg':
			n = n+1
			pass
		else:
			location = dir + '/' + str(file)
			saveloc = outdir + '/' + str(file)[:-3] + 'png'
			img = cv.imread(location)
			face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
			try:
				gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
			except:
				pass
			faces = face_cascade.detectMultiScale(gray, scal, 10)
			dims = img.shape
			if len(faces) < 1:
				n+=1
			if len(faces) > 1:
				faces = faces[0]
				faces = [np.array(faces)]
			for(x,y,w,h) in faces:
				y1 = int(y-round((dims[1])/2))
				y2 = int(y+h+(round((dims[1])/12)))
				x1 = int(x-round(dims[0]/ 86))
				x2 = int(x+w+round(dims[0]/36))
				if y1 < 0:
					y1 = 0
				if y2 < 0:
					y2 = 0
				if x1 < 0:
					x1 = 0
				if x2 < 0:
					x2 = 0
				crop_img = img[y1:y2, x1:x2]
				crop_img = cv.resize(crop_img, (res, res))
				if de == True:
					os.remove(location)  
				cv.imwrite(saveloc, crop_img)
				n=n+1
				printProgressBar(n-1, nums, prefix = 'Progress:', suffix = 'complete', length = 50, fill = '#') 
	printProgressBar(n, nums, prefix = 'Progress:', suffix = 'complete', length = 50, fill = '#') 
def re(dir, outdir, res, de):
	numLs = 0
	n = 0
	for file in os.listdir(dir):
		if file[-3:] != 'png' and file[-3:] != 'jpg':
			n += 1
			pass
		else:
			location = dir + '/' + str(file)
			saveloc = outdir + '/' + str(file)[:-3] + 'png'
			img = cv.imread(location)
			crop_img = cv.resize(img, (res, res))
			if de == True:
				os.remove(location)  
			cv.imwrite(saveloc, crop_img)
			n=n+1 
			time.sleep(0.1)
			printProgressBar(n-1, nums, prefix = 'Progress:', suffix = 'complete', length = 50, fill = '#')  
	printProgressBar(n, nums, prefix = 'Progress:', suffix = 'complete', length = 50, fill = '#')  
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
#Call in a loop to create terminal progress bar
#@params:
#iteration   - Required  : current iteration (Int)
#total       - Required  : total iterations (Int)
#prefix      - Optional  : prefix string (Str)
#suffix      - Optional  : fix string (Str)
#decimals    - Optional  : positive number of decimals in percent complete (Int)
#length      - Optional  : character length of bar (Int)
#fill        - Optional  : bar fill character (Str)
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end == '\r')
	if iteration == total: 
		print()

if args.resize_only == True:
	re(dir, outdir, res, args.delete_orig) 
else:
	crop(dir, outdir, res, scal, args.delete_orig)

