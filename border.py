from PIL import Image, ImageOps, ExifTags
import os

def walk(dir):
	file_list = []
	for root, _, filenames in os.walk(dir):
		for f in filenames:	
			file_list.append(f)
	return file_list

def get_images_only(file_list):
	valid = ["jpg", "gif", "png"]
	new_list = []
	for file in file_list:
		f = file.split(".")
		if f[-1].lower() not in valid:
			continue
		new_list.append(file)
	return new_list

def make_path(folder, filename):
	return folder + "/" + filename

def border_manager(src):
	min_border = 30
	x = 0
	y = 0
	img = Image.open(src)
	width, height = img.size
	if width > height:
		x = min_border
		y = width-height+min_border+1
	elif height > width:
		x = height-width+min_border+1
		y = min_border
	else:
		x = min_border
		y = min_border
	return (int(x/2), int(y/2))

def add_border(src, out, border):
	img = Image.open(src)
	for orientation in ExifTags.TAGS.keys() : 
		if ExifTags.TAGS[orientation]=='Orientation' : break 
	exif=dict(img._getexif().items())
	img = ImageOps.expand(img, border=border, fill="#fffff0")
	if exif[orientation] == 3 : 
		img=img.rotate(180, expand=True)
	elif exif[orientation] == 6 : 
		img=img.rotate(270, expand=True)
	elif exif[orientation] == 8 : 
		img=img.rotate(90, expand=True)
	img.save(out)

def main():
	try:
		in_folder = input("Enter the path of your file: ")
		assert os.path.exists(in_folder), "Path does not exist"
		out_folder = input("Enter the path on where to save the images: ")
		assert os.path.exists(out_folder), "Path does not exist"
	except:
		print("Path does not exist.")
		os.system("pause")
		exit()
	print("Getting files...")
	list = get_images_only(walk(in_folder))
	print("Converting images...")
	for image in list:
		add_border(make_path(in_folder, image), make_path(out_folder, image), border=border_manager(make_path(in_folder, image)))
	print("Done")
	