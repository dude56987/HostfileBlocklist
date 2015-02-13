show:
	echo 'Run "make install" as root to install program!'
run:
	python hostfileBlocklist
install: build
	sudo gdebi --non-interactive hostfileblocklist_UNSTABLE.deb
	sudo gdebi --non-interactive hostfileblocklist-gui_UNSTABLE.deb
uninstall:
	sudo apt-get purge hostfileblocklist
	sudo apt-get purge hostfileblocklist-gui
installed-size:
	du -sx --exclude DEBIAN ./debian/
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/etc/hostfileBlocklist
	# copy over the binary
	cp -vf hostfileBlocklist.py ./debian/usr/bin/hostfileblocklist
	cp -vfr localBackupFiles/. ./debian/etc/hostfileBlocklist/localBackupFiles
	cp -vfr sources/. ./debian/etc/hostfileBlocklist
	# make the program executable
	chmod +x ./debian/usr/bin/hostfileblocklist
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size	
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	# copy over package data
	cp -rv debdata/. debian/DEBIAN/
	# fix permissions in package
	chmod -Rv 775 debian/DEBIAN/
	chmod -Rv ugo+r debian/
	chmod -Rv go-w debian/
	chmod -Rv u+w debian/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb hostfileblocklist_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
