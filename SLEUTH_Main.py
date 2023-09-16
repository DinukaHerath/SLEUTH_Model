import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import imageio
#from SLEUTH_Read_Image import *
#import SLEUTH_Read_Image
#import SLEUTH_Rules
#from SLEUTH_Rules import *
import SLEUTH_Modeling
#from SLEUTH_initialization import Get_property_array

#from SLEUTH_initialization.SLEUTH_init import UrbanUnit

#%%
#Image Directory
directory_in='E:\Dinuka\Projects\ENS\ENS_Project\Images'
directory_out='E:\Dinuka\Projects\ENS\ENS_Project\Python Script\Images\Test_Run_4_07_12'

#Defining the files to be considered as input images
HillShade_file_name=directory_in+'\Munich_Hillshade.tif'
Exclusion_file_name =directory_in+'\Munich_Exclusion_protectarea.tif'
Road_file_name =directory_in+'\Munich_Road2020.tif'
Urbanization_file_name =directory_in+'\Munich_Urban.tif'

#Read the road network as a binary input
RoadArray=SLEUTH_Modeling.SLEUTH_Read_Image.ReadBinaryImage(Road_file_name)

#Read the exclusion status as a binary input
ExclusionArray=SLEUTH_Modeling.SLEUTH_Read_Image.ReadBinaryImage(Exclusion_file_name)


#Read the Urbanization state as a binary input
UrbanizationStateArray=SLEUTH_Modeling.SLEUTH_Read_Image.ReadBinaryImage(Urbanization_file_name)

#Generate the domain from the input images
DomainArray=SLEUTH_Modeling.SLEUTH_Read_Image.ReadBinaryImage(HillShade_file_name,cuttoff=254)

#Generate the hillshade from the input images
HillShadeArray=SLEUTH_Modeling.SLEUTH_Read_Image.ConvertImagetoContiniousMatrix(HillShade_file_name) 

#Get the border of the Domain
DomainBorder=SLEUTH_Modeling.SLEUTH_Read_Image.GetDomainBorder(DomainArray)

#Get the dimensions of the input images
dimensionX,dimensionY=SLEUTH_Modeling.SLEUTH_Read_Image.GetImageResolution(HillShade_file_name)

#Evaluate the road effects layer from the road network layer
Road_eff=SLEUTH_Modeling.SLEUTH_Read_Image.RoadEffects_Calc(dimensionX,dimensionY, RoadArray)

#Plot Exclusion input image
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(ExclusionArray,"Exclusion")
plt.show()
#Plot Road network input image
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(RoadArray, 'Road Network') 
plt.show()

#Creating exclusion layer with Road network and Exclusion layer
Layers=[ExclusionArray,RoadArray]
exclude=[0,0]            
ExclusionArray=SLEUTH_Modeling.SLEUTH_Read_Image.Form_exclusion_layer(Layers,dimensionX,dimensionY,exclude)

#Generating images of the layers which are taken as inputs to the model
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.Write_processed_layers(directory_out, ExclusionArray, RoadArray, UrbanizationStateArray, HillShadeArray)   

#Plotting Domain image
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(DomainArray,"Domain") 
plt.savefig(directory_out+'Domain_image.png',dpi=600) 
plt.show() 

#Plotting New Exclusion image.
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(ExclusionArray,"Exclusion_Merged")  
plt.savefig(directory_out+'Exclusion Merged_image.png',dpi=600) 
plt.show()

#Creating the Cell object array with use of input layers
Cell_arr=SLEUTH_Modeling.UrbanUnit.Create_Urban_Object_array(dimensionX,dimensionY,UrbanizationStateArray,HillShadeArray,ExclusionArray,Road_eff)

#%% Coefficients

dispersion=0.01                     #Spontaneous Growth
slope_resistance=0.9                #Effect of Slope in to Urbanization
K_breed=0.2                         #Urban Center formation
K_spread=0.2                        #Edge Growth
K_roadgravity=0.7                   #Road Gravity


#Other Coefficients
spontaneous_settlements=50          #Spontaneous Growth
Total_settlements=100               #Spontaneous Growth

time_steps=100                      #Number of timesteps

X=6                                 #Number of Urban Cells required to Urbanize under Spreading Center rule
Y=5                                 #Number of urban Cells required to Urbanize under Edge Growth
Z1=10                               #Maximum number of cells Urbanized under Road Gravity rule in a timestep


#%%
#PU_in=np.zeros((dimensionX,dimensionY)) #Defining initial Layer
PU_in=UrbanizationStateArray
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(PU_in, 'PU_in')
plt.show()

#Defining output Layer
PU_out=np.zeros((dimensionX,dimensionY))  

#Slope_Layer=DefineSlopeLayer(dimensionX,dimensionY,slope_resistance) #Defining Slope Layer
Slope_Layer=HillShadeArray
SLEUTH_Modeling.SLEUTH_Plot_Write_Image.PlotLayers(Slope_Layer, 'Slope')
plt.show()

#Defining Road Effects
plt.imshow(Road_eff,cmap='binary')
plt.title("Road Effect")
plt.colorbar()
plt.savefig(directory_out+'Road Effects_image.png',dpi=600) 
plt.show()

#Getting road effects layer and calculating the slope gravity matrix
Road_effect_dyn=Road_eff

PU_slope=SLEUTH_Modeling.SLEUTH_Rules.PU_Slope_calc(slope_resistance,Slope_Layer,dimensionX,dimensionY)
PU_sg_out= SLEUTH_Modeling.SLEUTH_Rules.SlopeGravityCalc(dispersion, spontaneous_settlements, Total_settlements, PU_slope)

#Generating exclusion layer
Exclude=ExclusionArray
Cell_arr_tn=Cell_arr
frames=[]

#%%

for t in range(time_steps):
    if t==0:
        Cell_arr_tn=Cell_arr
        print('Starting SLEUTH @ timestep : 0')
        
    
    else:
        z=1
        cell_ID=0

        max_roadeffect=max(map(max, Road_effect_dyn))
        
        print('Time Step Increased to :', t)

        for j in range(dimensionX):
            for k in range(dimensionY):
                r=SLEUTH_Modeling.SLEUTH_Rules.Generate_Random_No(1000)
                
                if DomainArray[j][k]==1:
                    if Cell_arr[cell_ID].IDx==j and Cell_arr[cell_ID].IDy==k:
                        Cell_arr_tn[cell_ID].Urbanization=Cell_arr[cell_ID].Urbanization
                        Road_effect_dyn[j][k]=0
                        cell_ID=cell_ID+1
                        continue
             
                else:
                    if Cell_arr[cell_ID].Urbanization==1:
                        Cell_arr_tn[cell_ID].Urbanization=Cell_arr[cell_ID].Urbanization
                        
                    elif Cell_arr[cell_ID].exclusion==1:
                        Cell_arr_tn[cell_ID].Urbanization=Cell_arr[cell_ID].Urbanization

                    
                    elif Cell_arr[cell_ID].Urbanization_spontaneous==1:
                        Cell_arr_tn[cell_ID].Urbanization_spontaneous=Cell_arr[cell_ID].Urbanization_spontaneous

                        
                    elif Cell_arr[cell_ID].Urbanization_spreading_center==1:
                        Cell_arr_tn[cell_ID].Urbanization_spreading_center=Cell_arr[cell_ID].Urbanization_spreading_center

                      
                    elif Cell_arr[cell_ID].Urbanization_edge==1:
                        Cell_arr_tn[cell_ID].Urbanization_edge=Cell_arr[cell_ID].Urbanization_edge

                        
                    elif Cell_arr[cell_ID].Urbanization_roadgravity==1:
                        Cell_arr_tn[cell_ID].Urbanization_roadgravity=Cell_arr[cell_ID].Urbanization_roadgravity

                        
                    else:    
                        Cell_arr_tn[cell_ID].Urbanization_spontaneous=SLEUTH_Modeling.SLEUTH_Rules.Spontaneous_Growth_Rule(r,PU_sg_out[j][k],Cell_arr[cell_ID])
                        Cell_arr_tn[cell_ID].Urbanization_spreading_center=SLEUTH_Modeling.SLEUTH_Rules.SpreadingCenter_rule(K_breed,X,r,Cell_arr[cell_ID],Cell_arr)
                        Cell_arr_tn[cell_ID].Urbanization_edge=SLEUTH_Modeling.SLEUTH_Rules.EdgeGrowth_rule(r, Y, K_spread,PU_slope[j][k],Cell_arr[cell_ID],Cell_arr )
                        Cell_arr_tn[cell_ID].Urbanization_roadgravity=SLEUTH_Modeling.SLEUTH_Rules.RoadGravity_rule(r,K_roadgravity,Road_effect_dyn[j][k],max_roadeffect,PU_slope[j][k],Cell_arr[cell_ID],z,Z1)[0]
                        z=SLEUTH_Modeling.SLEUTH_Rules.RoadGravity_rule(r,K_roadgravity,Road_effect_dyn[j][k],max_roadeffect,PU_slope[j][k],Cell_arr[cell_ID],z,Z1)[1]
                    Road_effect_dyn[j][k]=0                    
                cell_ID=cell_ID+1
    
    Urb_layer_initial=SLEUTH_Modeling.UrbanUnit.Get_property_array(Cell_arr_tn,'Urbanization',dimensionX,dimensionY)
    Urb_layer_spontaneous=SLEUTH_Modeling.UrbanUnit.Get_property_array(Cell_arr_tn,'Urbanization_spontaneous',dimensionX,dimensionY)
    Urb_layer_spreadingcenter=SLEUTH_Modeling.UrbanUnit.Get_property_array(Cell_arr_tn,'Urbanization_spreading_center',dimensionX,dimensionY)
    Urb_layer_edgegrowth=SLEUTH_Modeling.UrbanUnit.Get_property_array(Cell_arr_tn,'Urbanization_edge',dimensionX,dimensionY)
    Urb_layer_roadinfluenced=SLEUTH_Modeling.UrbanUnit.Get_property_array(Cell_arr_tn,'Urbanization_roadgravity',dimensionX,dimensionY)

    cmap = matplotlib.colors.ListedColormap([ 'white','black','#653700','#6E750E','#00008B','r','c' ])
 
    PU_out=Urb_layer_initial+DomainBorder+2*Urb_layer_spontaneous+3*Urb_layer_spreadingcenter+4*Urb_layer_edgegrowth+5*Urb_layer_roadinfluenced
    PU_out_plot=PU_out
    plt.figure(figsize=(6,4),dpi=600)
    fig=plt.imshow(PU_out_plot, cmap=cmap)
    plt.title("Urbanization at timestep -"+str(t))
    plt.colorbar(orientation='vertical', label='Colours based on Growth type',shrink=0.5)
    plt.clim(0, 6)
    plt.legend([ 0,1,2,3,4,5,6])
    plt.savefig(directory_out+f'/{t}_image.png',dpi=600)
    
    plt.show()
    Cell_arr=Cell_arr_tn
    
#%%
with imageio.get_writer(directory_out+'/Animation_UE.gif', mode='I') as writer:
    for x in range(time_steps):
        image = imageio.imread(directory_out+f'/{x}_image.png')
        writer.append_data(image)

