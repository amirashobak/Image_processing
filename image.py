import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while( cap.isOpened() ) :
    ret,img = cap.read()
    #rectangle
    cv2.rectangle(img, (500,500), (100,100), (0,255,0),0)
    crop_img = img[100:500, 100:500]

    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
    #contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, hierarchy, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(crop_img.shape,np.uint8)

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) 
                cy = int(moments['m01']/moments['m00']) 
              
    centr=(cx,cy)       
    cv2.circle(crop_img,centr,5,[0,0,255],2)       
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)
    
    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    cv2.line(crop_img,start,end,[0,255,0],2)
                    
                    cv2.circle(crop_img,far,5,[0,0,255],-1)
               print(i)
               if(i==2):
               	    cv2.putText(img,"2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               if(i==1):
               	    cv2.putText(img,"1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               if(i==3):
               	    cv2.putText(img,"3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               if(i==4):
               	    cv2.putText(img,"4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               if(i==5):
               	    cv2.putText(img,"5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               i=0
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('output',drawing)
    cv2.imshow('input',crop_img)
                
    k = cv2.waitKey(10)
    if k == 27:
        break