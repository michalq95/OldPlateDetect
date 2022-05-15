def wybor(tp,SHOW_IMG):
	list1 = []
	list2 = []
	try:
		for i in range(0,len(tp)):
			if tp[i] not in list1:
				if len(tp[i])<6 or len(tp[i])>10:
					continue
				list1.append(tp[i])
				list2.append(1)
			else:
				j = list1.index(tp[i])
				list2[j]=list2[j]+1
	except:
		pass
	for i in range(0,len(list1)):
		if list1[i][2].isalpha():
			if list1[i][0]+list1[i][1]+list1[i][2] in open('files/tablice.csv').read():
				list2[i]=list2[i]+1
			else:
				list2[i]=list2[i]-1
		else:
			if list1[i][0]+list1[i][1] in open('files/tablice.csv').read():
				list2[i]=list2[i]+1
			else:
				list2[i]=list2[i]-1
		if list1[i].isalpha():
			list2[i]=list2[i]-1


	if SHOW_IMG==True:
		print(list1)
		print(list2)

	

	#dodatkowe punkty za idealna wielkosc
	for i in range(0,len(list1)):
		if (len(list1[i]) ==7 or len(list1[i]) ==8 ):
			list2[i]=list2[i]+1
		if (len(list1[i]) ==8):
			if list1[i][2].isdigit():
				list2[i]=list2[i]-0.5
	#
	for i in range(0,len(list1)):
		for j in range(0,len(list1)):
			if i==j:
				continue
			if list1[i] in list1[j]:
				list2[i]=list2[i]+0.1
	dlg = 0

	#zaklocenia czesto sa mylone z tymi znakami
	for i in range(0,len(list1)):
		if list1[i][0] == 'I' or list1[i][0]=="L" or list1[i][0] == 'E' or list1[i][0] == '1':
			if list1[i][1:] in list1:
				j = list1.index(list1[i][1:])
				list2[j]=list2[j]+1
			else:
				list1.append(list1[i][1:])
				list2.append(1)


	for i in range(0,len(list1)):
		dlg = dlg+float(len(list1[i]))
	try:
		dlg = int(round(dlg/len(list1)))
	except:
		pass
	if SHOW_IMG==True:
		print(dlg)
	for i in range(0,len(list1)):
		if len(list1[i])==dlg:
			list2[i]=list2[i]+0.4
	if not list1:
		print("Nie znaleziono tablicy")
	else:
		for i in range(0,len(list1)):
			if list1[i][2].isalpha():
				if list1[i][0]+list1[i][1]+list1[i][2] in open('files/tablice.csv').read():
					list2[i]=list2[i]+1.5
				else:
			   		list2[i]=list2[i]-1.5
			else:
				#print(string[0]+string[1])
				if list1[i][0]+list1[i][1] in open('files/tablice.csv').read():
					list2[i]=list2[i]+1.5
				else:
					list2[i]=list2[i]-0.5
			if list1[i].isalpha():
				list2[i]=list2[i]-1		


		top = max(list2)
		gg = list2.index(top)
		tops = []
		#for i in range(0,len(list1[gg])):
			#if list1[gg][i] == 'S':
		if 'S' in list1[gg][2:]:
			tmp = list1[gg].replace('S', "5")
			#	tmp[i] = '5';
			tops.append(tmp)
		if '5' in list1[gg]:
			tmp = list1[gg].replace('5', "S")
			#	tmp[i] = '5';
			tops.append(tmp)	

		for i in range(0,len(list1)):
			if top - list2[i]<1.2 and list2[i]>0:
				if list1[i] not in tops:
					tops.append(list1[i])
		print("Najbardziej: {}".format(list1[gg]))
		print("Prawdopodobne: {}".format(tops))
		list1, list2 = zip(*sorted(zip(list1, list2)))
		if SHOW_IMG==True:
			print(list(reversed(list1)))
			print(list(reversed(list2)))	
			print("mozliwe:")
			for i in range(0,len(list1)):
				if list2[i]>0:
					print(list1[i])
		return tops
