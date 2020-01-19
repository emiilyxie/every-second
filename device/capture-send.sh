# run both functions at once -- capturing and uploading
nohup /usr/bin/python3 /home/pi/everysecond/capture-picture.py > /dev/null 2>&1 &
nohup ./upload-img.sh > /dev/null 2>&1 &
