'''
This migrates the old file system, which had too many subdirectories and divisions, to a newer, cleaner one.
'filter' variable restricts the copying to the main clients' files.
'''

import os, shutil, errno
proj_list, work, fdict = [], [], {}
filter = 'AESY一'
filecounter = 0
dropbox = 'c:\\'
path = dropbox + 'Dropbox (Pavilion)\\R&D Team\\'
wrkpath = 'C:\\Dropbox (Pavilion)\\R&D Team\\Admin\\Scripts\\'
skipped = []

def copydir(src, dest, symlinks=False, ignore=None):
	'''copy only files (not subdirectories) in src to dest'''
	global filecounter, skipped
	if not os.path.exists(dest):
		os.makedirs(dest)
	#	print('copydir created', dest)
	try:
		for item in os.listdir(src):
			s = os.path.join(src, item)
			d = os.path.join(dest, item)
			if os.path.isdir(s):
				skipped.append(s)
				continue
			else:
				if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
	#				print('{}'.format(d))
					filecounter += 1
					shutil.copy2(s, d)
	except:
	#	print('not found:', src)
		skipped.append(src)
		pass

def with_open(_file, _var, _type):
	'''Store a return-separated (_file), in a (_var), of (_type: 'list' / 'dict')'''
	with open(wrkpath+_file, 'r') as opened:
		if _type == 'list':
			for x in opened:
				x = x.rstrip()
				if not x: continue
				_var.append(x)
		if _type == 'dict':
			for x in opened:
				x = (x.rstrip()).split(',')
				for c, j in enumerate(x):
					if c == 0: k = j
					if c == 1: v = j
				_var[k] = v

def migrate(path):
	'''
	Revise folder structure. Care is taken to copy only the folders we want, and no subdirectories.
	'''
	global filecounter, skipped
	with_open('FolderDestinationDict.txt', fdict, 'dict')
	with_open('WorkFolders.txt', work, 'list')
	
	# This chunk gets a list of the project dirs in each clients' folder, skipping other dir types.
	for c, i in enumerate(work):
		proj_list.append([])
		for j in next(os.walk(path + i))[1]:
			if j[0] in filter and j.lower() != 'admin':
				proj_list[c].append(j)
			if i.lower() == 'archived projects\\':
				proj_list[c].append(j)
	
	# This chunk copies the subs and files to the destinations mapped in the dict file.
	for c, i in enumerate(work):
		for j in proj_list[c]:
			for k in list(fdict):	
				src = path + i + j + '\\' + k + '\\'
				dest = 'c:\\temp\\' + i + j + '\\' + fdict[k].lstrip()
				copydir(src, dest)
			
			#This chunk copies the versions of files in the 3D folder.
			versions = []			
			try:
				for m in next(os.walk(path + i + j + '\\Assets\\3D\\'))[1]:
					if m[0].lower() == 'v':
						versions.append(m)
			except:
				pass
			for v in versions:
				src = path + i + j + '\\Assets\\3D\\' + v + '\\'
				dest = 'c:\\temp\\' + i + j + '\\3D\\' + v + '\\'
				copydir(src, dest)
			
			#This makes a new folder in each project called Renders.
			try: 					
				os.makedirs('c:\\temp\\' + i + j + '\\Renders')
			except:
				pass

	print('filecounter: {}'.format(filecounter))
	print('skipped: {}'.format(len(skipped)))
	s = input('enter s to see skipped list: ')
	if s == 's':
		for i in skipped: 
			print('skipped: {} \r'.format(i))
	
migrate(path)
s = input('press enter to quit')
if s != '': quit()
