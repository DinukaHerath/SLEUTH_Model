import matplotlib.pyplot as plt
import matplotlib.colors
import cv2

#Ploting layers obtained in data or intermediate stages
def PlotLayers(LayerName,Plot_title):
    cmap1 = matplotlib.colors.ListedColormap([ 'white','black'])
    plt.imshow(LayerName, cmap=cmap1)
    plt.colorbar()
    plt.title(Plot_title)
    plt.clim(0, 1)
    
#Creating images of the data layers provided in to the model
def Write_processed_layers(file_location,ExclusionArray,RoadArray,UrbanizationStateArray,HillShadeArray):
    cv2.imwrite(file_location+'\Munich_Exclusion_Out.png', ExclusionArray*255)
    cv2.imwrite(file_location+'\Munich_Road_Out.png', RoadArray*255)
    cv2.imwrite(file_location+'\Munich_U_State_Out.png', UrbanizationStateArray*255) 
    cv2.imwrite(file_location+'\Munich_Hillshade.png', HillShadeArray*255)
    