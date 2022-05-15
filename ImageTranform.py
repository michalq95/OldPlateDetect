from PIL import Image
import os

class Obrazek:
	MALE = 12,12
	threshold = 127  
	
	def __init__(self,inp,testthu):
		self.dir = os.path.dirname(os.path.relpath(__file__))
		self.folder = "temp"
		self.name = 'temp'
		self.inp = inp
		self.testthu = testthu

		self.folder_path= os.path.join(self.dir,self.folder)

		if not os.path.exists(self.folder_path):
			try:
				os.makedirs(self.folder_path)
			except:
				raise

	def setSize(x,y):
		self.MALE[0]=x
		self.MALE[1]=y

	def topline(self,pix,hei,wid):
		for i in range(hei):
			for j in range(wid):
				if (pix[i][j]==0):
					return i

	def topline2(self,pix,hei,wid,mini):
		for i in range(mini,hei):
			for j in range(wid):
				if (pix[i][j]==0):
					return i

	def botline(self,pix,tl,hei,wid):
		for i in range(tl,hei):
			c=0
			for j in range(wid):
				if (pix[i][j]<255):
					c=1
			if c==0:
				return i
		return hei

	def leftmost(self,pix,hei,wid,mini):
		for i in range(mini,wid):
			for j in range(hei):
				if (pix[j][i]==0):
					return i

	def rightmost(self,pix,lm,hei,wid):
		for i in range(lm,wid):
			c=0
			for j in range(hei):
				if (pix[j][i]<255):
					c=1
			if c==0:
				return i
		return wid

	def tnij(self):
		if not os.path.exists(os.path.join(self.folder_path,self.testthu)):
			try:
				os.makedirs(os.path.join(self.folder_path,self.testthu))
			except:
				raise

		MIN_LEFT = 0
		MIN_UP = 0
		tl=0
		l=0
		im = Image.open( self.inp )
		

		while 1:
			pixels = list(im.getdata())
			WIDTH, HEIGHT = im.size
			pixels = [pixels[i * WIDTH:(i + 1) * WIDTH] for i in range(HEIGHT)]
			tl=self.topline2(pixels,HEIGHT,WIDTH,MIN_UP)
			#print("tl "+str(tl))
			if tl==None:
				break	
			bl=self.botline(pixels,tl,HEIGHT,WIDTH)
			MIN_UP = bl
			#print("minup "+str(MIN_UP))
			im2 = im.crop((0,tl,WIDTH,bl))
			# im2.save(self.out+"linia"+str(l),'BMP')
			pixels3 = list(im2.getdata())
			WIDTH3, HEIGHT3 = im2.size
			pixels3 = [pixels3[i * WIDTH3:(i + 1) * WIDTH3] for i in range(HEIGHT3)]
			licz = 0
			MIN_LEFT = 0
			while 1:
				lm = self.leftmost(pixels3,HEIGHT3,WIDTH3,MIN_LEFT)
				if lm==None:
					break
				rm = self.rightmost(pixels3,lm,HEIGHT3,WIDTH3)	
				MIN_LEFT = rm		
				im_szer1 = im2.crop((lm,0,rm,HEIGHT3))

				pixels2 = list(im_szer1.getdata())
				WIDTH2, HEIGHT2 = im_szer1.size
				pixels2 = [pixels2[i * WIDTH2:(i + 1) * WIDTH2] for i in range(HEIGHT2)]

				tl2=self.topline(pixels2,HEIGHT2,WIDTH2)
				bl2=self.botline(pixels2,tl2,HEIGHT2,WIDTH2)
				im_szer11 = im_szer1.crop((0,tl2,WIDTH2,bl2))
				#im_szer11.save(os.path.join(self.folder_path,self.out,self.name+str(l).zfill(2)+"_"+str(licz).zfill(2)+".bmp"),'BMP')
				img = im_szer11.resize(self.MALE,Image.BILINEAR)
				img = img.point(lambda p: p > self.threshold and 255)  
				img.save(os.path.join(self.folder_path,self.testthu,self.name+str(licz).zfill(2)+".bmp"), 'BMP')		
				licz+=1
				#print(licz)
			l+=1
		return(os.path.join(self.folder_path,self.testthu))

#o = Obrazek("blob.bmp","test_data_min")
#o.tnij()