from PIL import Image, ImageFilter, ImageOps
import numpy as np
from easygui import fileopenbox
import cv2

class Image_handler(object):
	def __init__(self,image):
		self.im = Image.open(image)

	@staticmethod
	def get_image() -> str:
		"""
		Ask's users the name of the file to be used
		:return:
		a string of the file name
		"""
		path = fileopenbox()
		return path

	def convert_bandw(self, mode) -> None:
		"""
		--- THIS IS THE NEW, ENHANCED FUNCTION ---
		Converts an image into clean, black-and-white line art (edges).
		This PREVENTS the "dotted" look by creating lines, not dots.
		"""
		if mode == "color":
			self.im = self.im.convert(mode='RGB') 
		
		elif mode == "black":
			open_cv_image = np.array(self.im.convert('L'))
			
			blurred = cv2.GaussianBlur(open_cv_image, (5, 5), 0)
			
			canny_edges = cv2.Canny(blurred, 50, 150)
			
			canny_inverted = cv2.bitwise_not(canny_edges)
			self.im = Image.fromarray(canny_inverted).convert('1')

	def invert(self,image) -> None:
		"""
		Returns a color inverted image file
		:return:
		"""
		self.im = ImageOps.invert(Image.open(image))

	def resize(self,value:int) -> None:
		"""
		resizes image to fit withing an X by X square
		:param value:
		Size of the square input field
		:return:
		"""
		if value < 1:
			value = 1
		
		horizontalsize, verticalsize = self.im.size
		if horizontalsize > verticalsize:
			conversion = horizontalsize / value
			self.im = self.im.resize((int(horizontalsize / conversion), int(verticalsize / conversion)))
		else:
			conversion = verticalsize / value
			self.im = self.im.resize((int(horizontalsize / conversion), int(verticalsize / conversion)))

	def update_array(self) -> np.array:
		"""
		Converts image into a numpy array of bools
		:return:
		"""
		array = np.array(self.im)
		return array
