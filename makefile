show:
	echo 'Run "make install" as root to install program!'
run:
	python hostfileBlocklist
install:
	sudo cp hostfileBlocklist.py /usr/bin/hostfileBlocklist
	sudo chmod +x /usr/bin/hostfileBlocklist
	sudo mkdir /etc/hostfileBlocklist/
	sudo cp sources/*.source /etc/hostfileBlocklist/
	sudo cp localBackupFiles/*.* /etc/hostfileBlocklist/
	sudo link /usr/bin/hostfileBlocklist /etc/cron.monthly/hostfileupdater
uninstall:
	sudo rm -r /etc/hostfileBlocklist/
	sudo rm /usr/bin/hostfileBlocklist
	sudo rm /etc/cron.monthly/hostfileupdater
installed-size:
	du -sx --exclude DEBIAN ./debian/
build:
	sudo make build-deb
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/etc/hostfileBlocklist
	# make post and pre install scripts have the correct permissions
	chmod 775 debdata/postinst
	chmod 775 debdata/postrm
	# copy over the binary
	cp -vf hostfileBlocklist.py ./debian/usr/bin/hostfileblocklist
	cp -vfr localBackupFiles/. ./debian/etc/hostfileBlocklist
	cp -vfr sources/. ./debian/etc/hostfileBlocklist
	# make the program executable
	chmod +x ./debian/usr/bin/hostfileblocklist
	# start the md5sums file
	md5sum ./debian/usr/bin/hostfileblocklist > ./debian/DEBIAN/md5sums
	# create md5 sums for all the config files transfered over
	md5sum ./debian/etc/hostfileBlocklist/* >> ./debian/DEBIAN/md5sums
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	# the below can not be done in make, bash variables wont work
	#size=$(du -sx --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.]//g")
	#du -sx --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.\\t]\{1,\}//g" > ./debdata/packagesize
	#sed -i.bak 's/Installed-Size: [0123456789]\{2,20\}/Installed-Size: $(more ./debdata/packagesize)/g' ./debdata/control
	#~ rm -v ./debdata/control.bak
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	dpkg-deb --build debian
	cp -v debian.deb hostfileblocklist_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
