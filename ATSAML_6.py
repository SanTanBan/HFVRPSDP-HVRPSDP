import time
import pandas as pd
import matplotlib.pylab as plt
import os
from random import random,randint,shuffle
import GeneRead
from math import pow,exp,floor,ceil
import numpy as np
#from matplotlib.patches import Patch
#from scipy.stats import norm

def ATSAML_6(directory_details_for_saving="",directory_containing_Vehicle_Types_file="",directory_containing_Node_Locations_file="",directory_containing_Distance_Matrix_file="",Time_Constraint=99999999999999999999999999999999999999999999999):

    dir_name="ATSAML_6 Evaluation"
    os.mkdir(directory_details_for_saving+dir_name)
    directory_to_save_ATSAML_6_solution=directory_details_for_saving+dir_name+"/"
    Original_Cost=99999999999999999999999999999999999999999999999

    def SubArray_Transplant_Allowing_Operations(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        Upto_Len=len(Node_Sequence)
        sub_array=[]

        # Creating The Sub-Array [2 Ways:=> First is Sequential, 2nd is Arbitrary]
        if randint(-1,1):   # Way 1 is Taking a Random Length of Consequetive Elements
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
            #while random_point_2==random_point_1 or (random_point_1==0 and random_point_2==Upto_Len) or (random_point_1==Upto_Len and random_point_2==0):
                random_point_2=randint(0,Upto_Len)
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            # Removing the Sub-Array Elements
            for i in sub_array:
                Node_Sequence.remove(i)
        else:   # Way 2
            random_length_of_sub_array=randint(0,Upto_Len)
            for i in range(random_length_of_sub_array):
                position_of_element=randint(0,len(Node_Sequence)-1)
                sub_array.append(Node_Sequence[position_of_element])
                # Removing the Sub-Array Elements
                Node_Sequence.pop(position_of_element)
        
        # Performing Operations on the Sub Array
        if randint(-1,1):
            shuffle(sub_array)
        elif randint(-1,1):
            sub_array.reverse()

        # Performing Operations on the Node_Sequence withput the Sub-Array Elements
        if randint(-1,1):
            shuffle(Node_Sequence)
        elif randint(-1,1):
            Node_Sequence.reverse()
        
        # Insertion the Sub Array Elements [2 Ways:=> First is Single Bulk Insertion, 2nd is Random Insertion at Arbitrary Places]
        if randint(-1,1):   # Way 1 is inserting the Total Sub-Array in a Random Location in the Operated Node Sequence (By default this insertion is reversed)
            random_insertion_point=randint(0,len(Node_Sequence))
            for i in sub_array:
                Node_Sequence.insert(random_insertion_point,i)
        else:   # Way 2 is inserting individual Sub-Array Elements in Random Locations in the Node Sequence
            for i in range(len(sub_array)):
                random_insertion_point=randint(0,len(Node_Sequence))
                Node_Sequence.insert(random_insertion_point,sub_array[i])

        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def Adjacent_Swap(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        Upto_Len=len(Node_Sequence)-2
        if Upto_Len<0:
            return
        temp=randint(0, Upto_Len)
        Node_Sequence[temp]-=Node_Sequence[temp+1]
        Node_Sequence[temp+1]+=Node_Sequence[temp]
        Node_Sequence[temp]=Node_Sequence[temp+1]-Node_Sequence[temp]
        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def General_Swap(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        Upto_Len=len(Node_Sequence)-1
        if Upto_Len<1:
            return
        temp1=randint(0, Upto_Len)
        temp2=randint(0, Upto_Len)
        while temp2==temp1:
            temp2=randint(0, Upto_Len)
        temp=Node_Sequence[temp1]
        Node_Sequence[temp1]=Node_Sequence[temp2]
        Node_Sequence[temp2]=temp
        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element
    

    def Single_Insertion(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node

        Upto_Len=len(Node_Sequence)-1
        if Upto_Len<1:
            return
        ejection_point=randint(0, Upto_Len)
        element=Node_Sequence[ejection_point]
        del Node_Sequence[ejection_point]
        insertion_point=randint(0, Upto_Len)
        while insertion_point==ejection_point:
            insertion_point=randint(0, Upto_Len)
        Node_Sequence.insert(insertion_point,element)

        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element
    

    def Reversal(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        
        Node_Sequence.reverse()

        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def Shuffle_Random(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        
        shuffle(Node_Sequence)
        
        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def Linear_Cake_Cutting_and_Accumulation(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node

        Upto_Len=len(Node_Sequence)
        if Upto_Len<3:
            return

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            SubArray_Transplant_Allowing_Operations(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)            
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            Adjacent_Swap(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)            
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            General_Swap(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)            
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            Single_Insertion(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)            
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            Reversal(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if random()<0.3:
            random_point_1=randint(0,Upto_Len)
            random_point_2=randint(0,Upto_Len)
            while random_point_2==random_point_1:
                random_point_2=randint(0,Upto_Len)            
            if random_point_1>random_point_2:
                random_end_point=random_point_1
                random_start_point=random_point_2
            else:
                random_end_point=random_point_2
                random_start_point=random_point_1
            sub_array=Node_Sequence[random_start_point:random_end_point]
            Shuffle_Random(sub_array,is_Depot_within_sequence_as_First_Node=="N")
            for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def Linear_Cake_Cutting_once_without_Overlap(Node_Sequence,is_Depot_within_sequence_as_First_Node="Y"):
        if is_Depot_within_sequence_as_First_Node=="Y":
            First_Node_Depot=Node_Sequence[0]
            Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node

        Upto_Len=len(Node_Sequence)
        if Upto_Len<3:
            return

        random_point_1=randint(0,Upto_Len)
        random_point_2=randint(0,Upto_Len)
        while random_point_2==random_point_1:
            random_point_2=randint(0,Upto_Len)
        if random_point_1>random_point_2:
            random_end_point=random_point_1
            random_start_point=random_point_2
        else:
            random_end_point=random_point_2
            random_start_point=random_point_1

        sub_array=Node_Sequence[random_start_point:random_end_point]

        if random()<0.3:
            SubArray_Transplant_Allowing_Operations(sub_array,is_Depot_within_sequence_as_First_Node=="N")

        if random()<0.3:
            Adjacent_Swap(sub_array,is_Depot_within_sequence_as_First_Node=="N")

        if random()<0.3:
            General_Swap(sub_array,is_Depot_within_sequence_as_First_Node=="N")

        if random()<0.3:
            Single_Insertion(sub_array,is_Depot_within_sequence_as_First_Node=="N")

        if random()<0.3:
            Reversal(sub_array,is_Depot_within_sequence_as_First_Node=="N")

        if random()<0.3:
            Shuffle_Random(sub_array,is_Depot_within_sequence_as_First_Node=="N")
        
        for i,j in enumerate(sub_array):
                Node_Sequence[random_start_point+i]=j

        if is_Depot_within_sequence_as_First_Node=="Y":
            Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element




    def Decoding_Mechanism_0(Node_Sequence):

        def generating_Daughter_Edges(starting_Node,Vehicle_Type_used):
 
            DynamicCapacityLeft=[VQ[Vehicle_Type_used]]
            array_containing_Daughter_Edges=[]
            # Each Edge consists of its information in the form (From Node, To Node, Vehicle Type, Cost)

            Starting_Edge_Cost_from_Depot=VC[Vehicle_Type_used]+VS[Vehicle_Type_used]*C[Depot_First_Node,Node_Sequence[starting_Node+1],Vehicle_Type_used]
            Other_Edge_Costs=0
            
            for stopping_Node_of_Daughter_Edge in range(starting_Node+1,num_of_Nodes): # The Loop variable refers to the Ending Node of each Edge

                CapacityCheck=0
                #print(DynamicCapacityLeft[0])
                DynamicCapacityLeft[0]=DynamicCapacityLeft[0]-Deliveries[Node_Sequence[stopping_Node_of_Daughter_Edge]]
                DynamicCapacityLeft.append(Deliveries[Node_Sequence[stopping_Node_of_Daughter_Edge]]-PickUps[Node_Sequence[stopping_Node_of_Daughter_Edge]])
                for m in DynamicCapacityLeft:
                    CapacityCheck+=m
                    if CapacityCheck<0:
                        break
                if CapacityCheck<0:
                    break

                if stopping_Node_of_Daughter_Edge>(starting_Node+1):
                    Other_Edge_Costs+=VS[Vehicle_Type_used]*C[Node_Sequence[stopping_Node_of_Daughter_Edge-1],Node_Sequence[stopping_Node_of_Daughter_Edge],Vehicle_Type_used]

                Ending_Edge_Cost_to_Depot=VS[Vehicle_Type_used]*C[Node_Sequence[stopping_Node_of_Daughter_Edge],Depot_First_Node,Vehicle_Type_used]
                Total_Edge_Cost=Starting_Edge_Cost_from_Depot+Other_Edge_Costs+Ending_Edge_Cost_to_Depot

                array_containing_Daughter_Edges.append((starting_Node,stopping_Node_of_Daughter_Edge,Vehicle_Type_used,Total_Edge_Cost))
            
            return array_containing_Daughter_Edges # Each Edge is a Tuple of 4 elements containing (Origin Node, Destination Node, Vehicle Type, Cost)

        
        aa = np.random.normal(mu_of_a_b_c_d_e_f[0],sigma_of_a_b_c_d_e_f[0])            
        bb = np.random.normal(mu_of_a_b_c_d_e_f[1],sigma_of_a_b_c_d_e_f[1])
        cc = np.random.normal(mu_of_a_b_c_d_e_f[2],sigma_of_a_b_c_d_e_f[2])
        dd = np.random.normal(mu_of_a_b_c_d_e_f[3],sigma_of_a_b_c_d_e_f[3])
        ee = np.random.normal(mu_of_a_b_c_d_e_f[4],sigma_of_a_b_c_d_e_f[4])
        ff = np.random.normal(mu_of_a_b_c_d_e_f[5],sigma_of_a_b_c_d_e_f[5])

        num_of_Nodes=len(Node_Sequence)

        Depot_First_Node=Node_Sequence[0]
        if Node_Sequence[0]!=0:
            # This check is for the specific problem considered in the Paper
            for just_some_screen_space in range(99):
                print("EXCEPTION: Line 353 :Please Check Code")
            return
        # Node Sequence should be an array starting from 0th Node and containing other Node Indexes, example 0,1,8,6,7

        left_over_Vehicles_of_each_Type=VN.copy() # The VN dictionary is being copied
        for VT_name in VN:
            if VN[VT_name]==0:
                del left_over_Vehicles_of_each_Type[VT_name]

        # Each Edge Graph is a Tuple consisting of 1 Element 1 Array and 1 Dictionary:-
            # The ELEMENT is the Node Number of the present staring EDGE from which we shall start analysisng
            # The ARRAY contains the Edges present in it
                # Each Edge consists of its information in the form (From Node, To Node, Vehicle Type, Cost)
            # The DICTIONARY contains the details of the Vehicles which may be used of each Type
                # So a Dictionary {2:4,5:6} means that there are 4 Vehicles left of Type 2 and 6 Vehicles of Type 5
        set_of_Mother_Edge_Graphs=[(0,[],left_over_Vehicles_of_each_Type)]
        set_of_Final_Edge_Graphs=[] # Sets were replaced by arrays due to sets being unhashable when arrays are wihin them ?!?

        # This loop is for populating the Final Edge Graphs set
        while set_of_Mother_Edge_Graphs:

            set_of_Daughter_Edge_Graphs=[]
            for each_Edge_Graph in set_of_Mother_Edge_Graphs:

                array_containing_all_Daughter_Edges=[]
                for Vehicle_Type_considered in each_Edge_Graph[2]:
                    # Creating a function to obtain the Daughter Edges
                    # Send a Mother Edge Graph for each Vehicle Type to the function and obtain the array of the daughter Edges to be individually added to the Mother Edge for that Vehicle Type
                    if each_Edge_Graph[2][Vehicle_Type_considered]>0:  # Only calculating when a Vehicle is available
                        daughter_edges_of_specific_Vehicle_Type=generating_Daughter_Edges(each_Edge_Graph[0],Vehicle_Type_considered)
                        for i in daughter_edges_of_specific_Vehicle_Type:
                            array_containing_all_Daughter_Edges.append(i)

                array_of_Daughter_Edges=[]
                length_of_Daughter_array=len(array_containing_all_Daughter_Edges)
                if length_of_Daughter_array>=3:
                    # Logically  Accepting the Best Edges
                    potential_mother_edge=0
                    minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                    for i in array_containing_all_Daughter_Edges:
                        fixed_cost=VC[i[2]]
                        variable_cost=i[3]-VC[i[2]]
                        length=i[1]-i[0]
                        edge_minimization_objective=aa*pow(fixed_cost,bb)*pow(length,cc) + dd*pow(variable_cost,ee)*pow(length,ff)
                        if edge_minimization_objective<minimum_Distributed_Cost:
                            minimum_Distributed_Cost=edge_minimization_objective
                            potential_mother_edge=i
                    if potential_mother_edge!=0:
                        array_of_Daughter_Edges.append(potential_mother_edge)

                else:
                    array_of_Daughter_Edges=array_containing_all_Daughter_Edges


                all_Edges_in_Mother=each_Edge_Graph[1]
                for Daughter_Edge in array_of_Daughter_Edges:
                    next_starting_Node=Daughter_Edge[1]
                    all_Edges_in_Daughter=all_Edges_in_Mother.copy()
                    all_Edges_in_Daughter.append(Daughter_Edge)
                    left_over_Vehicles=each_Edge_Graph[2].copy()
                    Vehicle_Type_considered=Daughter_Edge[2]
                    left_over_Vehicles[Vehicle_Type_considered]=left_over_Vehicles[Vehicle_Type_considered]-1
                    if left_over_Vehicles[Vehicle_Type_considered]==0:
                        del left_over_Vehicles[Vehicle_Type_considered]


                    if next_starting_Node==num_of_Nodes-1:
                        set_of_Final_Edge_Graphs.append((all_Edges_in_Daughter,left_over_Vehicles))
                        # Each Final Edge contains an ARRAY of all its Edges from the 1st Node (DEPOT) till the last Node
                        # It also contains a Dictionary of the Left-Over Vehicles which are un-utilised

                    elif len(left_over_Vehicles)!=0:
                        set_of_Daughter_Edge_Graphs.append((next_starting_Node,all_Edges_in_Daughter,left_over_Vehicles))

            set_of_Mother_Edge_Graphs=set_of_Daughter_Edge_Graphs.copy()

        Optimal_Cost=Original_Cost
        Edges_of_Optimal_Solution=[]
        UnUtilised_Vehicles_at_Optimality={}
        # Calculating the Minimum Cost Graph
        for all_finalists in set_of_Final_Edge_Graphs:
            cumulative_edge_cost=0
            for each_final_edge in all_finalists[0]:
                cumulative_edge_cost+=each_final_edge[3]
            if cumulative_edge_cost<Optimal_Cost:
                Edges_of_Optimal_Solution=all_finalists[0]
                Optimal_Cost=cumulative_edge_cost
                UnUtilised_Vehicles_at_Optimality=all_finalists[1]

        Solution_Edges=set()
        for tuple_of_4 in Edges_of_Optimal_Solution:
            Solution_Edges.add((tuple_of_4[0],tuple_of_4[1],tuple_of_4[2]))


        Message_for_Notepad="Routes:- \n "
        for route in Edges_of_Optimal_Solution:
            Message_for_Notepad+=" Vehicle Type "+str(route[2])+" :\t "
            Message_for_Notepad+=str(Depot_First_Node)+" --> "
            for Nodes_in_a_route in range(route[0]+1,route[1]+1):
                Message_for_Notepad+=str(Node_Sequence[Nodes_in_a_route])+" --> "
            Message_for_Notepad+=str(Depot_First_Node)+" \t Route Cost: "+str(route[3])+" \n "

        Num_of_Vehicle_of_each_Type_being_used=VN.copy()
        for Vehicle_Type_number in UnUtilised_Vehicles_at_Optimality:
            Num_of_Vehicle_of_each_Type_being_used[Vehicle_Type_number]-=UnUtilised_Vehicles_at_Optimality[Vehicle_Type_number]


        if x_b[0]>Optimal_Cost:
            mu_of_a_b_c_d_e_f[0]+=(aa-mu_of_a_b_c_d_e_f[0])*f/f_iter
            mu_of_a_b_c_d_e_f[1]+=(bb-mu_of_a_b_c_d_e_f[1])*f/f_iter
            mu_of_a_b_c_d_e_f[2]+=(cc-mu_of_a_b_c_d_e_f[2])*f/f_iter
            mu_of_a_b_c_d_e_f[3]+=(dd-mu_of_a_b_c_d_e_f[3])*f/f_iter
            mu_of_a_b_c_d_e_f[4]+=(ee-mu_of_a_b_c_d_e_f[4])*f/f_iter
            mu_of_a_b_c_d_e_f[5]+=(ff-mu_of_a_b_c_d_e_f[5])*f/f_iter

            sigma_of_a_b_c_d_e_f[0]-=sigma_of_a_b_c_d_e_f[0]*f/f_iter
            sigma_of_a_b_c_d_e_f[1]-=sigma_of_a_b_c_d_e_f[1]*f/f_iter
            sigma_of_a_b_c_d_e_f[2]-=sigma_of_a_b_c_d_e_f[2]*f/f_iter
            sigma_of_a_b_c_d_e_f[3]-=sigma_of_a_b_c_d_e_f[3]*f/f_iter
            sigma_of_a_b_c_d_e_f[4]-=sigma_of_a_b_c_d_e_f[4]*f/f_iter
            sigma_of_a_b_c_d_e_f[5]-=sigma_of_a_b_c_d_e_f[5]*f/f_iter

        return Optimal_Cost,Message_for_Notepad,Solution_Edges,Num_of_Vehicle_of_each_Type_being_used



    def Decoding_Mechanism_1(Node_Sequence):

        def generating_Daughter_Edges(starting_Node,Vehicle_Type_used):
 
            DynamicCapacityLeft=[VQ[Vehicle_Type_used]]
            array_containing_Daughter_Edges=[]
            # Each Edge consists of its information in the form (From Node, To Node, Vehicle Type, Cost)

            Starting_Edge_Cost_from_Depot=VC[Vehicle_Type_used]+VS[Vehicle_Type_used]*C[Depot_First_Node,Node_Sequence[starting_Node+1],Vehicle_Type_used]
            Other_Edge_Costs=0
            
            for stopping_Node_of_Daughter_Edge in range(starting_Node+1,num_of_Nodes): # The Loop variable refers to the Ending Node of each Edge

                CapacityCheck=0
                #print(DynamicCapacityLeft[0])
                DynamicCapacityLeft[0]=DynamicCapacityLeft[0]-Deliveries[Node_Sequence[stopping_Node_of_Daughter_Edge]]
                DynamicCapacityLeft.append(Deliveries[Node_Sequence[stopping_Node_of_Daughter_Edge]]-PickUps[Node_Sequence[stopping_Node_of_Daughter_Edge]])
                for m in DynamicCapacityLeft:
                    CapacityCheck+=m
                    if CapacityCheck<0:
                        break
                if CapacityCheck<0:
                    break

                if stopping_Node_of_Daughter_Edge>(starting_Node+1):
                    Other_Edge_Costs+=VS[Vehicle_Type_used]*C[Node_Sequence[stopping_Node_of_Daughter_Edge-1],Node_Sequence[stopping_Node_of_Daughter_Edge],Vehicle_Type_used]

                Ending_Edge_Cost_to_Depot=VS[Vehicle_Type_used]*C[Node_Sequence[stopping_Node_of_Daughter_Edge],Depot_First_Node,Vehicle_Type_used]
                Total_Edge_Cost=Starting_Edge_Cost_from_Depot+Other_Edge_Costs+Ending_Edge_Cost_to_Depot

                array_containing_Daughter_Edges.append((starting_Node,stopping_Node_of_Daughter_Edge,Vehicle_Type_used,Total_Edge_Cost))
            
            return array_containing_Daughter_Edges # Each Edge is a Tuple of 4 elements containing (Origin Node, Destination Node, Vehicle Type, Cost)

        num_of_Nodes=len(Node_Sequence)

        Depot_First_Node=Node_Sequence[0]
        if Node_Sequence[0]!=0:
            # This check is for the specific problem considered in the Paper
            for just_some_screen_space in range(99):
                print("EXCEPTION: Line 353 :Please Check Code")
            return
        # Node Sequence should be an array starting from 0th Node and containing other Node Indexes, example 0,1,8,6,7

        left_over_Vehicles_of_each_Type=VN.copy() # The VN dictionary is being copied
        for VT_name in VN:
            if VN[VT_name]==0:
                del left_over_Vehicles_of_each_Type[VT_name]

        # Each Edge Graph is a Tuple consisting of 1 Element 1 Array and 1 Dictionary:-
            # The ELEMENT is the Node Number of the present staring EDGE from which we shall start analysisng
            # The ARRAY contains the Edges present in it
                # Each Edge consists of its information in the form (From Node, To Node, Vehicle Type, Cost)
            # The DICTIONARY contains the details of the Vehicles which may be used of each Type
                # So a Dictionary {2:4,5:6} means that there are 4 Vehicles left of Type 2 and 6 Vehicles of Type 5
        set_of_Mother_Edge_Graphs=[(0,[],left_over_Vehicles_of_each_Type)]
        set_of_Final_Edge_Graphs=[] # Sets were replaced by arrays due to sets being unhashable when arrays are wihin them ?!?

        # This loop is for populating the Final Edge Graphs set
        while set_of_Mother_Edge_Graphs:

            set_of_Daughter_Edge_Graphs=[]
            for each_Edge_Graph in set_of_Mother_Edge_Graphs:

                array_containing_all_Daughter_Edges=[]
                for Vehicle_Type_considered in each_Edge_Graph[2]:
                    # Creating a function to obtain the Daughter Edges
                    # Send a Mother Edge Graph for each Vehicle Type to the function and obtain the array of the daughter Edges to be individually added to the Mother Edge for that Vehicle Type
                    if each_Edge_Graph[2][Vehicle_Type_considered]>0:  # Only calculating when a Vehicle is available
                        daughter_edges_of_specific_Vehicle_Type=generating_Daughter_Edges(each_Edge_Graph[0],Vehicle_Type_considered)
                        for i in daughter_edges_of_specific_Vehicle_Type:
                            array_containing_all_Daughter_Edges.append(i)

                array_of_Daughter_Edges=[]
                length_of_Daughter_array=len(array_containing_all_Daughter_Edges)
                if length_of_Daughter_array>=3:
                    # Logically  Accepting the Best Edges

                    aa = np.random.normal(mu_of_a_b_c_d_e_f[0],sigma_of_a_b_c_d_e_f[0])            
                    bb = np.random.normal(mu_of_a_b_c_d_e_f[1],sigma_of_a_b_c_d_e_f[1])
                    cc = np.random.normal(mu_of_a_b_c_d_e_f[2],sigma_of_a_b_c_d_e_f[2])
                    dd = np.random.normal(mu_of_a_b_c_d_e_f[3],sigma_of_a_b_c_d_e_f[3])
                    ee = np.random.normal(mu_of_a_b_c_d_e_f[4],sigma_of_a_b_c_d_e_f[4])
                    ff = np.random.normal(mu_of_a_b_c_d_e_f[5],sigma_of_a_b_c_d_e_f[5])

                    potential_mother_edge=0
                    minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                    for i in array_containing_all_Daughter_Edges:
                        fixed_cost=VC[i[2]]
                        variable_cost=i[3]-VC[i[2]]
                        length=i[1]-i[0]
                        edge_minimization_objective=aa*pow(fixed_cost,bb)*pow(length,cc) + dd*pow(variable_cost,ee)*pow(length,ff)
                        if edge_minimization_objective<minimum_Distributed_Cost:
                            minimum_Distributed_Cost=edge_minimization_objective
                            potential_mother_edge=i
                    if potential_mother_edge!=0:
                        array_of_Daughter_Edges.append(potential_mother_edge)

                else:
                    array_of_Daughter_Edges=array_containing_all_Daughter_Edges


                all_Edges_in_Mother=each_Edge_Graph[1]
                for Daughter_Edge in array_of_Daughter_Edges:
                    next_starting_Node=Daughter_Edge[1]
                    all_Edges_in_Daughter=all_Edges_in_Mother.copy()
                    all_Edges_in_Daughter.append(Daughter_Edge)
                    left_over_Vehicles=each_Edge_Graph[2].copy()
                    Vehicle_Type_considered=Daughter_Edge[2]
                    left_over_Vehicles[Vehicle_Type_considered]=left_over_Vehicles[Vehicle_Type_considered]-1
                    if left_over_Vehicles[Vehicle_Type_considered]==0:
                        del left_over_Vehicles[Vehicle_Type_considered]


                    if next_starting_Node==num_of_Nodes-1:
                        set_of_Final_Edge_Graphs.append((all_Edges_in_Daughter,left_over_Vehicles))
                        # Each Final Edge contains an ARRAY of all its Edges from the 1st Node (DEPOT) till the last Node
                        # It also contains a Dictionary of the Left-Over Vehicles which are un-utilised

                    elif len(left_over_Vehicles)!=0:
                        set_of_Daughter_Edge_Graphs.append((next_starting_Node,all_Edges_in_Daughter,left_over_Vehicles))

            set_of_Mother_Edge_Graphs=set_of_Daughter_Edge_Graphs.copy()

        Optimal_Cost=Original_Cost
        Edges_of_Optimal_Solution=[]
        UnUtilised_Vehicles_at_Optimality={}
        # Calculating the Minimum Cost Graph
        for all_finalists in set_of_Final_Edge_Graphs:
            cumulative_edge_cost=0
            for each_final_edge in all_finalists[0]:
                cumulative_edge_cost+=each_final_edge[3]
            if cumulative_edge_cost<Optimal_Cost:
                Edges_of_Optimal_Solution=all_finalists[0]
                Optimal_Cost=cumulative_edge_cost
                UnUtilised_Vehicles_at_Optimality=all_finalists[1]

        Solution_Edges=set()
        for tuple_of_4 in Edges_of_Optimal_Solution:
            Solution_Edges.add((tuple_of_4[0],tuple_of_4[1],tuple_of_4[2]))


        Message_for_Notepad="Routes:- \n "
        for route in Edges_of_Optimal_Solution:
            Message_for_Notepad+=" Vehicle Type "+str(route[2])+" :\t "
            Message_for_Notepad+=str(Depot_First_Node)+" --> "
            for Nodes_in_a_route in range(route[0]+1,route[1]+1):
                Message_for_Notepad+=str(Node_Sequence[Nodes_in_a_route])+" --> "
            Message_for_Notepad+=str(Depot_First_Node)+" \t Route Cost: "+str(route[3])+" \n "

        Num_of_Vehicle_of_each_Type_being_used=VN.copy()
        for Vehicle_Type_number in UnUtilised_Vehicles_at_Optimality:
            Num_of_Vehicle_of_each_Type_being_used[Vehicle_Type_number]-=UnUtilised_Vehicles_at_Optimality[Vehicle_Type_number]


        return Optimal_Cost,Message_for_Notepad,Solution_Edges,Num_of_Vehicle_of_each_Type_being_used





    print("\n ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~")
    Node_Sequence,Latitude,Longitude,PickUps,Deliveries=GeneRead.Reader.Relief_Centre_Reader(directory_of_Relief_Centre_Specifications_file=directory_containing_Node_Locations_file)
    print(" ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~")
    Vehicle_Types,VN,VQ,VS,VC,Vehicle_Width=GeneRead.Reader.Vehicle_Type_Reader(directory_containing_Vehicle_Types_file)
    print(" Starting ATSAML_6 following Evaluation Processes after reading Inputs")
    C=GeneRead.Reader.Distance_Combinations_Reader(directory_containing_Distance_Locations_file=directory_containing_Distance_Matrix_file,directory_of_Vehicle_Types_considered_file=directory_containing_Vehicle_Types_file)
    print(" ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~")

    textfile = open(directory_to_save_ATSAML_6_solution+"Vehicle Routes from ATSAML_6.txt","w")

    size_of_prob=len(Node_Sequence)
    N=8 # Neighbourhood Structure Numbers
    Ci=1
    ii=1
    ultimate_counter=0

    f_iter=2000*(1-pow(size_of_prob/1500,0.1)+pow(1-(size_of_prob/1000),5))
    #f_iter=3250*(1-pow(size_of_prob/2750,0.1)+pow(1-(size_of_prob/750),5))
    
    f=0

    # Obtaining the First Solution
    Depot_First_Node=Node_Sequence[0]
    Node_Sequence_Intermediate=Node_Sequence
    x_b=(99999999999999999999999999999999999999999999999,"First Solution yet to be found",set(),{})
    print(" ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~ \n")
    
    mu_of_a_b_c_d_e_f=[2*random(),random(),3*random()-2,2*random(),random(),3*random()-2]
    sigma_of_a_b_c_d_e_f=[1,1.25,1.5,1,1.25,1.5]

    set_of_mu_of_a_2_f=[mu_of_a_b_c_d_e_f]

    if len(mu_of_a_b_c_d_e_f)!=len(sigma_of_a_b_c_d_e_f):
        for i in range(999):
            print("Fatal Error: Line 680")

    first_solution_start_time=time.time()
    x=Decoding_Mechanism_1(Node_Sequence)
    while x[0]>=99999999999999999999999999999999999999999999999:
        print("Trying to find the first feasible solution")
        if random()>0.5:
            x=Decoding_Mechanism_1(Node_Sequence)
        else:
            x=Decoding_Mechanism_0(Node_Sequence)
    first_solution_end_time=time.time()

    if Time_Constraint>=99999999999999999999999999999999999999999999999:
        print("No Time Constraint found. Come back after 25 years to check solution if problem is exceedingly large or try your Convergence Luck!")

    delta_T=first_solution_end_time-first_solution_start_time

    textfile.write(str("\n"))
    textfile.write("\n The first output was obtained after "+str(delta_T)+" seconds with the outer-loop_counter="+str(ultimate_counter)+".\n")
    textfile.write("Objective Function Value \t "+str(x[0])+"\n")
    textfile.write(str(x[1]))
    textfile.write("\n Vehicles Used (Vehicle Type Index : Number of Vehicles Used of this Type) \t "+str(x[3]))
    textfile.write(str("\n \n"))

    print("\n The first output was obtained after ",delta_T," seconds with the outer-loop_counter=",ultimate_counter,".\n")
    print("Objective Function Value \t ",x[0],"\n")
    print(x[1])
    print("\n Vehicles Used (Vehicle Type Index : Number of Vehicles Used of this Type) \t ",x[3])
    
    x_b=x
    x_dash=x
    age=0
    a1=x_b[0]/x[0]
    a2=Ci/ii
    t=1+a1*a2
    
    Objective_Plot=[]
    Time_Plot=[]

    f_Plot=[]
    Time_Plot_fr_f=[]

    Threshold=[]
    ALL_tIME=[]

    Objectives_above_Threshold=[]
    Times_for_Objectives_above_Threshold=[]

    Objectives_below_Threshold=[] # not including the Best Solution
    Times_for_Objectives_below_Threshold=[]

    #slope=(99999999999999999999999999999999999999999999999-x[0])/delta_T
    #min_slope=slope

    start_time=time.time()
    while f<=f_iter and delta_T<=Time_Constraint:
    #while (f<f_iter or slope>min_slope) and delta_T<=Time_Constraint:
        ultimate_counter+=1 # This Value multiplied by 8*2 gives the Number of times different Decoding Mechanisms were called


        Node_Sequence_1=Node_Sequence.copy()
        Adjacent_Swap(Node_Sequence_1,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_1=Decoding_Mechanism_1(Node_Sequence_1)
        if x_dash_1[0]<x_dash[0]:
            x_dash=x_dash_1
            Node_Sequence_Intermediate=Node_Sequence_1

        Node_Sequence_2=Node_Sequence.copy()
        General_Swap(Node_Sequence_2,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_2=Decoding_Mechanism_1(Node_Sequence_2)
        if x_dash_2[0]<x_dash[0]:
            x_dash=x_dash_2
            Node_Sequence_Intermediate=Node_Sequence_2

        Node_Sequence_3=Node_Sequence.copy()
        Single_Insertion(Node_Sequence_3,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_3=Decoding_Mechanism_1(Node_Sequence_3)
        if x_dash_3[0]<x_dash[0]:
            x_dash=x_dash_3
            Node_Sequence_Intermediate=Node_Sequence_3

        Node_Sequence_4=Node_Sequence.copy()
        Reversal(Node_Sequence_4,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_4=Decoding_Mechanism_1(Node_Sequence_4)
        if x_dash_4[0]<x_dash[0]:
            x_dash=x_dash_4
            Node_Sequence_Intermediate=Node_Sequence_4

        Node_Sequence_5=Node_Sequence.copy()
        Shuffle_Random(Node_Sequence_5,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_5=Decoding_Mechanism_1(Node_Sequence_5)
        if x_dash_5[0]<x_dash[0]:
            x_dash=x_dash_5
            Node_Sequence_Intermediate=Node_Sequence_5

        Node_Sequence_6=Node_Sequence.copy()
        SubArray_Transplant_Allowing_Operations(Node_Sequence_6,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_6=Decoding_Mechanism_1(Node_Sequence_6)
        if x_dash_6[0]<x_dash[0]:
            x_dash=x_dash_6
            Node_Sequence_Intermediate=Node_Sequence_6

        Node_Sequence_7=Node_Sequence.copy()
        Linear_Cake_Cutting_once_without_Overlap(Node_Sequence_7,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_7=Decoding_Mechanism_1(Node_Sequence_7)
        if x_dash_7[0]<x_dash[0]:
            x_dash=x_dash_7
            Node_Sequence_Intermediate=Node_Sequence_7
        
        Node_Sequence_8=Node_Sequence.copy()
        Linear_Cake_Cutting_and_Accumulation(Node_Sequence_8,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_8=Decoding_Mechanism_1(Node_Sequence_8)
        if x_dash_8[0]<x_dash[0]:
            x_dash=x_dash_8
            Node_Sequence_Intermediate=Node_Sequence_8




        Node_Sequence_1=Node_Sequence.copy()
        Adjacent_Swap(Node_Sequence_1,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_1=Decoding_Mechanism_0(Node_Sequence_1)
        if x_dash_1[0]<x_dash[0]:
            x_dash=x_dash_1
            Node_Sequence_Intermediate=Node_Sequence_1

        Node_Sequence_2=Node_Sequence.copy()
        General_Swap(Node_Sequence_2,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_2=Decoding_Mechanism_0(Node_Sequence_2)
        if x_dash_2[0]<x_dash[0]:
            x_dash=x_dash_2
            Node_Sequence_Intermediate=Node_Sequence_2

        Node_Sequence_3=Node_Sequence.copy()
        Single_Insertion(Node_Sequence_3,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_3=Decoding_Mechanism_0(Node_Sequence_3)
        if x_dash_3[0]<x_dash[0]:
            x_dash=x_dash_3
            Node_Sequence_Intermediate=Node_Sequence_3

        Node_Sequence_4=Node_Sequence.copy()
        Reversal(Node_Sequence_4,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_4=Decoding_Mechanism_0(Node_Sequence_4)
        if x_dash_4[0]<x_dash[0]:
            x_dash=x_dash_4
            Node_Sequence_Intermediate=Node_Sequence_4

        Node_Sequence_5=Node_Sequence.copy()
        Shuffle_Random(Node_Sequence_5,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_5=Decoding_Mechanism_0(Node_Sequence_5)
        if x_dash_5[0]<x_dash[0]:
            x_dash=x_dash_5
            Node_Sequence_Intermediate=Node_Sequence_5

        Node_Sequence_6=Node_Sequence.copy()
        SubArray_Transplant_Allowing_Operations(Node_Sequence_6,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_6=Decoding_Mechanism_0(Node_Sequence_6)
        if x_dash_6[0]<x_dash[0]:
            x_dash=x_dash_6
            Node_Sequence_Intermediate=Node_Sequence_6

        Node_Sequence_7=Node_Sequence.copy()
        Linear_Cake_Cutting_once_without_Overlap(Node_Sequence_7,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_7=Decoding_Mechanism_0(Node_Sequence_7)
        if x_dash_7[0]<x_dash[0]:
            x_dash=x_dash_7
            Node_Sequence_Intermediate=Node_Sequence_7
        
        Node_Sequence_8=Node_Sequence.copy()
        Linear_Cake_Cutting_and_Accumulation(Node_Sequence_8,is_Depot_within_sequence_as_First_Node="Y")
        x_dash_8=Decoding_Mechanism_0(Node_Sequence_8)
        if x_dash_8[0]<x_dash[0]:
            x_dash=x_dash_8
            Node_Sequence_Intermediate=Node_Sequence_8


        #Node_Sequence=Node_Sequence_Intermediate.copy()
        Node_Sequence=Node_Sequence_Intermediate      

        end_time=time.time()
        delta_T=end_time-start_time

        Threshold.append(t*x_b[0])
        ALL_tIME.append(delta_T)

        if x_dash[0]<=t*x_b[0]:
            x=x_dash
            ii+=1
            age=0
            if x[0]<x_b[0]:
                print("The present value of f is ",f)

                Time_Plot.append(delta_T)
                Objective_Plot.append(x[0])

                f_Plot.append(f)
                Time_Plot_fr_f.append(delta_T)
                
                #slope=(x_b[0]-x[0])/delta_T
                #if slope<min_slope:
                #    min_slope=slope

                x_b=x
                Ci+=1

                textfile.write(str("\n"))
                textfile.write("\n Outer-loop_counter="+str(ultimate_counter))
                textfile.write("\n Objective Function Value \t "+str(x_b[0])+" obtained after "+str(delta_T)+" seconds\n")
                textfile.write(str(x_b[1]))
                #textfile.write("Solutions (Origin Node,Destination Node,Vehicle Type):- "+str(x_b[2]))
                textfile.write("\n Vehicles Used (Vehicle Type Index : Number of Vehicles Used of this Type) \t "+str(x_b[3]))
                textfile.write(str("\n \n"))
                
                print("\n Outer-loop_counter=",ultimate_counter,"at ",delta_T," seconds\n")
                for each_element in x_b:
                    print(each_element)
                print("Mean: \t ",mu_of_a_b_c_d_e_f)
                print("S.D.: \t ",sigma_of_a_b_c_d_e_f,"\n")

                set_of_mu_of_a_2_f.append(mu_of_a_b_c_d_e_f.copy())

                f=0
                f_Plot.append(f)
                Time_Plot_fr_f.append(time.time()-start_time)

            else:
                Objectives_below_Threshold.append(x_dash[0])
                Times_for_Objectives_below_Threshold.append(delta_T)
                f+=1
            a1=x_b[0]/x[0]
            a2=Ci/ii
            t=1+a1*a2
        else:
            Objectives_above_Threshold.append(x_dash[0])
            Times_for_Objectives_above_Threshold.append(delta_T)
            age+=1
            if age>=N/3:
                age=0
                t=t+a1*a2

    end_time=time.time()

    delta_T=end_time-start_time
    print("The final output was obtained after ",delta_T," seconds with the outer-loop_counter=",ultimate_counter,".\n")    
    textfile.write("\n The final output was obtained after "+str(delta_T)+" seconds with the outer-loop_counter="+str(ultimate_counter)+".\n")
    for k in Vehicle_Types:
        # Maximum number of vehicles being used for each Vehicle Type
        print(x_b[3][k]," vehicles of Vehicle Type "+str(k)+" are used")
        textfile.write(str(x_b[3][k])+" vehicles of Vehicle Type "+str(k)+" are used \n")

    textfile.write("The final values of Mean are:- "+str(mu_of_a_b_c_d_e_f)+" \n")
    textfile.write("The final values of S.D. are:- "+str(sigma_of_a_b_c_d_e_f)+" \n")
    print("Tuned Mean Values: ",mu_of_a_b_c_d_e_f)
    print("Tuned S.D. Values: ",sigma_of_a_b_c_d_e_f)
    textfile.close()

    original_colour_diversity=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf' , 'C0' , 'C1' , 'tab:blue' , 'tab:orange' , 'tab:green' , 'tab:red' , 'tab:purple' , 'tab:brown' , 'tab:pink' , 'tab:gray' , 'tab:olive' , 'tab:cyan' , 'xkcd:sky blue' , 'xkcd:eggshell' , 'aquamarine' , 'mediumseagreen' , 'b' , 'g' , 'r' , 'c' , 'm' , 'y' , 'k' , 'w' , (0.1, 0.2, 0.5) , (0.1, 0.2, 0.5, 0.3) , '#0f0f0f' , '#0f0f0f80' , '#abc' , '#aabbcc' , '#fb1' , '#ffbb11']
    
    # Plotting the Depot and Relief Centres
    for k in Vehicle_Types:
        plt.figure(figsize=(11,11))
        for i in Node_Sequence:
            if i==Depot_First_Node:
                plt.scatter(Longitude[i],Latitude[i], c='r',marker='s')
                plt.text(Longitude[i] + 0.33, Latitude[i] + 0.33, "Depot")
            else:
                plt.scatter(Longitude[i], Latitude[i], c='black')
                plt.text(Longitude[i] + 0.33, Latitude[i] + 0.33, i)
        plt.title('mVRPSDC Tours for Vehicles of Type '+str(k)+" on the corresponding layer "+str(k))
        plt.ylabel("Latitude")
        plt.xlabel("Longitude")

        routes=[]
        for element in x_b[2]:            
            if element[2]==k:
                route_of_one_vehicle=[]
                route_of_one_vehicle.append((Depot_First_Node,Node_Sequence[element[0]+1]))
                route_of_one_vehicle.append((Node_Sequence[element[1]],Depot_First_Node))
                for i in range(element[0]+1,element[1]):
                    route_of_one_vehicle.append((Node_Sequence[i],Node_Sequence[i+1]))
                routes.append(route_of_one_vehicle)
                

        colour_diversity=original_colour_diversity.copy()
        for individual_vehicle_route in routes:
            existing_number_of_colours_available=len(colour_diversity)
            colour_choice=randint(1,existing_number_of_colours_available)
            edge_colour=colour_diversity[colour_choice-1]
            
            # Drawing the optimal routes Layerwise
            for i,j in individual_vehicle_route:
                plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="simple", connectionstyle='arc3', edgecolor=edge_colour))
                #plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="-|>", connectionstyle='arc3', edgecolor=(count/colour_intervals,1-(count/colour_intervals),1)))
                #plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="simple", connectionstyle='angle3', edgecolor=(count/colour_intervals,1-(count/colour_intervals),1)))
                # Edge_Notes="P="+str(y[i,j,k].varValue)+" ; D="+str(z[i,j,k].varValue) How to get this? Is this necessary?
                #plt.text((Longitude[i]+Longitude[j])/2, (Latitude[i]+Latitude[j])/2, f'{Edge_Notes}',fontweight="bold")
                # Directly load the Vehicle with the sum of the Demands and route it so that it may take up the PickUps from the respective Nodes after individual Deliveries

            if existing_number_of_colours_available==1:
                colour_diversity=original_colour_diversity.copy()
            else:del colour_diversity[colour_choice-1]


        # Finding the Maximum Utilised Vehicle Capacity for each Vehicle Type?
        main_dir_for_Image=directory_to_save_ATSAML_6_solution+"{}"
        name="Used "+str(x_b[3][k])+" Vehicles of Type "+str(k)+" having Capacity_ "+str(VQ[k])+".eps"
        plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
        name="Used "+str(x_b[3][k])+" Vehicles of Type "+str(k)+" having Capacity_ "+str(VQ[k])+"PNG.png"
        plt.savefig(main_dir_for_Image.format(name))
        #plt.figure().clear()
        #plt.cla()
        #plt.clf()
        plt.close()


    """plt.figure(figsize=(19,11))
    plt.plot(Time_Plot, Objective_Plot)
    plt.scatter(Time_Plot, Objective_Plot)
    plt.xlabel('Solution Time')
    plt.ylabel('Objective Value', color='g')
    name="Progressive slowdown of Objective decrease.png"
    plt.savefig(main_dir_for_Image.format(name))
    plt.close()

    plt.figure(figsize=(19,11))
    plt.plot(Time_Plot, f_Plot)
    plt.scatter(Time_Plot, f_Plot)
    plt.xlabel('Solution Time')
    plt.ylabel('f -> Termination Criteria', color='b')
    name="Understanding threshold effects of F_iter = "+str(f_iter)+".png"
    plt.savefig(main_dir_for_Image.format(name))
    plt.close()"""
    
    
    store=" "
    for i in mu_of_a_b_c_d_e_f:
        store=store+str(round(i,2))+" , "

    plt.figure(figsize=(11,5))
    plt.plot(Time_Plot, Objective_Plot,c="darkolivegreen")
    plt.scatter(Time_Plot, Objective_Plot,c="mediumseagreen")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Solution Time',fontsize=15)
    #plt.ylabel('Objective Fn. Value', color='g',fontsize=19)
    plt.ylabel('Objective Fn. Value',fontsize=20)
    #plt.title("Best Objective of "+str(x_b[0])+" obtained in "+str(delta_T)+" seconds \n Tuned Means: ["+store+"]")
    plt.title("Best Objective of "+str(x_b[0])+" obtained in "+str(round(delta_T,1))+" seconds",fontsize=18)
    name="Progressive slowdown of Objective decrease.eps"
    plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
    name="Progressive slowdown of Objective decreasePNG.png"
    plt.savefig(main_dir_for_Image.format(name))
    plt.close()

    plt.figure(figsize=(11,5))
    plt.plot(Time_Plot_fr_f, f_Plot,c="dodgerblue")
    plt.scatter(Time_Plot_fr_f, f_Plot,c="royalblue")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    #plt.axhline(y = f_iter, color = 'r', linestyle = '-')
    #plt.text(delta_T/2 - 3.33, f_iter - 0.33, "Maximum "+str(f_iter)+" iterations allowed before Termination")
    plt.xlabel('Solution Time',fontsize=15)
    #plt.ylabel('f  ->  Termination Criteria', color='b',fontsize=19)
    plt.ylabel('f  ->  Termination Criteria',fontsize=20)
    #plt.title("Algorithm terminates when f reaches "+str(f_iter)+"; Total Iterations: "+str(ultimate_counter)+" gives each iteration span of "+str(delta_T/ultimate_counter)+" seconds")
    plt.title("Algorithm terminates when f reaches "+str(round(f_iter,2))+"; Total Iterations: "+str(ultimate_counter),fontsize=18)
    name="Understanding threshold effects of F_iter.eps"
    plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
    name="Understanding threshold effects of F_iterPNG.png"
    plt.savefig(main_dir_for_Image.format(name))
    plt.close()

    plt.figure(figsize=(19.2,10.8))
    plt.plot(ALL_tIME, Threshold, dashes=[6,2], drawstyle='steps-pre',c='orange',label="Threshold") # Threshold Line Orange
    plt.plot(Time_Plot, Objective_Plot, dashes=[3,1], drawstyle='steps-pre',c='green',label="Best Objective") # Best Objective Line Green
    plt.scatter(Times_for_Objectives_above_Threshold, Objectives_above_Threshold,c="red", label="Objectives above Threshold")
    plt.scatter(Times_for_Objectives_below_Threshold, Objectives_below_Threshold,c="dodgerblue",label="Objectives between Threshold and Best")
    plt.xlabel('Solution Time')
    plt.ylabel('Objective Value')
    plt.title("Best Objective of "+str(x_b[0])+" obtained in "+str(delta_T)+" seconds. "+'\n Total Iterations: '+str(ultimate_counter)+" gives each iteration span of "+str(delta_T/ultimate_counter)+" seconds \n Tuned Means: ["+store+"]")
    plt.legend()
    name="Bounds.eps"
    plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
    name="BoundsPNG.png"
    plt.savefig(main_dir_for_Image.format(name))    
    plt.close()


    num_of_x_b=len(set_of_mu_of_a_2_f)
    step=0.99/(num_of_x_b+2.5)
    parameters=["k","m","l","h","i","j"]
    parameters = [*parameters, parameters[0]]
    plt.figure(figsize=(5.4,5.4))
    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(parameters))
    #line_thickness_progress=0
    
    color_progress=[1,0,0]
    for i in range(floor(num_of_x_b/2)):
        parameter_means=set_of_mu_of_a_2_f[i]
        parameter_means=[*parameter_means,parameter_means[0]]
        color_progress[0]=color_progress[0]-2*step
        color_progress[1]=color_progress[1]+2*step
        #line_thickness_progress+=3*step
        plt.subplot(polar=True)
        #plt.plot(label_loc, parameter_means,c=color_progress.copy(),linewidth=line_thickness_progress)
        plt.plot(label_loc, parameter_means,c=color_progress.copy(),linewidth=1)

    color_progress=[0,1,0]
    for i in range(ceil(num_of_x_b/2),num_of_x_b):
        parameter_means=set_of_mu_of_a_2_f[i]
        parameter_means=[*parameter_means,parameter_means[0]]
        color_progress[1]=color_progress[1]-2*step
        color_progress[2]=color_progress[2]+2*step
        #line_thickness_progress+=3*step
        plt.subplot(polar=True)
        #plt.plot(label_loc, parameter_means,c=color_progress.copy(),linewidth=line_thickness_progress)
        plt.plot(label_loc, parameter_means,c=color_progress.copy(),linewidth=1)

    plt.title('Transition of Mean Values of Parameters \n obtaining final objective value of '+str(x_b[0]), size=13, y=1.05)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=parameters, size=19)
    #plt.legend()
    name="ProgressParameters.eps"
    plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
    name="ProgressParametersPNG.png"
    plt.savefig(main_dir_for_Image.format(name))
    plt.close()

    textfile0 = open(directory_to_save_ATSAML_6_solution+"Time_Plot.txt","w")
    textfile0.write(str(Time_Plot))
    textfile0.close()

    textfile1 = open(directory_to_save_ATSAML_6_solution+"Objective_Plot.txt","w")
    textfile1.write(str(Objective_Plot))
    textfile1.close()

    textfile2 = open(directory_to_save_ATSAML_6_solution+"Time_Plot_fr_f.txt","w")
    textfile2.write(str(Time_Plot_fr_f))
    textfile2.close()

    textfile3 = open(directory_to_save_ATSAML_6_solution+"f_Plot.txt","w")
    textfile3.write(str(f_Plot))
    textfile3.close()
    
    textfile4 = open(directory_to_save_ATSAML_6_solution+"ALL_tIME.txt","w")
    textfile4.write(str(ALL_tIME))
    textfile4.close()

    textfile5 = open(directory_to_save_ATSAML_6_solution+"Threshold.txt","w")
    textfile5.write(str(Threshold))
    textfile5.close()

    textfile6 = open(directory_to_save_ATSAML_6_solution+"Times_for_Objectives_above_Threshold.txt","w")
    textfile6.write(str(Times_for_Objectives_above_Threshold))
    textfile6.close()

    textfile7 = open(directory_to_save_ATSAML_6_solution+"Objectives_above_Threshold.txt","w")
    textfile7.write(str(Objectives_above_Threshold))
    textfile7.close()

    textfile8 = open(directory_to_save_ATSAML_6_solution+"Times_for_Objectives_below_Threshold.txt","w")
    textfile8.write(str(Times_for_Objectives_below_Threshold))
    textfile8.close()


    textfile9 = open(directory_to_save_ATSAML_6_solution+"Objectives_below_Threshold.txt","w")
    textfile9.write(str(Objectives_below_Threshold))
    textfile9.close()

    textfile10 = open(directory_to_save_ATSAML_6_solution+"set_of_mu_of_a_2_f.txt","w")
    textfile10.write(str(set_of_mu_of_a_2_f))
    textfile10.close()


    # returns Objective Function Value, Routes Message, All selected Edge Solutions, Number of Vehicle Used of each Type and the Time Taken to compute this Solution
    return x_b,delta_T,ultimate_counter,mu_of_a_b_c_d_e_f