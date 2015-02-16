#A simple game using token tracking using a camera

import numpy as np
import cv2
import pyttsx


def mapcolor(src, hue, tolerance):
    """Creates a map with the locations of +/-tolerance hue"""
    imgHSV = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) #Convert the captured frame from BGR to HSV
    iLowH = hue-tolerance
    iHighH = hue+tolerance
    iLowS = 50
    iHighS = 250
    iLowV = 50
    iHighV = 200
    out = cv2.inRange(imgHSV, np.array([iLowH, iLowS, iLowV]), np.array([iHighH, iHighS, iHighV])) #Threshold the image
    kernel = np.ones((1,1),np.uint8)
   #morphological opening (removes small objects from the foreground)
    out = cv2.erode(out, kernel, iterations=10 )
    out = cv2.dilate( out, kernel, iterations=10 )
   #morphological closing (removes small holes from the foreground)
    out = cv2.dilate( out, kernel, iterations=10 )
    out = cv2.erode(out, kernel, iterations=10 )
    return out



def mapshade( src, value, tolerance):
    """Creates a map wit the locations of +/-tolerance value"""
    imgHSV = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) #Convert the captured frame from BGR to HSV
    iLowH = 1
    iHighH = 179
    iLowS = 1
    iHighS = 255
    iLowV = value-tolerance
    iHighV = value+tolerance
    out = cv2.inRange(imgHSV, np.array([iLowH, iLowS, iLowV]), np.array([iHighH, iHighS, iHighV])) #Threshold the image
    kernel = np.ones((5,5),np.uint8)
  #morphological opening (removes small objects from the foreground)
    out = cv2.erode(out, kernel, iterations=1 )
    out = cv2.dilate( out, kernel, iterations=1 )
   #morphological closing (removes small holes from the foreground)
    out = cv2.dilate( out, kernel, iterations=1 )
    out = cv2.erode(out, kernel, iterations=1 )
    return out


def countshapes(src):
    """Returns the number of shapes in the map src"""
    imgray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    #finding all contours in the image.
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)


def findshape(src, n):
    """Returns the central point of the nth shape in map src"""
    temp1 = src
    #finding all contours in the image.
    contour, heirarchy = cv2.findContours( temp1, cv2.CV_RETR_LIST, cv2.CV_CHAIN_APPROX_SIMPLE)
    tmoment = cv2.moments(contour[n])
    shape = cv2.approxPolyDP(contour[n], arcLength(contour[n], 0)*0.1, 0)
    coord.x = tmoment.m10/tmoment.m00
    coord.y = tmoment.m01/tmoment.m00
    return coord


def findarea(src, n):
    """Returns the area of the nth shape in map src"""
    temp1 = src
    #finding all contours in the image.
    contour, heirarchy = cv2.findContours( temp1, cv2.CV_RETR_LIST, cv2.CV_CHAIN_APPROX_SIMPLE)
    tmoment = cv2.moments(contour[n])
    shape = cv2.approxPolyDP(contour[n], arcLength(contour[n], 0)*0.1, 0)
    area = tmoment.m00
    return area


def removecolor(src, hue, tolerance):
    """Removes the color given in hue"""
    imgThresholded = mapcolor(src, hue, tolerance)
    imgEdited = cv2.cvtColor(imgThresholded, cv2.COLOR_GRAY2BGR)
    imgGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2BGR)
    imgGray = cv2.bitwise_and(imgGray, imgEdited)
    imgEdited = cv2.bitwise_and(src, imgEdited)
    imgEdited = src - imgEdited + imgGray
    return imgEdited


def turn(timer, player):
    """Runs a turn for player of number "player" """
    worked=1;
    while(failure==1):
        print "It is "
        if player == 1:
            print "yellow\'s"
        elif player == 2:
            print "green\'s"
        elif player == 3:
            print "teal\'s"
        elif player == 4:
            print "blue\'s"
        elif player == 5:
            print "purple\'s"
        elif player == 6:
            print "red\'s"
        print " turn, please play your action card.\nPress any key after card has been played.\n"
        ret, startturn = cap.read()
        cv2.imshow("New Turn", startturn);
        cv2.waitKey(0);
        ret, endturn = cap.read()
        endturn = mapshade(endturn, 21, 20)
        shapes = countshapes(endturn)
        if shapes == 1: #Move
            timer[player] = timer[player] + movement(player*30)
            failure=0
        elif shapes == 2: #Fire
            targethue=huetarget(player*30)
            fire(player*30, targethue)
            timer[player]=timer[player]+3
            failure=0
        else:
            print "Error, misread action card. Please try again.\n"


def movement(hue):
    """Moves the player of the given hue to another location"""
    cap.read(startturn)
    print "You have chosen to move.\nPlease move your robot as far as you want and press any key.\n";
    cv2.waitKey(0)
    cap.read(endturn)
    mapcolor(endturn, endturn, hue, 10)
    mapcolor(startturn, startturn, hue, 10)
    startinglocation = findshape(startturn, 0)
    endinglocation = findshape(endturn,0)
    area = findarea(startturn, 0)
    distance = sqrt(((startinglocation.x-endinglocation.x)*(startinglocation.x-endinglocation.x))+((startinglocation.y-endinglocation.y)*(startinglocation.y-endinglocation.y)))
    print "You moved a distance of ", distance, ".\n"
    return distance/sqrt(area)


def huetarget(hue):
    """Allows the player to target a particular hue based on whichever is closest to the card"""
    while(Failure):
        cap.read(startturn)
        test = mapshade(startturn, 21, 20)
        targetlocation = findshape(startturn, 0)
        test = mapcolor(startturn, hue, 10)
        shooterlocation = findshape(test, 0)
        while n<=5:
            test = mapcolor(startturn, (hue+n*30)%180, 10)
            testlocation = findshape(test, 0)
            testdistance = sqrt(((targetlocation.x-testlocation.x)*(targetlocation.x-testlocation.x))+((targetlocation.y-testlocation.y)*(targetlocation.y-testlocation.y)))
            if testdistance<distance:
                distance = testdistance
                targethue = (hue+n*30)%180
            print "You fired at "
            if targethue == 30:
                print "yellow\'s"
            elif targethue == 60:
                print "green\'s"
            elif targethue == 90:
                print "teal\'s"
            elif targethue == 120:
                print "blue\'s"
            elif targethue == 150:
                print "purple\'s"
            elif targethue == 0:
                print "red\'s"
            print " robot!"
            n=n+1
        Failure=0
    return targethue


def testforplayer(n):
    """Test to see if there is a token for player n on the board"""
    ret, src = cap.read()
    size = src.shape
    out = np.zeros(size, dtype=np.uint8)
    out = mapcolor(src, (n*30)%180, 20)
    return countshapes(out)




#Main sequence

cap = cv2.VideoCapture(1)
while(1):

    # Take each frame
    _, frame = cap.read()
    cv2.imshow('original',frame)
    mapped = mapcolor(frame,120,30)
    blueless = removecolor(frame,120,30)

    cv2.imshow('mapped',mapped)
    cv2.imshow('edited',blueless)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
