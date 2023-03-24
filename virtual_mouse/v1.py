import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
pTime=0
detector = htm.handDetector(maxHands=1)

frameR = 100 # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
#######
wCam , hCam = 640,480
######
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
wScr, hScr = autopy.screen.size()

while(cap.isOpened()):
        # Read each frame where ret is a return boollean value(True or False)
        ret, frame = cap.read()
        # if return is true continue because if it isn't then frame is of NoneType in that case you cant work on that frame
        if ret:
            frame = detector.findHands(frame)
            lmList, bbox = detector.findPosition(frame)
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
            fingers = detector.fingersUp()
            print(fingers)

            cv2.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR),
                           (255, 0, 255), 2)
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, frame)
                print(length)
                # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(frame, (lineInfo[4], lineInfo[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()


            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            cv2.imshow('frame', frame)
            # finally write your preprocessed frame into your output video
           # out_video.write(gray) # write the modifies frame into output video
            # to forcefully stop the running loop and break out, if it doesnt work use ctlr+c
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
       # break out if frame has return NoneType this means that once script encounters such frame it breaks out
       # You will get the error otherwise
        else:
            break
