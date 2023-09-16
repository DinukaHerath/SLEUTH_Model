import numpy as np

class UrbanUnit:
    #Defing the attributes of the object assigned at the creation of the object
    def __init__(self,IDx,IDy,ID_Number,Urbanization,neighbour_ids_l1,neighbour_ids_l2, slope, exclusion, road_effect):
        self.IDx=IDx
        self.IDy=IDy
        self.ID_num=ID_Number
        self.neighbour_ids_l1=neighbour_ids_l1
        self.neighbour_ids_l2=neighbour_ids_l2
        self.Urbanization=Urbanization
        self.slope=slope
        self.exclusion=exclusion
        self.road_effect=road_effect
        self.Urbanization_spontaneous=0
        self.Urbanization_spreading_center=0
        self.Urbanization_edge=0
        self.Urbanization_roadgravity=0

    #Function to print the object if necessary in the development process   
    def __str__(self):
        return f"{self.IDx}{self.IDy}({self.Urbanization}{self.slope}{self.exclusion}{self.road_effect}{self.neighbour_ids_l1}{self.neighbour_ids_l2})"    
    
    #Function to get an array of object attributes when cell object array is formed
    def Get_property_array(Cell_array,property_to_get,dimensionX,dimensionY):
        property_layer=np.zeros((dimensionX,dimensionY))
        for i in range(len(Cell_array)):
            x=Cell_array[i].IDx
            y=Cell_array[i].IDy
            property_layer[x][y]=getattr(Cell_array[i],property_to_get)
        return property_layer
    

    
    #Create an array consists of UrbanUnit Objects using the inputs 
    def Create_Urban_Object_array(dimensionX,dimensionY,UrbanizationStateArray,HillShadeArray,ExclusionArray,Road_eff):
        ID_generator=1
        Cell_array=[]
        
        Cell_IDs=np.zeros((dimensionX,dimensionY),dtype=int)
        for i in range(dimensionX):
            for j in range(dimensionY):
                Cell_IDs[i][j]=int(ID_generator)
                ID_generator=ID_generator+1
                
        L1_Neighbours=np.zeros((dimensionX,dimensionY),dtype=list)
        L2_Neighbours=np.zeros((dimensionX,dimensionY),dtype=list)
        L1_list=[]
        L2_list=[]
        
        #Local function to evaluate the capabiltiy to create the cell objects based on the neighbouring cells
        def try_cell(k,l,list1):
            try:
                if k>=0 and l>=0:
                    val=list1[k][l]
                    return val
                else:
                    val=0
                    return val
            except:
                val=0
                return val
        
        #Obtaining the neighbour ID for a certain cell
        for i in range(dimensionX):
            for j in range(dimensionY): 
                n_list=[try_cell(i-1, j-1, Cell_IDs),try_cell(i, j-1, Cell_IDs),try_cell(i+1, j-1, Cell_IDs),try_cell(i-1, j, Cell_IDs),try_cell(i+1, j, Cell_IDs),try_cell(i-1, j+1, Cell_IDs),try_cell(i, j+1, Cell_IDs),try_cell(i+1, j+1, Cell_IDs)]
                
                # Creating level 1 neighbours list
                L1_list = [x for x in n_list if x != 0]
                L1_Neighbours[i][j]=L1_list
                
                n_list_2=[try_cell(i-2,j-2,Cell_IDs),try_cell(i-2,j-1,Cell_IDs),try_cell(i-2,j,Cell_IDs),try_cell(i-2,j+1,Cell_IDs),try_cell(i-2,j+2,Cell_IDs),try_cell(i-1,j-2,Cell_IDs),try_cell(i-1,j+2, Cell_IDs),try_cell(i,j-2,Cell_IDs),try_cell(i,j+2,Cell_IDs),try_cell(i+1,j-2,Cell_IDs),try_cell(i+1,j+2,Cell_IDs),try_cell(i+2,j-2,Cell_IDs),try_cell(i+2,j-1,Cell_IDs),try_cell(i+2,j,Cell_IDs),try_cell(i+2,j+1,Cell_IDs),try_cell(i+2,j+2,Cell_IDs)]
                
                # Creating level 2 neighbours list
                L2_list = [x for x in n_list_2 if x != 0]
                L2_Neighbours[i][j]=L2_list
        
        #Creating a one dimensional array of cell objects with the attributes provided at the initialization           
        for i in range(dimensionX):
            for j in range(dimensionY):
                Cell_object=UrbanUnit(i, j, Cell_IDs[i][j], UrbanizationStateArray[i][j], L1_Neighbours[i][j], L2_Neighbours[i][j], HillShadeArray[i][j], ExclusionArray[i][j], Road_eff[i][j])
                Cell_array.append(Cell_object)
        print('Object array for cells was Created')
        return Cell_array
    #Get Properties from Object Array
    
    
    

        

