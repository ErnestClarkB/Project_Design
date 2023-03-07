import numpy as np
import cv2

def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def find_area(img,imgContour):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    area_cnt = 0
    area_sum = 0
    for cnt in contours:
        area =  float(cv2.contourArea(cnt))
        area_sum =+ area
        area_cnt = area_cnt +1
        #area_index = contours.index(cnt)
        #print("Area %i = %f" %(area_index,area))
        #print("Area %i = %f" %(area_cnt,area))

        if area>150000:

            cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)

            approx = cv2.approxPolyDP(cnt,0.02*peri,True)

            objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
            

            obj = "Papaya"
            if objCor >7 and peri >1500:
                cv2.rectangle(imgContour,((x),(y)),(x+w,y+h),(0,255,0),2)
                cv2.putText(imgContour,obj,(x+170,y+170) ,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
            
    return (area_sum)

def getContours(img,imgContour):

    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    area_cnt = 0
    area_sum = 0
    for cnt in contours:
        area =  float(cv2.contourArea(cnt))
        area_sum =+ area
        area_cnt = area_cnt +1
        #area_index = contours.index(cnt)
        #print("Area %i = %f" %(area_index,area))
        #print("Area %i = %f" %(area_cnt,area))
        cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)

    return (area_sum)

        
        
        

def process_image(HSV,img):
    kernel = np.ones((5,5),np.uint8)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower = np.array(HSV[:3])
    upper = np.array(HSV[3:])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    #imgBlank = np.zeros_like(img)
    #imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgContour = img.copy()

    imgCanny = cv2.Canny(imgResult,100,100)#50,50
    imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)

    return (img,imgResult,imgContour,imgCanny,imgDialation,mask)

def results(orig):
    
    img,imgresult,imgContour,imgCanny,imgDialation,mask = orig
    imgStack = stackImages(0.4,([img,imgresult],
                            [imgCanny,imgDialation],
                            [mask,imgContour]))

    return imgStack

def result_stack(images):
    orig, result, green, yellow = images
    stack = stackImages(0.6,([orig,result],[green,yellow]))

    return stack
def findColor(img,color_HSV,color):
    img2Contour = img.copy()
    Orig = process_image(color_HSV,img)

    contours,hierarchy = cv2.findContours(Orig[4],cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    area_cnt = 0
    color_area_sum = []
    for cnt in contours:
        area =  float(cv2.contourArea(cnt))
        cv2.checkHardwareSupport
        color_area_sum.append(area)
        area_cnt = area_cnt +1
        #area_index = contours.index(cnt)
        #print("Area %i = %f" %(area_index,area))
        #print("Area %i = %f" %(area_cnt,area))
        cv2.drawContours(img2Contour,cnt,-1,(255,0,0),3)

    #cv2.imshow("Green",Orig[1])
    return (sum(color_area_sum),img2Contour,Orig[1])


    #cv2.imshow("Contour",)
    imgStack = results(Orig)


    return (color_area,imgStack)
def nonZero(img):
    pixel_nonzero = 0

    for i in range (499):
        for h in range(499):
            z = img[i][h]
            for t in range(3):
                q = img[i][h][t]
                if q > 0:
                    pixel_nonzero = pixel_nonzero + 1
    return pixel_nonzero
                