import numpy
import pyautogui
import time
import cv2

class Mouseomate(object):
	pyautogui.PAUSE = 0.005 
	pyautogui.FAILSAFE = True

	ACTIONS_BEFORE_PAUSE = 100 
	PAUSE_DURATION = 2.5       

	@staticmethod
	def draw_outline_and_fill(image_array: numpy.array, offset:int, rsleep:int, lsleep:int, start_pos) -> None:
		"""
		1. Draws all the outlines for smooth edges.
		2. Fills the insides with efficient, merged scanlines.
		"""
		
		print("Starting Pass 1: Drawing Outlines...")
		Mouseomate.contours_to_lines(image_array, offset, start_pos)
		
		time.sleep(Mouseomate.PAUSE_DURATION)
		
		print("Starting Pass 2: Filling Shapes...")
		Mouseomate.image_to_lines(image_array, offset, rsleep, lsleep, start_pos)
		
		print("Drawing Complete.")
	
	@staticmethod
	def image_to_lines(image_array: numpy.array, offset:int, rsleep:int, lsleep:int, start_pos) -> None:
		"""
		(Horizontal Fill) Fills the shape using efficient, merged scanlines.
		(Logic provided by user)
		"""
		startpositionx, startpositiony = start_pos
		actions_counter = 0

		height, width = image_array.shape
		tween = pyautogui.easeInQuad

		for y in range(height):
			start_x = None 
			
			for x in range(width):
				value = image_array[y, x] 
				
				if not value and start_x is None:
					start_x = x
				
				elif (value or x == width - 1) and start_x is not None:
					end_x = x if value else x + 1 
					
					screen_start_x = startpositionx + start_x * offset
					screen_start_y = startpositiony + y * offset
					screen_end_x = startpositionx + end_x * offset
					
					pyautogui.moveTo(screen_start_x, screen_start_y)
					pyautogui.dragTo(screen_end_x, screen_start_y, duration=lsleep, button='left', tween=tween)
					
					start_x = None
					
					actions_counter += 1
					if actions_counter >= Mouseomate.ACTIONS_BEFORE_PAUSE:
						time.sleep(Mouseomate.PAUSE_DURATION)
						actions_counter = 0
			
			time.sleep(rsleep) 
	
	@staticmethod
	def image_to_vertical_lines(image_array: numpy.array, offset:int, rsleep:int, lsleep:int, start_pos) -> None:
		pass

	@staticmethod
	def contours_to_lines(image_array: numpy.array, offset:int, start_pos) -> None:
		"""
		(Outlines) This draws all the "line art" using contours.
		"""
		try:
			import cv2
		except ImportError:
			print("="*50)
			print("ERROR: 'opencv-python' is required for Outline mode.")
			print("Please run: pip install opencv-python")
			print("="*50)
			return

		startpositionx, startpositiony = start_pos
		
		img_uint8 = (image_array == False).astype(numpy.uint8) * 255
		
		contours, _ = cv2.findContours(img_uint8, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		
		original_pause = pyautogui.PAUSE
		pyautogui.PAUSE = 0.005 
		
		actions_counter = 0
		tween = pyautogui.easeInQuad
		
		for cnt in contours:
			if len(cnt) < 2:
				continue

			start_point = cnt[0][0]
			px, py = start_point
			
			pyautogui.moveTo(startpositionx + px * offset, startpositiony + py * offset, duration=0.1, tween=tween)
			pyautogui.mouseDown(button='left')
			
			for point in cnt[1:]:
				px, py = point[0]
				pyautogui.moveTo(startpositionx + px * offset, startpositiony + py * offset, tween=tween)
				
				actions_counter += 1
				if actions_counter >= Mouseomate.ACTIONS_BEFORE_PAUSE:
					time.sleep(Mouseomate.PAUSE_DURATION)
					actions_counter = 0 
			
			pyautogui.mouseUp(button='left')
		
		pyautogui.PAUSE = original_pause
