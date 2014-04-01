########################################################################
# This dont do shit yet
# Copyright (C) 2013  Carl J Smith
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
import gzip
import sys
# after download read gziped file into memory
f = gzip.open('file.gz', 'rb')
file_content = f.read()
file_content = file_content.split('\n')
temp = ''
totalCount = len(file_content)
counterCount = 1.0
# pull out ip ranges stored in file
for index in file_content:
	sys.stdout.write(str(int((counterCount/totalCount)*100.0))+"%\r")
	if len(index.split(':'))==2:
		temp+=str(index.split(':')[1])+','
	counterCount+=1
file_content=temp[:-1]
sys.stdout.write('#### DONE ####')
f.close()
#convert ip address range into a command to add block to firewall
pass
#print content to screen for debug purposes
print file_content
