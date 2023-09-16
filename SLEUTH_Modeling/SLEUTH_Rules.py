import numpy as np
import random

#Calculating probability of urbanization under slope
def PU_Slope_calc(slope_res,Slope_layer,dimensionX,dimensionY):
    PU_slope_out=np.zeros((dimensionX,dimensionY))
    for j in range(dimensionX):
        for k in range(dimensionY):
            PU_slope_out[j][k]=np.exp(-slope_res * Slope_layer[j][k])
    return PU_slope_out

#Calculating slope gravity
def SlopeGravityCalc(dispersion,spontaneous_settlements,Total_settlements,PU_S_Out):
    PU_S_Out=np.array(PU_S_Out)
    PU_sg_out=dispersion*spontaneous_settlements*PU_S_Out/Total_settlements
    return PU_sg_out

#Generating random number    
def Generate_Random_No(num_range):
    random_num=(random.randrange(0,num_range))
    r=random_num/num_range
    return r
    
#Evaluating spontaneous growth rule for a cell    
def Spontaneous_Growth_Rule(random_no,SlopeGravity,Cell):
    if random_no<=SlopeGravity:
        #print(Cell.Urbanization,'/',Cell.Urbanization_spontaneous,'/',Cell.Urbanization_spreading_center,'/',Cell.Urbanization_edge,'/',Cell.Urbanization_roadgravity)
        if Cell.Urbanization==0 and Cell.Urbanization_spontaneous==0 and Cell.Urbanization_spreading_center==0 and Cell.Urbanization_edge==0 and Cell.Urbanization_roadgravity==0:  
            new_sp=1
                        
        else:
            new_sp=Cell.Urbanization_spontaneous
            
    else:
        new_sp=Cell.Urbanization_spontaneous
    return new_sp

#Evaluating spreading center rule for a cell
def SpreadingCenter_rule(K_breed,X,r,Cell,Cell_array):
    neighbours=Cell.neighbour_ids_l1
    tot=0
    for ID in neighbours:
        Cell_n=Cell_array[ID-1]
        Urban_neighbours=(Cell_n.Urbanization+Cell_n.Urbanization_spontaneous+Cell_n.Urbanization_spreading_center+Cell_n.Urbanization_edge+Cell_n.Urbanization_roadgravity)
        tot=tot+Urban_neighbours
    sum_in_neighbours=tot
    if Cell.Urbanization_spreading_center==1:
        if sum_in_neighbours>=X:
            counter=1
            while counter<=X:
                if r<K_breed:
                    if Cell.Urbanization==0 and Cell.Urbanization_spontaneous==0 and Cell.Urbanization_spreading_center==0 and Cell.Urbanization_edge==0 and Cell.Urbanization_roadgravity==0:
                        PU_SC=1
                        break
    
                counter=counter+1
            if counter>X:    
                PU_SC=Cell.Urbanization_spreading_center
        else:
           PU_SC=Cell.Urbanization_spreading_center
    else:
        PU_SC=Cell.Urbanization_spreading_center
    return PU_SC

#Evaluating edge growth rule for a cell
def EdgeGrowth_rule(r,Marginal_Value,K_spread,PU_slope,Cell,Cell_array):
    neighbours=Cell.neighbour_ids_l1
    tot=0
    for ID in neighbours:
        Cell_n=Cell_array[ID-1]
        Urban_neighbours=(Cell_n.Urbanization+Cell_n.Urbanization_spontaneous+Cell_n.Urbanization_spreading_center+Cell_n.Urbanization_edge+Cell_n.Urbanization_roadgravity)
        tot=tot+Urban_neighbours
    sum_in_neighbours=tot 
    
    if (sum_in_neighbours)>=Marginal_Value:
        P_urban=K_spread*(PU_slope)
        if r<P_urban:
            if Cell.Urbanization==0 and Cell.Urbanization_spontaneous==0 and Cell.Urbanization_spreading_center==0 and Cell.Urbanization_edge==0 and Cell.Urbanization_roadgravity==0:
                PU_EG=1
            else:
                PU_EG=Cell.Urbanization_edge
        else:
            PU_EG=Cell.Urbanization_edge
    else:
        PU_EG=Cell.Urbanization_edge
    return PU_EG

#Evaluating road gravity rule for a cell
def RoadGravity_rule(r,K_roadgravity,Road_effect_dyn,max_roadeffect,PU_slope,Cell,z,Z1):
    Slope=PU_slope
    P_urban=K_roadgravity*Slope*Road_effect_dyn
    if max_roadeffect==Road_effect_dyn:
        #print(Road_effect_dyn)
        if r<P_urban:
            if z<=Z1:
                
                if Cell.Urbanization==0 and Cell.Urbanization_spontaneous==0 and Cell.Urbanization_spreading_center==0 and Cell.Urbanization_edge==0 and Cell.Urbanization_roadgravity==0:
                    PU_RG=1
                    Road_effect_dyn=0   
                    z=z+1
                else:
                    z=z+1
                    PU_RG=Cell.Urbanization_roadgravity
                    Road_effect_dyn=0
            else:
                PU_RG=Cell.Urbanization_roadgravity
        else:
            PU_RG=Cell.Urbanization_roadgravity
    else:
        PU_RG=Cell.Urbanization_roadgravity
        
    output=[PU_RG,z]   
    return output
        