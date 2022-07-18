This is a readme file informing you about what the upload folder does:
Once a user submits a pcap file using the front page it is then sent to this /upload folder.
Here it will stay and be proccessed by the python script 'app.py', which is hosted upon a flask server.
This will then process the pcap file and extract all useful data to be used later on.
Once this process is complete, the upload folder will be emptied: allowing for a non cluttered folder.
