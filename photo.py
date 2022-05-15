import cv2
import wybor
import search
import sys
import funcs
import vals
import time
#from multiprocessing.pool import ThreadPool

def __main__(image):
	if vals.TIME == True:
		t1 = time.time()

	IMG = image
	if IMG is None:
		sys.exit("niewlasciwy plik")
	if not (IMG.any()):
		sys.exit("niewlasciwy_plik")	
	txt = []

	#pool = ThreadPool(processes=1)
	#async_result = pool.apply_async(funcs.procedure, (IMG, "1")) 
	txt1,txt2 = "",""
	#txt1 = funcs.procedure(IMG,"1")
	H,W,_ = IMG.shape
	while (H>1200 or W>1200):
		IMG = cv2.resize(IMG, (0,0), fx=0.5, fy=0.5) 
		H,W,_ = IMG.shape
	txt2 = funcs.procedure(IMG,"2")

	#txt1 = async_result.get()

	if vals.SHOW_IMG==True:
		print(txt1)
		print(txt2)
	for i in range(0,len(txt1)):
		if (len(txt1[i])>5 and len(txt1[i])<13):
			txt.append(txt1[i])
		if (len(txt2[i])>5 and len(txt2[i])<13):
			txt.append(txt2[i])
	if vals.SHOW_IMG==True:
		print(txt)
		print(len(txt))
	if len(txt)<4:
		list3 = search.search(IMG,vals.SHOW_IMG)
		txt=txt+list3
	if vals.SHOW_IMG==True:
		print(txt)
		print(len(txt))
	
	tab = wybor.wybor(txt,vals.SHOW_IMG)
	if vals.TIME == True:
		print('Czas: %d ms'%((time.time()-t1)*1000))
	vals.SHOW_ONCE=False
	if vals.SHOW_IMG==True or vals.VIDEO==False:
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	