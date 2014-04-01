show:
	echo 'Run "make install" as root to install program!'
	
run:
	python hostfileblocklist-gui.py
install:
	sudo apt-get install transmission-gtk --assume-yes
	sudo cp hostfileblocklist-gui.py /usr/bin/hostfileblocklist-gui
	sudo chmod +x /usr/bin/hostfileblocklist-gui
uninstall:
	sudo rm /usr/bin/hostfileblocklist-gui
installed-size:
	du -sx --exclude DEBIAN ./debian/
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/usr/share;
	mkdir -p debian/usr/share/applications;
	cp -vf hostfileblocklist-gui.desktop ./debian/usr/share/applications/
	# make post and pre install scripts have the correct permissions
	chmod 775 debdata/*
	# copy over the binary
	cp -vf hostfileblocklist-gui.py ./debian/usr/bin/hostfileblocklist-gui
	# make the program executable
	chmod +x ./debian/usr/bin/hostfileblocklist-gui
	# start the md5sums file
	md5sum ./debian/usr/bin/hostfileblocklist-gui > ./debian/DEBIAN/md5sums
	md5sum ./debian/usr/share/applications/hostfileblocklist-gui.desktop >> ./debian/DEBIAN/md5sums
	# create md5 sums for all the config files transfered over
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	du -sx --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.]//g" > packageSize.txt
	dpkg-deb --build debian
	cp -v debian.deb ../hostfileblocklist-gui_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
