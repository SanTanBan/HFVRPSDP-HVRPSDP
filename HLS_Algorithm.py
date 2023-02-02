import time
import pandas as pd
import matplotlib.pylab as plt
import os
import openpyxl
import random
from random import randint
import GeneRead

def HLS_Algorithm(directory_details_for_saving="",directory_containing_Vehicle_Types_file="",directory_containing_Node_Locations_file="",directory_containing_Distance_Matrix_file=""):

    os.mkdir(directory_details_for_saving+"HLS Algorithm Solution")
    directory_to_save_HLS_solution=directory_details_for_saving+"HLS Algorithm Solution/"

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

    def Dijktra_Dynamic_Programming(Node_Sequence=[],edges_with_Costs={}):
        # In the present case, the EDGES Dictionary has the KEY as (starting Node,ending Node,Vehicle Type) and the VALUE as Cost of the Edge
        # Applying Dijktra's Algorithm / Dynamic Programming to find the shortest path among the above routes
        Min_Cost_Array=[]
        Upto_Len=len(Node_Sequence)
        for i in range(len(Node_Sequence)):
            # This Dijktra / Dynamic Programming Array (Min_Cost_Array) will have (Minimum Cost,Next Node Position in Array Sequence,Vehicle Type) as its individual elements
            # So the last Node will have (0,0,-1) indicating Zero Cost as No Next Node and No Vehicle Type
            Min_Cost_Array.append((0,-1,-1))
        for i in range(Upto_Len-2,-1,-1):
            minim=999999999 # This should be a Very Large Number
            for j in edges_with_Costs:
                delete_bin=set()
                if j[0]==i:
                    compare=edges_with_Costs[j]+Min_Cost_Array[j[1]][0]
                    #print("This is compare",compare)
                    #print("this is min",min)
                    if compare<minim:
                        minim=compare
                        Min_Cost_Array[i]=(minim,j[1],j[2])
                    delete_bin.add(j) # Removing the used Edge from the subsequent search space after the loop is done
            for j in delete_bin:
                del edges_with_Costs[j]
        # The Min_Cost_Array refers to the indexes of the Node_Sequences
        return Min_Cost_Array

    def Decoding_Mechanism(Node_Sequence):
        Depot_First_Node=Node_Sequence[0]
        if Node_Sequence[0]!=0:
            # This check is for the specific problem considered in the Paper
            for just_some_screen_space in range(99):
                print("EXCEPTION: Please Check Code")
            return

        # Node Sequence should be an array starting from 0th Node and containing other Node Indexes, example 0,1,8,6,7
        set_of_routes={}
        Upto_Len=len(Node_Sequence)-1
        for i in range(Upto_Len):
            for k in Vehicle_Types:
                DynamicCapacityLeft=[VQ[k]]
                Edge=VC[k]+VS[k]*C[0,Node_Sequence[i+1],k]
                for j in range(i+1,Upto_Len+1):
                    CapacityCheck=0
                    #print(DynamicCapacityLeft[0])
                    DynamicCapacityLeft[0]=DynamicCapacityLeft[0]-Deliveries[Node_Sequence[j]]
                    DynamicCapacityLeft.append(Deliveries[Node_Sequence[j]]-PickUps[Node_Sequence[j]])
                    for m in DynamicCapacityLeft:
                        CapacityCheck+=m
                        if CapacityCheck<0:
                            break
                    if CapacityCheck<0:
                        break
                    #key=(Node_Sequence[i],Node_Sequence[j],k)
                    key=(i,j,k)
                    if j>i+1:
                        Edge+=VS[k]*C[Node_Sequence[j-1],Node_Sequence[j],k]
                    set_of_routes[key]=Edge+VS[k]*C[Node_Sequence[j],0,k]

        # Applying Dijktra's Algorithm / Dynamic Programming to find the shortest path among the above routes
        Min_Cost_Array=Dijktra_Dynamic_Programming(Node_Sequence=Node_Sequence,edges_with_Costs=set_of_routes.copy())

        Num_of_Vehicle_of_each_Type_being_used={}
        for k in Vehicle_Types:
            Num_of_Vehicle_of_each_Type_being_used[k]=0

        message="Routes:- \n "
        interval_start=0
        inter_startup=0
        Next_Node=Min_Cost_Array[0][1]
        while Next_Node!=-1:
            message+=" Vehicle Type "+str(Min_Cost_Array[inter_startup][2])+" : \t "
            Num_of_Vehicle_of_each_Type_being_used[Min_Cost_Array[inter_startup][2]]+=1
            # Dictionary with KEY baing the Vehicle ype Indes and VALUE being the Number of Times this Vehicle Type is considered
            if interval_start!=0:
                message+=str(Depot_First_Node)+" --> "
            for i in range(interval_start,Next_Node+1):
                message+=str(Node_Sequence[i])+" --> "
            message+=str(Depot_First_Node)+" \n "
            inter_startup=Next_Node
            interval_start=Next_Node+1
            Next_Node=Min_Cost_Array[Next_Node][1]
        
        start=Depot_First_Node
        solution=set()
        Next_Node=Min_Cost_Array[0][1]
        while Next_Node!=-1:
            solution.add((Depot_First_Node,Node_Sequence[start+1],Min_Cost_Array[start][2]))
            for i in range(start+1,Next_Node):
                solution.add((Node_Sequence[i],Node_Sequence[i+1],Min_Cost_Array[start][2]))
            solution.add((Node_Sequence[Next_Node],Depot_First_Node,Min_Cost_Array[start][2]))
            start=Next_Node
            Next_Node=Min_Cost_Array[Next_Node][1]
        # For this arrangement of Node Sequence, Returns the Most Minimum Cost, Message Containing the Information of the Routes, Solution
        # The Solution is represented as set of only those X(i,j,k)==1, where i to j is he traversed From and To Nodes by a Vehicle Type K
        return Min_Cost_Array[0][0],message,solution,Num_of_Vehicle_of_each_Type_being_used

    Node_Seq,Latitude,Longitude,PickUps,Deliveries=GeneRead.Reader.Relief_Centre_Reader(directory_of_Relief_Centre_Specifications_file=directory_containing_Node_Locations_file)
    Vehicle_Types,VN,VQ,VS,VC,Vehicle_Width=GeneRead.Reader.Vehicle_Type_Reader(directory_containing_Vehicle_Types_file)
    C=GeneRead.Reader.Distance_Combinations_Reader(directory_containing_Distance_Locations_file=directory_containing_Distance_Matrix_file,directory_of_Vehicle_Types_considered_file=directory_containing_Vehicle_Types_file)

    textfile = open(directory_to_save_HLS_solution+"Vehicle Routes from HLS Heuristic of Paper.txt","w")
    Tabu_List=[] # The ingredients of the return statement of the function Decoding Mechanism contains other sets and Python does not allow sets within sets. Also we need to limit this to 50 elements
    N=4 # Neighbourhood Structure Number
    Ci=1
    ii=1

    # Shuffling the initial Node Sequence
    Depot_First_Node=Node_Seq[0]
    Node_Sequence=Node_Seq[1::+1]
    random.shuffle(Node_Sequence)
    Node_Sequence.insert(0,Depot_First_Node)

    x=Decoding_Mechanism(Node_Sequence)

    Tabu_List.append(x)
    x_b=x
    age=0
    f=0
    a1=x_b[0]/x[0]
    a2=Ci/ii
    t=1+a1*a2
    f_iter=500

    start_time=time.time()
    while f<f_iter:
        ppass=0
        while ppass==0:
            Node_Sequence_1=Node_Sequence.copy()
            Adjacent_Swap(Node_Sequence_1)
            x_dash=Decoding_Mechanism(Node_Sequence_1)
            Node_Sequence_Intermediate=Node_Sequence_1
            
            Node_Sequence_2=Node_Sequence.copy()
            General_Swap(Node_Sequence_2)
            x_dash_2=Decoding_Mechanism(Node_Sequence_2)
            if x_dash_2[0]<x_dash[0]:
                x_dash=x_dash_2
                Node_Sequence_Intermediate=Node_Sequence_2

            Node_Sequence_3=Node_Sequence.copy()
            Single_Insertion(Node_Sequence_3)
            x_dash_3=Decoding_Mechanism(Node_Sequence_3)
            if x_dash_3[0]<x_dash[0]:
                x_dash=x_dash_3
                Node_Sequence_Intermediate=Node_Sequence_3

            Node_Sequence_4=Node_Sequence.copy()
            Node_Sequence_4=Reversal(Node_Sequence_4)
            x_dash_4=Decoding_Mechanism(Node_Sequence_4)
            if x_dash_4[0]<x_dash[0]:
                x_dash=x_dash_4
                Node_Sequence_Intermediate=Node_Sequence_4
            
            #Node_Sequence=Node_Sequence_Intermediate.copy()
            Node_Sequence=Node_Sequence_Intermediate

            counter=1
            for inside_Tabu in Tabu_List:
                if inside_Tabu[0]==x_dash[0]:
                    if inside_Tabu[2]==x_dash[2]:
                            counter=0
                            break
            if counter==1:
                ppass=1

        if x_dash[0]<=t*x_b[0]:
            x=x_dash
            ii+=1
            age=0
            if len(Tabu_List)==50: # Length of the Tabu list is hereby limited to 50 elements
                del Tabu_List[0]
            Tabu_List.append(x)
            if x[0]<x_b[0]:
                f=0
                x_b=x
                Ci+=1

                textfile.write(str("\n"))
                textfile.write("Objective Function Value \t "+str(x_b[0])+"\n")
                textfile.write(str(x_b[1]))
                textfile.write("Solutions (Origin Node,Destination Node,Vehicle Type):- "+str(x_b[2]))
                textfile.write("\n Vehicles Used (Vehicle Type Index : Number of Vehicles Used of this Type) \t "+str(x_b[3]))
                textfile.write(str("\n \n"))
                
                print("\n")
                print(x_b)
                print("\n \n")
                
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
    print("The final output was obtained after "+str(delta_T)+" seconds.")
    textfile.write("\n The final output was obtained after "+str(delta_T)+" seconds.\n")
    for k in Vehicle_Types:
        # Maximum number of vehicles being used for each Vehicle Type
        print(x_b[3][k]," vehicles of Vehicle Type "+str(k)+" are used")
        textfile.write(str(x_b[3][k])+" vehicles of Vehicle Type "+str(k)+" are used \n")
    textfile.close()

    """# Plotting the Depot and Relief Centres
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
                routes.append((element[0],element[1]))

        # Drawing the optimal routes Layerwise
        Current_Node=Depot_First_Node
        colour_intervals=len(routes)
        for count in range(colour_intervals):
            for i,j in routes:
                if i==Current_Node:
                    plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="simple", connectionstyle='arc3', edgecolor=(count/colour_intervals,1-(count/colour_intervals),1)))
                    #plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="-|>", connectionstyle='arc3', edgecolor=(count/colour_intervals,1-(count/colour_intervals),1)))
                    #plt.annotate('', xy=[Longitude[j], Latitude[j]], xytext=[Longitude[i], Latitude[i]], arrowprops=dict(arrowstyle="simple", connectionstyle='angle3', edgecolor=(count/colour_intervals,1-(count/colour_intervals),1)))
                    # Edge_Notes="P="+str(y[i,j,k].varValue)+" ; D="+str(z[i,j,k].varValue) How to get this? Is this necessary?
                    #plt.text((Longitude[i]+Longitude[j])/2, (Latitude[i]+Latitude[j])/2, f'{Edge_Notes}',fontweight="bold")
                    # Directly load the Vehicle with the sum of the Demands and route it so that it may take up the PickUps from the respective Nodes after individual Deliveries
                    Current_Node=j
                    break
            routes.remove((i,j))

        # Finding the Maximum Utilised Vehicle Capacity for each Vehicle Type?

        name="Used "+str(x_b[3][k])+" Vehicles of Type "+str(k)+" having Capacity_ "+str(VQ[k])+".png"
        main_dir_for_Image=directory_to_save_HLS_solution+"{}"
        plt.savefig(main_dir_for_Image.format(name))"""


    # returns Objective Function Value, Routes Message, All selected Edge Solutions, Number of Vehicle Used of each Type and the Time Taken to compute this Solution
    return x_b,delta_T