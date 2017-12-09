from PIL import Image
import os
images = os.listdir("./Frames1")
for i in images:
	print i
	img = Image.open("./Frames1/" + i)
	width = img.size[0]
	height = img.size[1]
	img2 = img.crop((35, 305, 260, 333	))
	print img2
	img2.save("./Crop3/" + i)
# img = Image.open("./Frames2/" + "0072.bmp")
# width = img.size[0]
# height = img.size[1]
# img2 = img.crop((0, 643, width, height))
# print img2
# img2.save("img2.jpg")	
