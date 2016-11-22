#! /usr/bin/python
########################################################################
# Downloads and compiles a hostfile using multiple sources from the net.
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import urllib2, os, re, sys, json, datetime
from socket import gethostname
from socket import gethostbyname
########################################################################
# create global to store system arguments passed though shell
def currentDirectory():
	currentDirectory = os.path.abspath(__file__)
	temp = currentDirectory.split(os.path.sep)
	currentDirectory = ''
	for item in range((len(temp)-1)):
		if len(temp[item]) != 0:
			currentDirectory += os.path.sep+temp[item]
	return (currentDirectory+os.path.sep)
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def loadFile(fileName):
	try:
		print "Loading :",fileName
		fileObject=open(fileName,'r')
	except:
		print "Failed to load :",fileName
		return "FAIL"
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	print "Finished Loading :",fileName
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return fail
	return False
########################################################################
def loadSourcesFile(primaryFilePath,secondaryFilePath):
	hostfiles = []
	# try to load first path, then second and if it does not exist
	# create the second path with contentForEmptyConfig
	print 'Loading source files...'
	if os.path.exists(primaryFilePath):
		# primary file path used for installed program resources
		temp = str(loadFile(primaryFilePath)).split('\n')
		for line in temp:
			if line[:1] != '#' and line != '':
				hostfiles.append(line)
	elif os.path.exists(secondaryFilePath):
		# secondary file path used for debuging on not fully installed program
		temp = str(loadFile(secondaryFilePath)).split('\n')
		for line in temp:
			if line[:1] != '#' and line != '':
				hostfiles.append(line)
	else:
		# if neither file exists
		print "ERROR: No config files exist!"
	#return the hostfiles in a array
	return hostfiles
########################################################################
def downloadFile(fileAddress):
	try:
		print "Downloading :",fileAddress
		downloadedFileObject = urllib2.urlopen(str(fileAddress))
	except:
		print "Failed to download :",fileAddress
		return "FAIL"
	lineCount = 0
	fileText = ''
	for line in downloadedFileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount+=1
	downloadedFileObject.close()
	print "Finished Loading :",fileAddress
	return fileText
########################################################################
def convertFilename(inputFileName):
	temp = ''
	inputFileName = re.sub('[&=]','',inputFileName)
	temp += inputFileName.split('/')[2] # domain name
	temp += '_'
	if '?' in inputFileName:
		temp += ((str(inputFileName.split('/')[len(inputFileName.split('/'))-1])).split('?')[0])
	else:
		temp += (str(inputFileName.split('/')[len(inputFileName.split('/'))-1]))
	temp = temp.replace('.','_')
	temp = temp.replace('/','_')
	temp += '.host'
	return temp
########################################################################
def downloadFileWithBackup(fileAddress):
	# use download url first
	orignalAddress = fileAddress
	fileContent = downloadFile(fileAddress)
	primaryBackupAddress = os.path.join('/etc','hostfileBlocklist','localBackupFiles',str(convertFilename(fileAddress)))
	alternateBackupAddress = os.path.join(currentDirectory(),'localBackupFiles',convertFilename(fileAddress))
	if fileContent == "FAIL":
		# if download fails load installed backup
		print 'Attempting to load backup at:',primaryBackupAddress
		fileContent = loadFile(primaryBackupAddress)
		if fileContent == "FAIL":
			# if backup  fails try local backup folder
			print 'Attempting to load alternate backup at:',alternateBackupAddress
			fileContent = loadFile(alternateBackupAddress)
			if fileContent == False:
				print ('ERROR: Could not download "'+orignalAddress+'" or backup at "'+fileAddress+'" or alternate backup at "'+alternateBackupAddress)
				return False
			else:
				return fileContent
		else:
			return fileContent
	else:
		# if success return file text and write file to backups,
		# remove last element of path since its the filename and write
		# path if it dont exist
		primaryBackupPath = primaryBackupAddress.split('/')
		primaryBackupPath.pop()
		primaryBackupPath = (os.sep).join(primaryBackupPath)
		if os.path.exists(primaryBackupPath) != True and os.name != 'nt':
			# if directory doesnt exist create it recursivley
			os.makedirs(primaryBackupPath)
		writeFile(primaryBackupAddress,fileContent)
		return fileContent
########################################################################
def downloadArrayOfHostfiles(arrayName):
	# loads an array of filenames and returns a string of them all combined
	temp = ''
	compiledHostfileText = ''
	for fileAddress in arrayName:
		if fileAddress[:4] == 'http':# check if online file address
			temp = downloadFileWithBackup(fileAddress)
			#~ if temp != "FAIL" and temp != None:
			if temp != "FAIL":
				compiledHostfileText += temp
		else:# if not grab localy stored hostfile
			temp = loadFile(os.path.join(os.path.abspath(os.curdir),"localBackupFiles",fileAddress))
			if temp != "FAIL":
				compiledHostfileText += temp
	return compiledHostfileText
########################################################################
def downloadArrayOfDomainFiles(arrayName):
	# loads a array of localy stored files returns a string
	temp = ''
	compiledText = ''
	for fileAddress in arrayName:
		# if the file is stored online somewhere
		if fileAddress[:4] == 'http':
			temp = downloadFileWithBackup(fileAddress)
			if temp != "FAIL": # checks that document loaded correctly
				compiledText += temp
		else:
			# if the file is local just load the file
			temp = loadFile('/etc/hostfileBlocklist/localBackupFiles'+str(fileAddress))
			if temp != "FAIL": # checks that document loaded correctly
				compiledText += temp
	# split the text into an array
	temp = compiledText.split('\n')
	for line in temp:
		# remove comments from text
		if line[:1] != '#':
			compiledText += line+'\n'
	# return comment cleaned string of text, seprated by newlines
	return compiledText
########################################################################
def buildListOfDomains():
	# some variables
	compiledHostfileText = '\n\n'
	####################################################################
	# Primary online host file resources to use for compile #
	####################################################################
	filePath = os.path.join('/etc','hostfileBlocklist','hostfiles.source')
	secondFilePath = os.path.join(os.path.abspath(os.curdir),'sources','hostfiles.source')
	hostfiles = loadSourcesFile(filePath,secondFilePath)
	####################################################################
	# domain lists that must be converted to hostfile format#
	####################################################################
	filePath = os.path.join('/etc','hostfileBlocklist','domainLists.source')
	secondFilePath = os.path.join(os.path.abspath(os.curdir),'sources','domainLists.source')
	domainLists = loadSourcesFile(filePath,secondFilePath)
	####################################################################
	# after loading sources, download the files
	compiledHostfileText = downloadArrayOfHostfiles(hostfiles)
	# remove commented lines in text
	print 'Removing commented lines...'
	temp = compiledHostfileText.split('\n')
	compiledHostfileText = ''
	for line in temp:
		if line[:1] != '#':
			#return only the names of the hosts,ignore comments
			compiledHostfileText += line+'\n'
	# clean up hostfile before save
	print 'Converting tabs to spaces...'
	#convert tabs to spaces for compatibility
	compiledHostfileText = re.sub('\t',' ',compiledHostfileText)
	print 'Converting endline formats...'
	#convert returns to newlines for compatibility
	compiledHostfileText = re.sub('\r','\n',compiledHostfileText)
	#convert ^M to newlines for compatibility
	compiledHostfileText = re.sub('^M','\n',compiledHostfileText)
	# convert redirects to 0.0.0.0
	compiledHostfileText = compiledHostfileText.replace('127.0.0.1','\n0.0.0.0')
	# strip www. from begining of entries(this is for later)
	compiledHostfileText = compiledHostfileText.replace('www.','')
	print 'Removing broken lines...'
	compiledHostfileText = compiledHostfileText.replace('#',' ')
	# bad entry that apears after filter of hostfile
	compiledHostfileText = compiledHostfileText.replace('::1 localhost IPv6','')
	# split and recombine the hostfile to remove extra spacing that was missed
	print "Removing empty lines..."
	while re.search('\n\n',compiledHostfileText) != None:
		compiledHostfileText = re.sub('\n\n','\n',compiledHostfileText)
	print 'Removing extra spaces...'
	while re.search('  ',compiledHostfileText) != None:
		compiledHostfileText = re.sub('  ',' ',compiledHostfileText)
	temp = compiledHostfileText.split('\n')
	temp2 = []
	compiledHostfileText = ''
	for line in temp:
		temp2 = line.split(' ')
		if len(temp2)>1 and temp2[1] != 'localhost':
			#return only the names of the hosts
			compiledHostfileText += str(temp2[1])+'\n'
		temp2 = []
	# remove remaining spaces that would cause errors
	compiledHostfileText = re.sub(' ','',compiledHostfileText)
	# sort the hostfile
	print 'Spliting text for sort...'
	temp = compiledHostfileText.split('\n')

	domainTexts=downloadArrayOfDomainFiles(domainLists).split('\n')
	print 'Adding domain files...'
	for line in domainTexts:
		if line[:1] != '#':
			temp.append(line)
	# remove protected domains from list
	print 'Removing protected domains from list...'
	if os.path.exists(os.path.join('/etc/','hostfileBlocklist','protectedDomains.source')):
		protectList = loadFile(os.path.join('/etc/','hostfileBlocklist','protectedDomains.source')).split('\n')
	elif os.path.exists(os.path.join('sources','protectedDomains.source')):
		protectList = loadFile(os.path.join('sources','protectedDomains.source')).split('\n')
	else:
		print 'Could not load protected domains list...'
		protectList = []
	compiledHostfileText = temp
	temp = []
	# if test == true the domain is protected so dont add it to the blocklist
	# www. is added to check to make protect list smaller
	for line in compiledHostfileText:
		if line[:1] != '#': # this skips lines with # at start for comments
			test = False
			for line2 in protectList:
				if line == line2:
					test = True
				elif line == ('www.'+line2):
					test = True
			if test == False:
				temp.append(line)
	print 'Adding "www." variation to all entries...'
	for line in temp:
		# only add www. to entrys that dont have it
		if line[:4] != 'www.':
			temp.append('www.'+line)
			# if this creates dupes they will be removed next
	print 'Removing duplicated entries and preforming sort...'
	temp = list(sorted(set(temp)))#remove dupes
	# retrun a sorted and dedupd list
	return temp
########################################################################
def configLoad(filePath):
	# loads a file that has a json config stored to it
	temp = loadFile(filePath)
	if temp != False:
		return json.loads(temp)
	else:
		print 'ERROR: failed to load file',filePath
		return False
########################################################################
def recombineList(listOfDomains,optimizeFileCheck):
	# optimize does a trick for hostfiles where you can place 8 hosts on one
	# line redirecting to one ip address, this makes hostfile reads faster
	if optimizeFileCheck == True:
		compiledHostfileText = ''
		lineCount = 0
		for line in listOfDomains:
			if (lineCount % 8) == 0:
				compiledHostfileText += '\n0.0.0.0 '
			compiledHostfileText += line+' '
			lineCount += 1
			sys.stdout.write(str('Optimized '+str(lineCount)+' lines...\r'))
		print 'File optimize completed!'
		return compiledHostfileText
	else:
		compiledHostfileText = ''
		lineCount = 0
		for line in listOfDomains:
			compiledHostfileText += '\n0.0.0.0 '+line
			sys.stdout.write(str('Recombined '+str(lineCount)+' lines...\r'))
			lineCount += 1
		print 'File recombine completed!'
		return compiledHostfileText
########################################################################
def buildPrivoxyBlocklist(listOfDomains):
	# making privoxy blocklist
	'''Takes a list of domain names to be built in current working directory'''
	temp = []
	# take out the www. varation since privoxy uses varaible names
	for domainName in listOfDomains:
		if domainName != None:
			# remove www. from entries since privoxy uses the . like *.
			domainName = domainName.replace('www.','.')
			# check if line starts with . if not add it to start and append
			# to the new array
			if domainName[:1] == '.':
				temp.append(domainName)
			else:
				temp.append('.'+domainName)
	# sort and dedupe the temp array
	listOfDomains = list(sorted(set(temp)))#remove dupes
	#write top of privoxy blocklist text
	privoxyHostfileText = '{ +block }'
	lineCount = 0
	for domainName in listOfDomains:
		privoxyHostfileText += '\n'+domainName
		sys.stdout.write(str('Recombined '+str(lineCount)+' lines for privoxy blocklist...\r'))
		lineCount += 1
	# write privoxy blocklist to same directory
	writeFile(os.path.join(os.path.abspath(os.curdir),'privoxyHostfile.host'),privoxyHostfileText)
########################################################################
def buildRedirects():
	if os.path.exists('/etc/hostfileBlocklist/redirectList.source'):
		configFileContent = loadFile(os.path.join('/etc','hostfileBlocklist','redirectList.source')).split('\n')
	else:
		configFileContent = loadFile(os.path.join('sources','redirectList.source')).split('\n')
	temp = '\n############################################################\n'
	temp +='# Redirect List,For manually specified routing in hostfile #\n'
	temp +='############################################################\n'
	if configFileContent == False:
		print 'ERROR: config file redirectList.source could not be loaded!'
		return False
	else:
		for entry in configFileContent:
			if entry[:1] != '#' and entry != '\n' and entry != '':
				#simply pile up the entrys since they consist of hostfile format
				temp += entry + '\n'
	return temp
########################################################################
def buildUnblocks():
	if os.path.exists('/etc/hostfileBlocklist/unblockList.source'):
		configFileContent = loadFile(os.path.join('/etc','hostfileBlocklist','unblockList.source')).split('\n')
	else:
		configFileContent = loadFile(os.path.join('sources','unblockList.source')).split('\n')
	temp = '\n############################################################\n'
	temp +='# Unblock List, for routing around simple blocking methods #\n'
	temp +='############################################################\n'
	if configFileContent == False:
		print 'ERROR: config file unblockList.source could not be loaded!'
		return False
	else:
		for entry in configFileContent:
			if entry[:1] != '#' and entry != '\n' and entry != '':
				#simply pile up the entrys since they consist of hostfile format
				print 'Building unblock entry for :',entry
				try:
					temp += gethostbyname(entry)+' unblock'+entry+' www.unblock'+entry+'\n'
				except:
					print 'ERROR: could not get IP of',entry
	return temp
########################################################################
def installHostfile(commands):
	# load main config file
	if os.path.exists(os.path.join('/etc','hostfileBlocklist','config.source')):
		configData = configLoad(os.path.join('/etc','hostfileBlocklist','config.source'))
	else:
		configData = configLoad(os.path.join('sources','config.source'))
	#download and build a list of domains then combine and optimize domains
	#into a hostfile
	listOfDomains = buildListOfDomains()
	# write hostfile to backups for merge with next iteration if installed to /etc/hostfileBlocklist,otherwise localy write
	if os.path.exists(os.path.join('/etc','hostfileBlocklist')):
		writeFile(os.path.join('/etc','hostfileBlocklist','previousHostfile.host'),'\n'.join(listOfDomains))
	else:
		writeFile(os.path.join(os.path.abspath(os.curdir),'localBackupFiles','previousHostfile.host'),'\n'.join(listOfDomains))
	if ('-p' in commands) or ('--privoxy' in commands):
		buildPrivoxyBlocklist(listOfDomains)
	#recombine list with optimize turned on
	compiledHostfileText = recombineList(listOfDomains,True)
	# adding needed entrys to top and metadata
	print 'Adding contextual info to top of file...'
	temp = ''
	temp += '# Hostfile compiled by HackBox hostfile script\n'
	temp += '# The following sources were used by the script\n'
	temp += '################################################\n'
	# write the sources for the hostfiles to hostfile as comments
	if os.path.exists('/etc/hostfileBlocklist/hostfiles.source'):
		for line in loadFile('/etc/hostfileBlocklist/hostfiles.source').split('\n'):
			# check for comments or blank lines
			if line[:1] != '#' and line != '':
				temp += '# '+line + '\n'
	else:
		for line in loadFile(os.path.join('sources','hostfiles.source')).split('\n'):
			if line[:1] != '#' and line != '':
				temp += '# '+line + '\n'

	temp += '################################################\n'
	# comment to show when hostfile was compiled
	currentTime = datetime.datetime.now()
	temp += '# Hostfile last compiled at '
	temp += (str(currentTime).split(' ')[1].split('.')[0])
	temp +=' on '+ (str(currentTime).split(' ')[0]) +'\n'
	temp += '################################################\n'
	if os.name != 'nt':
		temp += '127.0.1.1 '+gethostname()+'\n'
	temp += '127.0.0.1 localhost #IPV4\n'
	temp += '::1 localhost #IPV6\n'
	temp += '################################################\n'
	compiledHostfileText = temp + compiledHostfileText
	# build redirects and unblocks and add to hostfile if they work
	buildSuccess = buildRedirects()
	if buildSuccess != False:
		compiledHostfileText += buildSuccess
	buildSuccess = buildUnblocks()
	if buildSuccess != False:
		compiledHostfileText += buildSuccess

	compiledHostfileText = compiledHostfileText.replace('0.0.0.0 ',(str(configData['routeToIp'])+' '))
	temp = None
	if ('-d' in commands) or ('--debug' in commands):
		#create a debug hostfile for testing purposes
		compiledHostfile = open('debugHostfile.txt','w')
		print '========================================================'
		print '====================== DEBUG MODE ======================'
		print '========================================================'
		print '== DEBUG FILE WILL BE WROTE NAMED "debugHostfile.txt" =='
		print '========================================================'
		# if debug flag set exit here and write hosts file localy
	# determine install method based on a Operating System check
	elif os.name == 'nt': #if run on windows
		# DNS service no longer disables the hostfile on windows 7 and up
		# commands will not show up on window CLI unless printed before launched
		# set install location for windows systems of hosts file
		compiledHostfile = open((os.environ['WINDIR']+'/system32/drivers/etc/hosts'),'w')
	elif os.name == 'posix': # if run on linux
		# install into location
		compiledHostfile = open('/etc/hosts','w')
	# write data to hostsfile
	print 'Writing the text to file...'
	compiledHostfile.write(compiledHostfileText)
	compiledHostfile.close()
	print "SUCCESS!!!!! :D The Hostsfile was successfully compiled and installed to the system!"
########################################################################
def main(argv):
	# before run check os and privlages if nessary, only if not in debug mode
	if (('-h' in argv)==True) or (('--help' in argv)==True):
		print "HostfileBlocklist builds a hostfile by aggerating multiple sources"
		print "Copyright (C) 2016  Carl J Smith"
		print ""
		print "This program is free software: you can redistribute it and/or modify"
		print "it under the terms of the GNU General Public License as published by"
		print "the Free Software Foundation, either version 3 of the License, or"
		print "(at your option) any later version."
		print ""
		print "This program is distributed in the hope that it will be useful,"
		print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
		print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
		print "GNU General Public License for more details."
		print ""
		print "You should have received a copy of the GNU General Public License"
		print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
		print "#############################################################"
		print "-h or --help"
		print "    Displays this menu"
		print "-d or --debug"
		print "    Builds a hostfile and saves it to the current working directory"
		print "    as a text file. When ran this way the program will not install"
		print "    the hostfile to the system."
		print "-p or --privoxy"
		print "    Builds a blocklist using the hostfile sites that is compatible"
		print "    with the privoxy proxy server."
		print '#############################################################'
	else:
		# still need to check if on windows or linux
		if os.name == 'nt': #if run on windows
			try:
				# check if running as admin my opening a system file
				open((os.environ['WINDIR']+'/system32/drivers/etc/hosts'),'w').close()
				# if success then run the program and exit
				installHostfile(argv)
			except:
				# if program is not run as admin print error and exit
				print 'ERROR: program is not being run as adminstrator, please launch the program as a adminstrator!'
		elif os.name == 'posix': # if run on linux confirm the user is root
			if os.geteuid() != 0:
				print 'ERROR: Run the program as root...'
			else:
				# if run as root
				installHostfile(argv)
########################################################################
