import cv2
import photo
from threading import Thread

def video(FILE):
	cap = cv2.VideoCapture(FILE)
	try:	
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		fps = cap.get(cv2.CAP_PROP_FPS)
		waitPerFrameInMillisec = int( 1/fps * 1000/1 )
	except:
		quit("zepsuty lub nieistniejacy plik")

	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	t1 = Thread()
	t1.start()
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('frame',frame)
			key = cv2.waitKey(waitPerFrameInMillisec)
			if key == ord('q'):
				break
			elif key != -1:
				try:
					t1.join()
					t1 = Thread(target=photo.__main__, args=(frame,))
					t1.start()
				except:
					pass
		else:
			break
	cap.release()
	cv2.waitKey
	cv2.destroyAllWindows()