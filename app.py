from flask import Flask, send_from_directory, jsonify, request, make_response, json, redirect
from flask_cors import CORS, cross_origin
import os
import dpkt
import datetime
import time
import pandas as pd


upload = "static/upload"
allow ={".pcap"}
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = upload
app.config["ALLOWED_EXTENSIONS"] = allow

#Route for javascript
@app.route("/JS/<file>")
def sendJava(file):
    return app.send_static_file("JS/" + file)


#Route for landing html page
@app.route('/')
def sendUsers():
    return app.send_static_file("user.html")

#Route for css
@app.route("/CSS/<file>")
def sendCss(file):
    return app.send_static_file("CSS/" + file)

@app.route("/test")
def test():
    return "I work"

def pcap_summary(file):

    print(f"[!] Initialising variables for data!")
    time.sleep(1)
    # Create a nested dictionary for values of each protocol type
    pro_dict = {
        "tcp": {"count": 0, "ts_first": "", "ts_last": "", "length": 0, "mean": 0},
        "udp": {"count": 0, "ts_first": "", "ts_last": "", "length": 0, "mean": 0},
        "igmp": {"count": 0, "ts_first": "", "ts_last": "", "length": 0, "mean": 0},
    }
    # Initialise a counter, so we can find the total amount of packets
    packet_total = 0

    # For each timestamp and buffer in the pcap file, increment the packet counter, set variables
    for ts, buf in file:
        packet_total += 1
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        protocol = ip.p

        # Upon looking at this I realised it would get very messy to have multiple if statements.
        # Having an if statement for each protocol would take up to much space and time.
        # I looked up python case statements to solve this problem. However it seems python does not support this.
        # To do this in python i would have to have seperate functions for each evaluation of protocol. This also seems messy.
        # So for now i am going to stick with if statements.
        # Verify protocol to know where to insert values in the dictionary
        if protocol == 6:
            pro_dict["tcp"]["count"] += 1
            pro_dict["tcp"]["ts_last"] = str(datetime.datetime.utcfromtimestamp(ts))
            pro_dict["tcp"]["length"] += len(buf)
            pro_dict["tcp"]["mean"] = round(
                pro_dict["tcp"]["length"] / pro_dict["tcp"]["count"], 2
            )
            if pro_dict["tcp"]["count"] == 1:
                pro_dict["tcp"]["ts_first"] = str(
                    datetime.datetime.utcfromtimestamp(ts)
                )
        elif protocol == 17:
            pro_dict["udp"]["count"] += 1
            pro_dict["udp"]["ts_last"] = str(datetime.datetime.utcfromtimestamp(ts))
            pro_dict["udp"]["length"] += len(buf)
            pro_dict["udp"]["mean"] = round(
                pro_dict["udp"]["length"] / pro_dict["udp"]["count"], 2
            )
            if pro_dict["udp"]["count"] == 1:
                pro_dict["udp"]["ts_first"] = str(
                    datetime.datetime.utcfromtimestamp(ts)
                )
        elif protocol == 2:
            pro_dict["igmp"]["count"] += 1
            pro_dict["igmp"]["ts_last"] = str(datetime.datetime.utcfromtimestamp(ts))
            pro_dict["igmp"]["length"] += len(buf)
            pro_dict["igmp"]["mean"] = round(
                pro_dict["igmp"]["length"] / pro_dict["igmp"]["count"], 2
            )
            if pro_dict["igmp"]["count"] == 1:
                pro_dict["igmp"]["ts_first"] = str(
                    datetime.datetime.utcfromtimestamp(ts)
                )
    # Output helpful comments to console for user
    # Add a delay so the user can see the output
    print(f"[!] Data created!")
    print(f"[!] Organising data to a table!")
    time.sleep(1)
    df = pd.DataFrame(pro_dict)
    df = df.transpose()
    # Remove the length field of all protocols as this was not part of the display output needed for the coursework
    print(f"[!] Removing excess data!")
    print()
    del df["length"]
    print(df)
    # Add a final delay so the user inspect the table
    time.sleep(6)
    return True





@app.route("/upload", methods=["POST"])
def uploadFile():
    if request.method == "POST":
        file = request.files["file"]
        extension = os.path.splitext(file.filename)
        if extension[1] in app.config["ALLOWED_EXTENSIONS"]:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            pcapFunctions(file.filename)
            return "Works!"
        else:
            return redirect("/")


def openFile(filename):
    filepath = os.getcwd() + "\\static\\upload\\" + filename
    stream = open(filepath, "rb")
    stream.seek(0, 0)
    pcap = dpkt.pcap.Reader(stream)
    return pcap

def pcapFunctions(filename):
    pcap = openFile(filename)
    pcap_summary(pcap)
    return True


if __name__ == '__main__':
    app.run(debug=True)


