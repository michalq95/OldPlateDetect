import numpy as np
import cv2
from PIL import Image
import pytesseract
import os
import re
import hists
import ImageTranform
import glob
import shutil
import vals

def remBlob(IMG):
	ret,IMG2 = cv2.threshold(IMG,127,255,cv2.THRESH_BINARY)
	IMG = cv2.bitwise_not(IMG)
	IMG = cv2.copyMakeBorder(IMG,1,1,1,1,cv2.BORDER_CONSTANT,value=[0,0,0])
	IMG = cv2.erode(IMG,np.ones((3,3),np.uint8),iterations = 1)
	IMG = cv2.dilate(IMG,np.ones((3,3),np.uint8),iterations = 1)
	(cnts,_) = cv2.findContours(IMG,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		area = cv2.contourArea(box)
		if area < vals.SIZE_BLOB:
			cv2.drawContours(IMG,[c],0,(0,0,0),cv2.FILLED)
		elif area > vals.SIZEMAX_BLOB:
			cv2.drawContours(IMG,[c],0,(0,0,0),cv2.FILLED)
			
	IMG = cv2.bitwise_not(IMG)
	return IMG

def OCR(IMAGE,nazwa,nr,rgb,bmp):
	if rgb == False:
		IMAGE = cv2.copyMakeBorder(IMAGE,2,2,2,2,cv2.BORDER_CONSTANT,value=[255,255,255])
		IMAGE = cv2.dilate(IMAGE,np.ones((3,3),np.uint8),iterations = 1)	
		#ret,IMAGE = cv2.threshold(IMAGE,0,255,cv2.THRESH_OTSU)
		IMAGE = cv2.erode(IMAGE,np.ones((5,5),np.uint8),iterations = 1)
	if bmp == True:
		cv2.imwrite(nazwa+nr+".bmp",IMAGE)	
	else:
		cv2.imwrite(nazwa+nr+".jpg",IMAGE)	
	if vals.SHOW_IMG==True:
		cv2.imshow(nazwa+nr,IMAGE)
	if bmp == True:
		t7 = pytesseract.image_to_string(Image.open(nazwa+nr+".bmp"),config="--psm 7 ")
	else:
		t7 = pytesseract.image_to_string(Image.open(nazwa+nr+".jpg"),config="--psm 7 ")
		if vals.DEL == True:
			os.remove(nazwa+nr+".jpg")
	t7 = re.sub(r'\W+', '', t7)
	t7 = t7.replace("_", "")
	t7 = t7.upper()
	if (len(t7)>6 and len(t7)<9 and vals.SHOW_ONCE==False):
		#cv2.imshow(nazwa+nr,IMAGE)
		vals.SHOW_ONCE=True
	return t7

def crop_transform_plate(IMAGE,IMAGE_EDG,aproxymacja):
	try:
		(cnts,_) = cv2.findContours(IMAGE_EDG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
		screenCnt = None
		for c in cnts:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, aproxymacja * peri, True) 
			if len(approx) == 4 and cv2.contourArea(approx)>50: 
				screenCnt = approx
				x,y,w,h = cv2.boundingRect(c)
				pt = screenCnt.reshape(4, 2)
				corners = np.zeros((4, 2), dtype = "float32")
				suma = pt.sum(axis = 1)
				corners[0] = pt[np.argmin(suma)]
				corners[2] = pt[np.argmax(suma)]
				rozn = np.diff(pt, axis = 1)
				corners[1] = pt[np.argmin(rozn)]
				corners[3] = pt[np.argmax(rozn)]
				#proba poprawienia gdy znalenione krawedzie znalazly nie tylko tablice
				#uzyty try except poniewaz mozliwe byloby wyjscie poza maksymalna wielkosc obrazka
				if (corners[1][0]-corners[2][0])<(corners[0][0]-corners[3][0]):
					try:
						rho = corners[1][0]-corners[2][0]
						corners[3][0]=corners[0][0]-rho
					except:
						pass	
				img = np.zeros(vals.size, np.uint8)
				pts2 = np.array([[0,0],[vals.size[0] - 1, 0],[vals.size[0] - 1, vals.size[1] -1],[0, vals.size[1] - 1 ],], dtype=float)
				h, status = cv2.findHomography(corners, pts2)
				img = cv2.warpPerspective(IMAGE, h, vals.size[0:2])
				return img
	except:
		pass
def oper_white(whitefield,name,nr,aproxymacja):
	textw= "temptemp"
	whitefield = find_white(whitefield,name,nr,aproxymacja)
	text_w = rec_white(whitefield,name,nr)
	whitefield = remBlob(whitefield)
	text_c = rec_white(whitefield,name+"_c",nr)
	if (len(text_c)<9 and len(text_c)>6 and (len(text_w)<6) or len(text_w)>9):
		return text_c
	else:
		return text_w

def find_white(whitefield,name,nr,aproxymacja):
	textfw = ""
	whitefield=cv2.copyMakeBorder(whitefield,1,1,1,1,cv2.BORDER_CONSTANT,value=[0,0,0])
	upper = np.array([255, 255, 255])
	lower = np.array([vals.BIEL_MIN, vals.BIEL_MIN, vals.BIEL_MIN])
	mask = cv2.inRange(whitefield, lower, upper)
	mask2 = crop_transform_plate(mask,mask,aproxymacja)
	mask2 = cv2.copyMakeBorder(mask2,1,1,1,1,cv2.BORDER_CONSTANT,value=[255,255,255])
	return mask2

def rec_white(mask2,name,nr):
	try:
		mask2 = cv2.dilate(mask2,np.ones((3,3),np.uint8),iterations = 1)	
		ret,mask2 = cv2.threshold(mask2,0,255,cv2.THRESH_OTSU)
		mask2 = cv2.erode(mask2,np.ones((5,5),np.uint8),iterations = 1)
		if vals.SHOW_IMG==True:
			cv2.imshow(name+nr,mask2)
		cv2.imwrite(name+nr+".jpg", mask2)
		textfw = pytesseract.image_to_string(Image.open(name+nr+".jpg"),config="--psm 7")
		textfw = re.sub(r'\W+', '', textfw)
		textfw = textfw.replace("_", "")
		textfw = textfw.upper()
		if vals.DEL == True:
			os.remove(name+nr+".jpg")
		if (len(textfw)>6 and len(textfw)<9 and vals.SHOW_ONCE==False):
			#cv2.imshow(name+nr,mask2)
			vals.SHOW_ONCE=True
	except:
		pass

	return textfw

def sear(img,nr):
	text0,text1,text2,text3,text4 = "","","","",""
	text0 = OCR(img,"e",nr,True,False)
	#cv2.imshow("text0"+nr,img)
	imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgg = imgg.astype("uint8")
	text3 = OCR(img,"e",nr,True,False)


	ret,imgg = cv2.threshold(imgg,127,255,cv2.THRESH_OTSU)
	cv2.imshow("text1"+nr,imgg)
	text1 = OCR(imgg,"ee",nr,False,False)
	imgg = cv2.morphologyEx(imgg, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	cv2.imshow("erode"+nr,imgg)

	
	#ret,imge = cv2.threshold(imgg,0,255,cv2.THRESH_OTSU)
	imge = crop_transform_plate(imgg,imgg,0.03)
	#text2 = OCR(imge,"eee",nr,False,False)
	imge = remBlob(imge)
	text3 = OCR(imge,"eeecln",nr,False,True)
	#cv2.imshow("text3"+nr,imge)
	#if text3 != "":
	#text4 = clnhist("eeecln",nr)
	#else:
	#	os.remove("eeecln"+nr+".bmp")
	return(text0,text1,text2,text3,text4)

def clnhist(nam,nr):
	text = ""
	o = ImageTranform.Obrazek(nam+nr+'.bmp',nam+nr)
	#pth = o.tnij()
	#order = sorted(glob.glob(pth+'/*.bmp'))
	#for i in order:
	#	text+=str(hists.HistogramOCR(i))
	shutil.rmtree(pth)
	if vals.DEL == True:
		os.remove(nam+nr+'.bmp')
	return text

def haar(plate,gray,nr):
	text0,text4,text1,text7,text8 = "","","","",""
	min = 0;
	for (x,y,w,h) in plate:
		if (min == 0):
			min=w+h
		if (min<w+h):
			continue;
		gray_crop = gray[y:y+h, x:x+w]
		ret,thr_img = cv2.threshold(gray_crop,0,255,cv2.THRESH_OTSU)
		text0 = OCR(thr_img,"q",nr,False,False)
		thr_img = cv2.bilateralFilter(thr_img,15,75,75)
		thr_img = cv2.copyMakeBorder(thr_img,1,1,1,1,cv2.BORDER_CONSTANT,value=[1,1,1])
		edge_img = cv2.Canny(thr_img, 30, 200)	
		#WYCIECIE SAMEJ TABLICY Z REZULTATU KASKADY
		im_dst=crop_transform_plate(thr_img,edge_img,0.06)
		backtorgb = cv2.cvtColor(thr_img,cv2.COLOR_GRAY2RGB)
		text4 = oper_white(backtorgb,"www",nr,0.06)
		try:
			text1 = OCR(im_dst,"qq",nr,False,False)
		except:	
			pass
		im_dst = remBlob(im_dst)
		text7 = OCR(im_dst,"qqcln",nr,False,True)
		#if (len(text7)==7 or len(text7)==8):
		#	text8 = clnhist("qqcln",nr)
		#else:
		#	os.remove("qqcln"+nr+".bmp")
	return text0,text4,text1,text7,text8


def procedure(img,nr):
	textin,text0,text1,text2,text3,text4,text5,text6,text7,text8,text9 = "","","","","","","","","","",""
	cascade = cv2.CascadeClassifier('files/haarcascade_russian_plate_number.xml')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#plate = cascade.detectMultiScale(gray, 1.3, 5)
	#szukanie kaskada haara najmniejszego wycinka zawietajacego tablice rejestracyjna
	#pool = ThreadPool(processes=1)
	#haar_result = pool.apply_async(haar, (plate, gray,nr))
	#haar_result = Process(target=haar ,args=(plate, gray,nr,))
	#haar_result.start()

	pha2 = cv2.bilateralFilter(gray,15,75,75)
	ret,pha2 = cv2.threshold(pha2,0,255,cv2.THRESH_OTSU)
	otsu = pha2.copy()
	pha2 = cv2.Canny(pha2,240,250)
	pha2 = cv2.copyMakeBorder(pha2,1,1,1,1,cv2.BORDER_CONSTANT,value=[0,0,0])
	pha2res = crop_transform_plate(otsu,pha2,0.06)
	text2 = OCR(pha2res,"qqq",nr,False,True)
	if (len(text2)==7 or len(text2)==8):
		text9 = clnhist("qqq",nr)
	else:
		os.remove("qqq"+nr+".bmp")
	#text3 = oper_white(img,"w",nr,0.01)
	#text5 = oper_white(img,"ww",nr,0.1)
	#
	#img = find_white(img,"wwww",nr,0.01)
	#img = remBlob(img)
	#text6 = rec_white(img,"wwww",nr)
	#text0,text4,text1,text7,text8 = haar(plate, gray,nr)

	#text0,text4,text1,text7,text8 = haar_result.get()
	return (text0,text1,text2,text3,text4,text5,text6,text7,text8,text9)