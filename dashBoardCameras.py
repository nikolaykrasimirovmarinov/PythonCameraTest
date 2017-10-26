import time
import os
import socket
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

isConnected=False
while not isConnected:
    isConnected=False
    try:
        print >>sys.stderr, '\n Trying to connect to IP: %s, Port: %s' %(TCP_IP,TCP_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        isConnected=True
    except:
        print >>sys.stderr, '\n Unable to connect!'
        isConnected=False
        time.sleep(0.5)

    if not isConnected:
        continue

    countEmptyData=0

    while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data = sock.recv(BUFFER_SIZE)
        print >>sys.stderr, 'received %s bytes' % (len(data))
        print >>sys.stderr, data

        if len(data) == 0:
            countEmptyData = countEmptyData + 1

        if countEmptyData == 3:
            isConnected=False
            sock.close()
            break;
   

        if data and len(data) > 4:
            countEmptyData = 0
            dataArray = data.split(",@\x00")
            print dataArray
            for item in dataArray:
                dataItem = item[4:]
                ds = dataItem.split(",")
                print ds
                if len(ds) == 5: 

                    if (ds[4] == "1" and ds[0] == "On"):
                        bashCommand = "fswebcam -r 640x480 image-" + str(time.time()) + ".jpg -S 20"
                        os.system(bashCommand)

                    if (ds[4] == "2" and ds[0] == "On"):
                        bashCommand = "timeout 60 avconv -f video4linux2 -r 30 -s 640x480 -i /dev/video0 test" + str(time.time()) + ".avi"
                        os.system(bashCommand)

                    if (ds[4] == "0" and ds[0] == "On"):
                        bashCommand = "sudo fswebcam -d /dev/video1 -r 640x480 image-r-" + str(time.time()) + ".jpg -S 20"
                        os.system(bashCommand)

                    if (ds[4] == "3" and ds[0] == "On"):
                        bashCommand = "sudo timeout 60 avconv -f video4linux2 -r 30 -s 640x480 -i /dev/video1 test-r" + str(time.time()) + ".avi"
                        os.system(bashCommand)
