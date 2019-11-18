# run both functions at once -- capturing and uploading
/usr/bin/python3 /home/pi/everysecond/capture-picture.py 2>&1 /dev/null  &
./upload-img.sh 2>&1 /dev/null &
