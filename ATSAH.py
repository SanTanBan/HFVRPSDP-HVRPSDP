import time
import pandas as pd
import matplotlib.pylab as plt
import os
from random import random,randint,shuffle
import GeneRead
from math import pow


def ATS_Algorithm_Heuristic(directory_details_for_saving="",directory_containing_Vehicle_Types_file="",directory_containing_Node_Locations_file="",directory_containing_Distance_Matrix_file=""):

    dir_name="ATSAH Evaluation"
    os.mkdir(directory_details_for_saving+dir_name)
    directory_to_save_ATSAH_solution=directory_details_for_saving+dir_name+"/"
    Original_Cost=99999999999999999999999999999999999999999999999

    def SubArray_Transplant_Allowing_Operations(Node_Sequence):
        First_Node_Depot=Node_Sequence[0]
        Upto_Len=len(Node_Sequence)-1
        Node_Sequence.remove(First_Node_Depot) # Removing the Depot Node
        sub_array=[]

        # Creating The Sub-Array [2 Ways:=> First is Sequential, 2nd is Arbitrary]
        if randint(-1,1):   # Way 1 is Taking a Random Length of Consequetive Elements
            random_point_1=randint(0,Upto_Len)
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
            reversed(sub_array)
            #sub_array.reverse()
        elif randint(-1,1):
            shuffle(sub_array)

        # Performing Operations on the Node_Sequence withput the Sub-Array Elements
        if randint(-1,1):
            Node_Sequence.reverse()
        elif randint(-1,1):
            shuffle(Node_Sequence)
        
        # Insertion the Sub Array Elements [2 Ways:=> First is Single Bulk Insertion, 2nd is Random Insertion at Arbitrary Places]
        if randint(-1,1):   # Way 1 is inserting the Total Sub-Array in a Random Location in the Operated Node Sequence (By default this insertion is reversed)
            random_insertion_point=randint(0,len(Node_Sequence))
            for i in sub_array:
                Node_Sequence.insert(random_insertion_point,i)    
        else:   # Way 2 is inserting individual Sub-Array Elements in Random Locations in the Node Sequence
            for i in range(len(sub_array)):
                random_insertion_point=randint(0,len(Node_Sequence))
                Node_Sequence.insert(random_insertion_point,sub_array[i])

        Node_Sequence.insert(0,First_Node_Depot) # Inserting the Depot Node as the First Element


    def Adjacent_Swap(Node_Sequence):
        Upto_Len=len(Node_Sequence)-2
        temp=randint(1, Upto_Len)
        Node_Sequence[temp]-=Node_Sequence[temp+1]
        Node_Sequence[temp+1]+=Node_Sequence[temp]
        Node_Sequence[temp]=Node_Sequence[temp+1]-Node_Sequence[temp]


    def General_Swap(Node_Sequence):
        Upto_Len=len(Node_Sequence)-1
        temp1=randint(1, Upto_Len)
        temp2=temp1
        while temp2==temp1:
            temp2=randint(1, Upto_Len)
        temp=Node_Sequence[temp1]
        Node_Sequence[temp1]=Node_Sequence[temp2]
        Node_Sequence[temp2]=temp
    

    def Single_Insertion(Node_Sequence):
        Upto_Len=len(Node_Sequence)-1-2
        temp1=randint(1, Upto_Len)
        temp2=Node_Sequence[temp1]
        del Node_Sequence[temp1]
        temp3=randint(temp1+2,Upto_Len+2)
        Node_Sequence.insert(temp3,temp2)
    

    def Reversal(Node_Sequence):
        Upto_Len=len(Node_Sequence)
        start=randint(1,Upto_Len-3)
        finish=randint(start+2,Upto_Len-1)
        Reversed_Node_Sequence=Node_Sequence[:start:+1]+Node_Sequence[finish:start-1:-1]+Node_Sequence[finish+1::+1]
        return Reversed_Node_Sequence


    def Shuffle_Random(Node_Sequence):
        First_Node_Depot=Node_Sequence[0]
        shuffle(Node_Sequence)
        Node_Sequence.remove(First_Node_Depot)
        Node_Sequence.insert(0,First_Node_Depot)


    def Decoding_Mechanism(Node_Sequence,evaluation_process=12):

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
                print("EXCEPTION: Please Check Code")
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

                    if evaluation_process==12:  # Randomly Accepting 1 or 2 Daughter Edges
                        rand_position=randint(0,length_of_Daughter_array-1)
                        if random()>0.99:
                            rand_position_2=rand_position
                            while rand_position==rand_position_2:
                                rand_position_2=randint(0,length_of_Daughter_array-1)
                            array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position_2])
                        array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position])

                    elif evaluation_process==0: # Randomly Accepting 1 Daughter Edge
                        rand_position=randint(0,length_of_Daughter_array-1)
                        array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position])

                    elif evaluation_process==1: # Accepting Only the Longest Edge
                        max_length=0
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            if length>max_length:
                                max_length=length
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==2: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            distributed_cost=i[3]/(i[1]-i[0])
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==3: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            distributed_cost=i[3]/cumulative_length
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==4: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                            fixed_distributed_cost=VC[i[2]]/length
                            distributed_cost=variable_distributed_cost+fixed_distributed_cost
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==5: # Doing any of the above Evaluations during each selection
                        rand_eval=randint(1,4)
                        if rand_eval==1:
                            max_length=0
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==2: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==3: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==4: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==6: # Accepting Only the Longest Edge or Second Longest
                        max_length=0
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            if length>max_length:
                                max_length=length
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge or Second_Minimum
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            distributed_cost=i[3]/(i[1]-i[0])
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            distributed_cost=i[3]/cumulative_length
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                            fixed_distributed_cost=VC[i[2]]/length
                            distributed_cost=variable_distributed_cost+fixed_distributed_cost
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==10: # Doing any of the above Evaluations during each selection
                        rand_eval=randint(6,9)
                        if rand_eval==6: # Accepting Only the Longest Edge
                            max_length=0
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==11: # Doing any of the above Evaluations during each selection and taking both the Best and the Second Best
                        rand_eval=randint(6,9)
                        if rand_eval==6: # Accepting Only the Longest Edge
                            max_length=0
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        if random()>=0.33:
                            array_of_Daughter_Edges.append(potential_mother_edge)
                            if random()>0.97:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif random()>=0.33:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)
                            if random()>0.97:
                                array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                            else:
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


    def Decoding_Mechanism_Randomised(Node_Sequence):

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
                print("EXCEPTION: Please Check Code")
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
                    evaluation_process=randint(0,12) # This is Unique: The others are for when 1 single Decoding Sequence call uses the same Evaluation_Process. This however randomises within it as well...

                    if evaluation_process==12:  # Randomly Accepting 1 or 2 Daughter Edges
                        rand_position=randint(0,length_of_Daughter_array-1)
                        if random()>=0.75:
                            rand_position_2=rand_position
                            while rand_position==rand_position_2:
                                rand_position_2=randint(0,length_of_Daughter_array-1)
                            array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position_2])
                        array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position])

                    elif evaluation_process==0: # Randomly Accepting 1 Daughter Edge
                        rand_position=randint(0,length_of_Daughter_array-1)
                        array_of_Daughter_Edges.append(array_containing_all_Daughter_Edges[rand_position])

                    elif evaluation_process==1: # Accepting Only the Longest Edge
                        max_length=0
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            if length>max_length:
                                max_length=length
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==2: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            distributed_cost=i[3]/(i[1]-i[0])
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==3: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            distributed_cost=i[3]/cumulative_length
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==4: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                            fixed_distributed_cost=VC[i[2]]/length
                            distributed_cost=variable_distributed_cost+fixed_distributed_cost
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                potential_mother_edge=i
                        array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==5: # Doing any of the above Evaluations during each selection
                        rand_eval=randint(1,4)
                        if rand_eval==1:
                            max_length=0
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==2: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==3: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        elif rand_eval==4: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    potential_mother_edge=i
                            array_of_Daughter_Edges.append(potential_mother_edge)

                    elif evaluation_process==6: # Accepting Only the Longest Edge or Second Longest
                        max_length=0
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            if length>max_length:
                                max_length=length
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge or Second_Minimum
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            distributed_cost=i[3]/(i[1]-i[0])
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            distributed_cost=i[3]/cumulative_length
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                        minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                        potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                        second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                        for i in array_containing_all_Daughter_Edges:
                            length=i[1]-i[0]
                            cumulative_length=length*(length+1)/2
                            variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                            fixed_distributed_cost=VC[i[2]]/length
                            distributed_cost=variable_distributed_cost+fixed_distributed_cost
                            if distributed_cost<minimum_Distributed_Cost:
                                minimum_Distributed_Cost=distributed_cost
                                second_potential_mother_edge=potential_mother_edge
                                potential_mother_edge=i
                        if randint(-1,1):
                            array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==10: # Doing any of the above Evaluations during each selection
                        rand_eval=randint(6,9)
                        if rand_eval==6: # Accepting Only the Longest Edge
                            max_length=0
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif rand_eval==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(potential_mother_edge)
                            else:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)

                    elif evaluation_process==11: # Doing any of the above Evaluations during each selection and taking both the Best and the Second Best
                        rand_eval=randint(6,9)
                        if rand_eval==6: # Accepting Only the Longest Edge
                            max_length=0
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                if length>max_length:
                                    max_length=length
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==7: # Accepting the Minimum Cost wrt Number of Nodes in that Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                distributed_cost=i[3]/(i[1]-i[0])
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==8: # Accepting the Minimum Cost wrt Cumulative Number of Nodes of the Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                distributed_cost=i[3]/cumulative_length
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        elif rand_eval==9: # Accepting the Minimum Cost; Here Cost is Variable_Cost/Cumulative_Number_of_Nodes + Fixed_Cost/Number_of_Nodes of any Edge
                            minimum_Distributed_Cost=99999999999999999999999999999999999999999999999
                            potential_mother_edge=array_containing_all_Daughter_Edges[-1]
                            second_potential_mother_edge=array_containing_all_Daughter_Edges[-2]
                            for i in array_containing_all_Daughter_Edges:
                                length=i[1]-i[0]
                                cumulative_length=length*(length+1)/2
                                variable_distributed_cost=(i[3]-VC[i[2]])/cumulative_length
                                fixed_distributed_cost=VC[i[2]]/length
                                distributed_cost=variable_distributed_cost+fixed_distributed_cost
                                if distributed_cost<minimum_Distributed_Cost:
                                    minimum_Distributed_Cost=distributed_cost
                                    second_potential_mother_edge=potential_mother_edge
                                    potential_mother_edge=i
                        if random()>=0.3:
                            array_of_Daughter_Edges.append(potential_mother_edge)
                            if random()>=0.6:
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                        elif random()>=0.3:
                            array_of_Daughter_Edges.append(second_potential_mother_edge)
                            if random()>=0.6:
                                array_of_Daughter_Edges.append(potential_mother_edge)
                        else:
                            if randint(-1,1):
                                array_of_Daughter_Edges.append(second_potential_mother_edge)
                            else:
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



    print("\n ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~ \n")
    print("\n ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~ \n")
    print("Starting ATSAH following Evaluation Process")
    print("\n ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~ \n")
    print("\n ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~ \n")
    Node_Sequence,Latitude,Longitude,PickUps,Deliveries=GeneRead.Reader.Relief_Centre_Reader(directory_of_Relief_Centre_Specifications_file=directory_containing_Node_Locations_file)
    Vehicle_Types,VN,VQ,VS,VC,Vehicle_Width=GeneRead.Reader.Vehicle_Type_Reader(directory_containing_Vehicle_Types_file)
    C=GeneRead.Reader.Distance_Combinations_Reader(directory_containing_Distance_Locations_file=directory_containing_Distance_Matrix_file,directory_of_Vehicle_Types_considered_file=directory_containing_Vehicle_Types_file)


    textfile = open(directory_to_save_ATSAH_solution+"Vehicle Routes from ATSAH.txt","w")

    N=6 # Neighbourhood Structure Numbers
    Ci=1
    ii=1
    ultimate_counter=0

    # Obtaining the First Solution
    Depot_First_Node=Node_Sequence[0]
    Node_Sequence_Intermediate=Node_Sequence
    first_solution_start_time=time.time()
    #Shuffle_Random(Node_Sequence)
    x=Decoding_Mechanism_Randomised(Node_Sequence)
    """
    while x==-1:
        Shuffle_Random(Node_Sequence)
        General_Swap(Node_Sequence)
        Single_Insertion(Node_Sequence)
        Reversal(Node_Sequence)
        Adjacent_Swap(Node_Sequence)
        SubArray_Transplant_Allowing_Operations(Node_Sequence)
        #print(Node_Sequence)
        x=Decoding_Mechanism_for_First_Time(Node_Sequence)
    """
    first_solution_end_time=time.time()

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

    time_limit=0.99
    if delta_T >= time_limit:
        message="\n The first single solution from the Decoding Mechanism is taking more than "+str(time_limit)+" seconds, therefore this may not end fast. Please change other parameters or this ending criteria \n"
        print(message)
        textfile.write(message)
        textfile.close()
        return x,delta_T,ultimate_counter


    x_b=x
    x_dash=x
    age=0
    f=0
    a1=x_b[0]/x[0]
    a2=Ci/ii
    t=1+a1*a2
    f_iter=25+len(Node_Sequence)/5

    start_time=time.time()
    while f<f_iter:
        ultimate_counter+=1 # This Value multiplied by 12 gives the Number of time different Decoding Mechanisms were called

        for eval_process in range(0,12):
            Node_Sequence_1=Node_Sequence.copy()
            Adjacent_Swap(Node_Sequence_1)
            x_dash_1=Decoding_Mechanism(Node_Sequence_1,eval_process)
            if x_dash_1[0]<x_dash[0]:
                x_dash=x_dash_1
                Node_Sequence_Intermediate=Node_Sequence_1
            Node_Sequence_2=Node_Sequence.copy()
            General_Swap(Node_Sequence_2)
            x_dash_2=Decoding_Mechanism(Node_Sequence_2,eval_process)
            if x_dash_2[0]<x_dash[0]:
                x_dash=x_dash_2
                Node_Sequence_Intermediate=Node_Sequence_2
            Node_Sequence_3=Node_Sequence.copy()
            Single_Insertion(Node_Sequence_3)
            x_dash_3=Decoding_Mechanism(Node_Sequence_3,eval_process)
            if x_dash_3[0]<x_dash[0]:
                x_dash=x_dash_3
                Node_Sequence_Intermediate=Node_Sequence_3
            Node_Sequence_4=Node_Sequence.copy()
            Node_Sequence_4=Reversal(Node_Sequence_4)
            x_dash_4=Decoding_Mechanism(Node_Sequence_4,eval_process)
            if x_dash_4[0]<x_dash[0]:
                x_dash=x_dash_4
                Node_Sequence_Intermediate=Node_Sequence_4
            Node_Sequence_5=Node_Sequence.copy()
            Shuffle_Random(Node_Sequence_5)
            x_dash_5=Decoding_Mechanism(Node_Sequence_5,eval_process)
            if x_dash_5[0]<x_dash[0]:
                x_dash=x_dash_5
                Node_Sequence_Intermediate=Node_Sequence_5
            Node_Sequence_6=Node_Sequence.copy()
            SubArray_Transplant_Allowing_Operations(Node_Sequence_6)
            x_dash_6=Decoding_Mechanism(Node_Sequence_6,eval_process)
            if x_dash_6[0]<x_dash[0]:
                x_dash=x_dash_6
                Node_Sequence_Intermediate=Node_Sequence_6

        x_dash_7=Decoding_Mechanism_Randomised(Node_Sequence_Intermediate)
        if x_dash_7[0]<x_dash[0]:
            x_dash=x_dash_7
        x_dash_8=Decoding_Mechanism_Randomised(Node_Sequence)
        if x_dash_8[0]<x_dash[0]:
            x_dash=x_dash_8
            Node_Sequence_Intermediate=Node_Sequence
        
        #Node_Sequence=Node_Sequence_Intermediate.copy()
        Node_Sequence=Node_Sequence_Intermediate

        if x_dash[0]<=t*x_b[0]:
            x=x_dash
            ii+=1
            age=0
            if x[0]<x_b[0]:
                end_time=time.time()
                delta_T=end_time-start_time

                print("The present value of f is ",f)
                f=0
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
                print("\n")

            else:
                f+=1
            a1=x_b[0]/x[0]
            a2=Ci/ii
            t=1+a1*a2
        else:
            age+=1
            if age==N:
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

        name="Used "+str(x_b[3][k])+" Vehicles of Type "+str(k)+" having Capacity_ "+str(VQ[k])+".eps"
        main_dir_for_Image=directory_to_save_ATSAH_solution+"{}"
        plt.savefig(main_dir_for_Image.format(name),format='eps', bbox_inches = 'tight')
        #plt.figure().clear()
        #plt.cla()
        #plt.clf()
        plt.close()

    # returns Objective Function Value, Routes Message, All selected Edge Solutions, Number of Vehicle Used of each Type and the Time Taken to compute this Solution
    return x_b,delta_T,ultimate_counter