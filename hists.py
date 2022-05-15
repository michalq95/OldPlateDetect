import cv2
import chars

def HistogramOCR(FILE):
	def CalcHistW__(img):
		histW = []
		histWv = []
		height, width = img.shape
		i=0
		for w in range(width):
			histW.append(0)
			for h in range(height):
				if img[h][w]==0:
					histW[w]=histW[w]+1
			histWv.append((histW[w]))
			i=i+1
		return(histWv)
	
	def CalcHistH__(img):
		histH = []
		histHv = []
		i=0
		height, width = img.shape
		for h in range(height):
			histH.append(0)
			for w in range(width):
				if img[h][w]==0:
					histH[h]=histH[h]+1
			histHv.append((histH[h]))
			i=i+1
		return(histHv)

	def pearsonr(x, y):
 		n = len(x)
 		sum_x = float(sum(x))
 		sum_y = float(sum(y))
 		sum_x_sq = sum(map(lambda x: pow(x, 2), x))
 		sum_y_sq = sum(map(lambda x: pow(x, 2), y))
 		psum = sum(map(lambda x, y: x * y, x, y))
 		num = psum - (sum_x * sum_y/n)
 		den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
 		if den == 0: return 0
 		return num / den
	
	ig = cv2.imread(FILE,0)
	histgW =CalcHistW__(ig)
	histgH =CalcHistH__(ig)
	maxi = -2
	stri = ""
	for fn in range(0,len(chars.W)):
		#im = cv2.imread(fn,0)
		histrW = chars.W[fn]
		histrH = chars.H[fn]
		b = pearsonr(histgW,histrW)
		c = pearsonr(histgH,histrH)
		d = (b+c)
		if d>maxi:
			maxi=d
			stri = chars.toChar(fn)
	return stri
