import cv2

image = cv2.imread("Feild.jpg")
print(image.shape)

resized = cv2.resize(image, (800, 800))
print(resized.shape)

yield_zones = {

}

for rows in range(40):
    for cols in range(40): 
        