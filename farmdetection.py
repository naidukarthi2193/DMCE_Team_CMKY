import cv2
 
img = cv2.imread('saatbara.png')
 
cv2.imshow('sample image',img)
 
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() 