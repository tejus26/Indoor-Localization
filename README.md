# Indoor-Localization
Indoor Localization using Arduino and DWM1000 Modules

The project is developed by Albert Davies, Anirban Ghosh and Tejus Siddagangaiah from CMU. 

The project aims to localize a mobile node in an indoor setting with known localtions of 
anchor nodes.

A laptop can communicate with TAG using Serial Port or WiFi to gather the ranges from each
ANCHOR node and perform localization computation and plot the location on a 3D plot.

Folder Structure:  

	Arduino:  
		+DWM1000 modified library  
		+Arduino code for TAG and ANCHOR nodes  
		+Arduino code for WiFi Communication  
	GUI:   
		+ serial_gui.py: Python script for localization and serial communication with TAG  
		+ wifi_comm.py : Python script for localization and wifi communication with TAG  
