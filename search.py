import numpy as np
import cv2
import funcs
import math

aspMIN = 1.5
aspMAX = 7
sizeMIN = 300
sizeMAX = 12000

def search(IMG,SHOW_IMG):
	print("search")
	probfnd = False
	kernel = np.ones((3,19),np.uint8)
	kernel5 = np.ones((5,5),np.uint8)
	#IMG = cv2.imread(FILE)
	h,w,_ = IMG.shape
	imgORG = IMG.copy()
	pomn = False
	grey = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)

	white = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel5)
	white = cv2.threshold(white, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#cv2.imshow("Light Regions", white)
	grey = cv2.GaussianBlur(grey,(3,15),0)
	#cv2.imshow("grey",grey)

	blackhat = cv2.morphologyEx(grey, cv2.MORPH_BLACKHAT, kernel)
	#cv2.imshow("blackhat",blackhat)
	#sobel = cv2.Sobel(blackhat,-1,0, 1, ksize=-1)
	#sobel = cv2.Sobel(blackhat,-1 ,dx=1, dy=0, ksize=-1)
	#cv2.imshow("sobel",sobel)
	ret,thr = cv2.threshold(blackhat,0,255,cv2.THRESH_OTSU)
	#cv2.imshow("thr1",thr)
	blur = thr
	#blur = cv2.GaussianBlur(thr,(5,13),0)

	closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
	#closing = cv2.morphologyEx(thr, cv2.MORPH_OPEN, np.ones((5,15),np.uint8))
	#cv2.imshow("closing",closing)
	ret,thresh_image = cv2.threshold(closing,0,255,cv2.THRESH_OTSU)
	#cv2.imshow("thresh_image",thresh_image)
	th = cv2.bitwise_and(thresh_image,white)
	#cv2.imshow("combo",th)
	#th = cv2.GaussianBlur(th,(5,5),0)
	(cnts,_) = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:7]
	screenCnt = None
	cv2.drawContours(IMG, cnts, -1, (255, 0, 0), 3)
	list3 = []
	licz = 0
	for c in cnts:
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(IMG,[box],0,(0,255,0),2)

		X = rect[0][0]
		Y = rect[0][1]
		angle = rect[2] 
		width = rect[1][0]
		height = rect[1][1]
		size = height*width

		#print(angle,width,height,size)

		if (width > 0 and height > 0) and ((width < IMG.shape[1]) and (height < IMG.shape[1])):
			if height > width:
				tmp = width
				width = height
				height = tmp
			asp = float(width)/height

			if (asp >= aspMIN and asp <= aspMAX):
				#print("1")
				#if True:
				if((size > sizeMIN) and (size < sizeMAX)):
					#print("2")
					corners = np.zeros((4, 2), dtype = "float32")
					suma = box.sum(axis = 1)
					corners[0] = box[np.argmin(suma)] 
					corners[2] = box[np.argmax(suma)]
					rozn = np.diff(box, axis = 1)
					corners[1] = box[np.argmin(rozn)]
					corners[3] = box[np.argmax(rozn)]
					#print(box)
					#print(corners)					

					#if 1==1:
					if ((math.dist(corners[0],corners[1])>math.dist(corners[1],corners[2]) and angle< 30) or (math.dist(corners[0],corners[1])>math.dist(corners[1],corners[2]) and angle> 60)):

						#print("3")
						cv2.drawContours(IMG,[box],0,(0,0,255),2)
						img = np.zeros((int(width),int(height),3), np.uint8)
						pts2 = np.array([[0,0],[width - 1, 0],[width - 1, height -1],[0, height - 1 ],], dtype=float)
						h, status = cv2.findHomography(corners, pts2)
						img = cv2.warpPerspective(imgORG, h, (int(width),int(height)))
															
						licz = licz+1
						res = funcs.sear(img,str(licz))						
						for i in range(0,len(res)):
							if len(res[i])>5:
								probfnd = True
								cv2.imshow("probfnd",img)
						list3 = list3 + list(res)

							
	if SHOW_IMG==True:
		cv2.imshow("th",IMG)
	return list3
