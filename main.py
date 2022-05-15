import photo
import os
import cv2
import vals
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("FILE", help="Podaj obraz lub film")
	parser.add_argument('-t', action='store_true', help="Mierz czas")
	parser.add_argument('-s', action='store_true', help="Pokaz szczegoly")
	parser.add_argument('-d', action='store_false', help="NIE usuwaj plikow do OCR")
	parser.add_argument('-a', action='store_true', help="Wcisnij klawisz gdy chcesz wyszukac tablice")
	parser.add_argument('-c', dest='fram', const=100, default=100, action='store', nargs='?', type=int, help='Tylko Video: co ile klatek szukac')
	args = parser.parse_args()
	vals.TIME = args.t
	fe = os.path.splitext(args.FILE)[1]
	if (fe==".jpg" or fe==".bmp" or fe == ".png" or fe==".jpeg"):
		vals.SHOW_IMG = args.s
		vals.DEL = args.d
		image = cv2.imread(args.FILE)
		if(image is None):
			quit("zepsuty lub nieistniejacy plik")
		cv2.namedWindow('image', cv2.WINDOW_NORMAL)	
		cv2.imshow('image',image)
		photo.__main__(image)
	elif (fe==".avi" or fe==".mp4"):
		if args.a == True:
			import video
			if args.fram>0:
				vals.FRAM = args.fram
			vals.VIDEO = True
			video.video(args.FILE)	
		else:
			import videoa
			vals.VIDEO = True
			videoa.video(args.FILE)
	else:
		quit("nieobslugiwany rodzaj pliku")



