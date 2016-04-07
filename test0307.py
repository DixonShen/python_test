__author__ = 'DixonShen'

import numpy as np
import cv2
import plate
cap = cv2.VideoCapture('C0002_198.mp4');
detector = plate.platedetect('us','/etc/openalpr/openalpr.conf','/home/liyang/Downloads/openalpr-2.2.0/runtime_data');

while(1):
    ret, new = cap.read()
    if ret == False: break
    detect_results = detector.compute(new)
    i = 0
    for plate in results['results']:
	    i += 1
	    print("Plate #%d" % i)
	    print("   %12s %12s" % ("Plate", "Confidence"))
	    for candidate in plate['candidates']:
	        prefix = "-"
	        if candidate['matches_template']:
	            prefix = "*"

	        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

cap.release()
cv2.destroyAllWindows()
