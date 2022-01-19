from os import chdir,listdir, system, getcwd, path
from cv2 import imread, imshow, imwrite, getRotationMatrix2D, warpAffine, add
import numpy as np

#With 2 images it is possible to generate 22 new images
'''For the rotation, the interesting thing is that the image has a shape and dimension
square not to lose proportion'''
 
#save images function ('Local', 'image.png')
def save (nome,imgRotation):
    imwrite(nome,imgRotation)

#Angle to rotate image
angle = [90,180]

#path local 'Windows'
get_root = getcwd()
#Normalize local path to unix path
Norm_root = get_root.replace("\\","/")


#Location of images
Input = Norm_root +'/Input'

#location to save the images
Output = Norm_root+ '/Output'

       

#name to concatenate with input image name
Namesave=['/90','/180','/Q','/Q90','/Q180']
TestNoise = ['/NN','/N90','/N180','/NQ','/NQ90','/NQ180']

#It is important to keep the amount of values ​​in the Namesave array equivalent to operations1, and the TestNoise to operations2
#_______________________________________________________________

#.os library function for reading data in directory
directory = listdir(Input)

#chdir changes the current working directory to the given path Input
chdir(Input)

for image in directory:
        #load the image into Input       
        img = imread(image)
        
        height, width = img.shape[:2]
        point = (width / 2, height / 2) #point in the center of the figure

        #angle for rotation    
        spin90 = getRotationMatrix2D(point, angle[0], 1)
        spin180 = getRotationMatrix2D(point, angle[1], 1)
        
        #rotated image   
        rotation90 = warpAffine(img, spin90, (width, height))
        rotation180 = warpAffine(img, spin180, (width, height))
        #----------------------------------------------------------
        #quantify image
        r =64
        img_quant = np.uint8(img/r)*r
        img_quant90 = np.uint8(rotation90/r)*r
        img_quant180 = np.uint8(rotation180/r)*r

        
        #----------------------------------------------------------
        gauss = np.random.normal(0,1,img.size)
        gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
        
        #Noisy image
        Noiseimg = add(img,gauss)
        Noiseimg90 = add(rotation90,gauss)
        Noiseimg180 = add(rotation180,gauss)
        NoiseimgQ = add(img_quant,gauss)
        NoiseimgQ90 = add(img_quant90,gauss)
        NoiseimgQ180 = add(img_quant180,gauss)
        
        operations1 = [(rotation90),(rotation180),(img_quant),(img_quant90),(img_quant180)]
        operations2 = [(Noiseimg),(Noiseimg90),(Noiseimg180),(NoiseimgQ),(NoiseimgQ90),(NoiseimgQ180)]
        
        #operations 1 saved
        for Nameimg in Namesave:
            for i in range(len(Nameimg)):
                save(Output+Nameimg+image,operations1[i])

        
        #operations 2 saved
        for Nameimg in TestNoise:
            for i in range(len(TestNoise)):
                save(Output+Nameimg+image,operations2[i])
                
                
print('Operation complete!!')
print('Check Output folder')
      


