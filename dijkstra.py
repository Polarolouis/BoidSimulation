from math import sqrt, ceil
from typing import final
from shapely.geometry import LineString, Point
import copy

class Node () :
    
    all_nodes = []
    
    def __init__(self, id = str, x_pos = int, y_pos = int, neigh = str, node_type = str) : 
        """
        Node class initialisation
            Args:
                id (str): identification of the node
                x_pos (int): x_position
                y_pos (int): y_position
                neigh (str): the neighbour nodes
                node_type (str): the node type
        """
        self.id = id
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.neigh = neigh
        self.node_type = node_type
        
        #initialisation of the list of nodes
        self.all_nodes.append(self)
        
    def __str__ (self) :
        """
        Sumary of a node
            Args :
            Returns :
                the output of the node for a print
        """
        return (f'the id of the node: {self.id} \n   x position : {self.x_pos} \n   y position : {self.y_pos} \n   the neighbour nodes : {self.neigh} \n   the node type : {self.node_type} \n')
    
    def dist (self, node_2):
        """
        Calculate the geometrical distance between the node and a seconde one
            Args : 
                node_2 (Node): the second node
            Returns :
                the algebric distance between the self.node and the node_2
        """
        return(sqrt( abs(self.x_pos - node_2.x_pos)**2 + abs(self.y_pos - node_2.y_pos)**2))
    
    def generate_ligne_eq (self, node_2) :
        """
        Calculate the line equation between the self.node and a seconde one
            Args : 
                node_2 (Node): the second node
            Returns :
                the algebric linear equation between the self.node and the node_2
        """
        x1 , y1 = self.x_pos , self.y_pos
        x2 , y2 = node_2.x_pos, node_2.y_pos
        try : 
            slope = float(y2-y1)/(x2-x1)
        except ZeroDivisionError :
            slope = 0
        intercept = slope*(-x1) + y1
        return ([slope, intercept])
        
    def is_goal_node (self) :
        return (self.node_type == 'goal')
    
    def is_start_node (self) :
        return (self.node_type == 'start')
    
    def is_block_node (self) :
        return (self.node_type == 'block')
    
    def get_a_node (self, node_name = str) :
        for i in range (len(self.all_nodes)) :
            if self.all_nodes[i].id == node_name :
                return (self.all_nodes[i])
            
    def get_all_block (self) :
        """"
        Gives back all the nodes that are "block" type
            Args : 
            Returns :
                block_nodes (list): a list containing all the block nodes 
        """
        block_nodes = []
        for i in range (len(self.all_nodes)) :
            if self.all_nodes[i].is_block_node () :
                block_nodes.append(self.all_nodes [i])
        return block_nodes

    def block_intersection (self, start_node, goal_node) :
        """
        Verify that a block is obstruing the path
            Args : 
                start_node (Node): the beginning path node, goal_node = the end path node
            Returns : 
                intersections (list): the list containing all the [x,y] values of the intersection(s) with the block
        """
        intersections = []
        block_nodes = self.get_all_block ()
        
        A = (start_node.x_pos, start_node.y_pos)
        B = (goal_node.x_pos, goal_node.y_pos)
        line1 = LineString([A, B])
        
        for i in range (len (block_nodes)-1) :
            C = (block_nodes[i].x_pos, block_nodes[i].y_pos)
            D = (block_nodes[i+1].x_pos, block_nodes[i+1].y_pos)
            line2 = LineString([C, D])

            try :
                intersec_pt = line1.intersection(line2)
                intersec_pt_pos = [intersec_pt.x, intersec_pt.y]
                intersections.append (intersec_pt_pos) 
                                   
            except AttributeError :
                pass
        return(intersections)
    
    def notation_intersections (self, intersections) :
        """
        Create a notation based on the nature of the intersection (block node or else)
            Args : 
                intersections (list):  the list of intersections for two segments (given by self.block_intersection)
            Returns : 
                ceil_value (int): the up-rounded intersection value
        """
        
        block_nodes = self.get_all_block ()
        block_nodes_pos = [ [block_nodes [i].x_pos, block_nodes [i].y_pos] for i in range (len(block_nodes))]
        
        value = 0.0
        for i in range (len(intersections)) :
            if intersections[i] in block_nodes_pos :
                value += 0.5
            else : 
                value += 1
        return (ceil(value))

    def knock_out_path (self) :
        """
        Actualize real paths through the graph (depending on block) for each node
            Args : 
            Returns : 
        """
        
        for i in range (len (self.all_nodes)) :
            actual_neigh = ""
            for j in range (len (self.all_nodes[i].neigh)) :
                intersections = self.block_intersection (self.all_nodes[i], self.get_a_node(self.all_nodes[i].neigh[j]))
                if self.notation_intersections (intersections) == 2 :
                    pass
                else :
                    actual_neigh += self.all_nodes[i].neigh[j]
            self.all_nodes[i].neigh = actual_neigh

    def djikstra_format (self) :
        """
        Changes the notations of nodes to better fit the djikstra algorithm
            Args : 
            Returns : a dict which has the following caracteristic
                {
                    'Node1' : {'Node2 : dist between Node1 and Node2, ...}
                    .....
                }
        """
        formatted_nodes = {}
        for i in range (len(self.all_nodes)) :
            neigh_dist = {}
            for j in range (len(self.all_nodes[i].neigh)) :
                cur_neigh_node = self.get_a_node (self.all_nodes[i].neigh[j])            
                neigh_dist[f'{self.all_nodes[i].neigh[j]}'] = self.all_nodes[i].dist(cur_neigh_node)
            
            formatted_nodes[f'{self.all_nodes[i].id}'] = neigh_dist
        return (formatted_nodes)          
            
    def djikstra_algo (self, formatted_nodes, starting_node, goal_node):
        """
        Finds the shortest path in a graph
            Args:
                formated_paths (dict): the formated infos on the graph network for the dijksta's algo
                starting_node (Node): the beginning node
                goal_node (Node): the end node
            Returns:
                final_node_path (list of Nodes.id): the path, from the starting_node to the goal_node
        """
        graph = formatted_nodes
        initial_id = str(starting_node.id)
        path = {} 
        adj_node = {} 
        node_queue = []

        for node in graph :
            path[node] = float("inf")
            adj_node[node] = None
            node_queue.append(node)
        
        path[initial_id] = 0

        while node_queue :
            key_min_val = node_queue[0]
            min_val = path[key_min_val]
            
            for n in range(1, len(node_queue)):
                if path[node_queue[n]] < min_val:
                    key_min_val = node_queue[n]
                    min_val = path[key_min_val]
            current_node = key_min_val
            node_queue.remove(current_node)
            
            for i in graph[current_node]:
                alternate = graph[current_node][i] + path[current_node]
                if path[i] > alternate:
                    path[i] = alternate
                    adj_node[i] = current_node
                    
        goal_node_dji = copy.deepcopy( goal_node )
        
        final_node_path = []
        final_node_path.append(goal_node_dji.id)
        
        while True :
            
            goal_node_dji.id = adj_node[goal_node_dji.id]
            if goal_node_dji.id is None:
                break
            final_node_path.append(goal_node_dji.id)
        return(final_node_path)
    
    def path_direction (self, final_node_path) :
        """
        Generates the equations for each path between the node
            Args:
                final_node_path (list of Nodes): the path, from the starting_node to the goal_node
            Returns:
                ligne_eqs (list): the list of equations from the starting_node to goal_node
                in that format [ [slope] [intercept], [slope] [intercept] ...  ]
                
        """
        ligne_eqs = []
        for i in range (len(final_node_path)-1):
            current_start_node = self.get_a_node(final_node_path[i])
            current_goal_node = self.get_a_node(final_node_path[i+1])
            ligne_eqs.append(current_start_node.generate_ligne_eq(current_goal_node))
        return(ligne_eqs)