#include <stdlib.h>
#include <iostream>

using namespace std;

int main(){
	// this is a simple program that works as a launcher for the python
	// script when it is ran on windows, It allows the user to right click
	// and hit run as adminstrator to run the program.
	cout << "#############################################################\n";
	cout << "!!!PROGRAM MUST BE RUN AS A ADMINSTRATOR TO WORK CORRECTLY!!!\n";
	cout << "#############################################################\n";
	system("C:\\\\python27\\python.exe hostfileBlocklist.py");
	cout << "Press enter to close the program...\n";
	cin.get();
	return 0;
}
