import numpy as np
import cv2

#Function to read continius images
def ConvertImagetoContiniousMatrix(location):
    image = cv2.imread(location,1)
    img = np.array(image)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    interval_min = 0
    interval_max = 1
    sample_mat=gray_image
    scaled_mat = ((sample_mat - np.min(sample_mat)) /( (np.max(sample_mat)) - np.min(sample_mat)))* (interval_max - interval_min) + interval_min
    scaled_mat=abs(scaled_mat-1)
    print('Image Converted to continious array:',location)
    return scaled_mat

#Function to read binary images    
def ReadBinaryImage(file_name,cuttoff=200):
    image = cv2.imread(file_name,1)
    img = np.array(image, dtype=np.uint8)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, cuttoff, 255, cv2.THRESH_BINARY)
    blackAndWhiteImage=blackAndWhiteImage/255
    print('Image Converted to binary array : ', file_name)
    return blackAndWhiteImage  

#Function to obtain image resolution
def GetImageResolution(file_name):
    dimensions=[]
    image = cv2.imread(file_name,1)
    height = image.shape[0]
    width = image.shape[1]
    dimensions.append(height)
    dimensions.append(width)
    print('Image dimensions achieved')
    return dimensions

#Function to get the domain border of the region
def GetDomainBorder(Domain_matrix):
    x,y=Domain_matrix.shape
    domain_border=np.zeros((x,y))
    for j in range(x):
        for k in range(y):
            if j!=0 and k!=0 and j!=x-1 and k!=y-1:
                if 1<=Domain_matrix[j-1][k]+Domain_matrix[j+1][k]+Domain_matrix[j][k-1]+Domain_matrix[j][k+1]<=2:
                    domain_border[j][k]=1
                else:
                    domain_border[j][k]=0
    print('Domain Border Created')
    return domain_border

#Function to calculate the road effect matrix
def RoadEffects_Calc(dimensionX,dimensionY,Road):
    Road_effect=np.zeros((dimensionX,dimensionY))

    for j in range(dimensionX):
        for k in range(dimensionY):
            if j>2 and k>2 and j<dimensionX-3 and k<dimensionY-3:
                Road_Neighbours=[Road[j-1][k-1],Road[j][k-1],Road[j+1][k-1],Road[j-1][k],Road[j+1][k],Road[j-1][k+1],Road[j][k+1],Road[j+1][k+1]]
                Secondary_Neighbours=[Road[j-2][k-2],Road[j-2][k-1],Road[j-2][k],Road[j-2][k+1],Road[j-2][k+2],Road[j-1][k-2],Road[j-1][k+2],Road[j][k-2],Road[j][k+2],Road[j+1][k-2],Road[j+1][k+2],Road[j+2][k-2],Road[j+2][k-1],Road[j+2][k],Road[j+2][k+1],Road[j+2][k+2]]
                Road_Neighbours=Road_Neighbours+Secondary_Neighbours
                #print(Road_Neighbours)
                sum_of_neighbours=0
                for cell in Road_Neighbours:
                    sum_of_neighbours=sum_of_neighbours+cell
                if sum_of_neighbours>=1:
                    if Road[j][k]==1:
                        continue
                    else:
                        Road_effect[j][k]=sum_of_neighbours 
        
    highest_effect=np.amax(Road_effect)
    Road_effect=((Road_effect/highest_effect))
    Road_effect=Road_effect
    print('Road Effects calculated')
    return Road_effect

#Function to form exclusion layer merging different images
def Form_exclusion_layer(Layers_to_merge,dimensionX,dimensionY,exclude_values):
    merged_array=np.zeros((dimensionX,dimensionY))
    for i in range(dimensionX):
        for j in range(dimensionY):
            pixel_l=[]
            for c in range(len(Layers_to_merge)):
                pixel_l.append(Layers_to_merge[c][i][j])
            if pixel_l==exclude_values:
                new_pixel=0
            else:
                new_pixel=1
            merged_array[i][j]=new_pixel
    print('Exclusion Layer was formed')
    return merged_array