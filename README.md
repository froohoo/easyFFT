# easyFFT
Simple Audio Analysis and Display Utility

##Background
This is my proof of concept sound analysis / signal processing tool that I wrote in support of my larger project to train a neural network to identify audio signatures from aircraft. 

##Usage
Just run the easyFFT.py script. See the top of the script for dependencies. You will likely need to update the device since your hardware configuration is unlikely to match mine. 
To determine your device, run <b> alrecord -l</b> and replace the DEVICE setting with hw:X,Y for your device, where X=Card #, and Y = Subdevice #.
