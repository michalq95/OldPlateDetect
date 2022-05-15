import cv2
import photo
from threading import Thread
import vals

def video(FILE):
	cap = cv2.VideoCapture(FILE)
	try:	
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		fps = cap.get(cv2.CAP_PROP_FPS)
	except:
		quit("zepsuty lub nieistniejacy plik")
	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	t1 = Thread()

	
	while(cap.isOpened()):
		ret, frame = cap.read()
		cv2.imshow('frame',frame)
		post_frame = cap.get(1)
		if post_frame%vals.FRAM==1:
			try:
				t1.join()
			except:
				pass

			t1 = Thread(target=photo.mian, args=(frame,))
			t1.start()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if post_frame+1==length:
			t1.join()
			photo.mian(frame)
			break	
	cap.release()
	cv2.waitKey
	cv2.destroyAllWindows()