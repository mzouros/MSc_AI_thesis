# Download Unsplash dataset images

# Impots
import csv
import pandas as pd
import numpy as np
import urllib
from urllib.request import urlopen
import cv2

# Paths
tsvPath = '/home/mike/Artificial Intelligence MSc/3rd Semester/Thesis/Unsplash_Full/photos.tsv000'
imagePath = '/home/mike/Artificial Intelligence MSc/3rd Semester/Thesis/Unsplash_Full/Images/'

# Download, Resize, Save Unsplash images
col_list = ["photo_image_url"]
df = pd.read_csv(tsvPath, usecols=col_list, sep='\t')
i = 0
while i<1000: # number of images
	print("Downloading from url: ", df["photo_image_url"][i])
	url = df["photo_image_url"][i]
	filename = url.split('/')[-1]
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# resize image (400x400)
	width = 400
	height = 400
	dim = (width, height)
	try:
		resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		# save image
		cv2.imwrite(imagePath+filename+".jpg", resized)
	except:
		print("skipped image (small size)")
	i = i + 1
