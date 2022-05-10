from math import sqrt, ceil
from operator import eq
from shapely.geometry import LineString, Point

class Node () :
    
    all_nodes = []
    goal_node_id = 'A'
    stat_node_id = 'F'
    
    def __init__(self, id = str, x_pos = int, y_pos = int, neigh = str, node_type = str) : 
        
        self.id = id
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.neigh = neigh
        self.node_type = node_type
        
        self.distance = {}
        self.ray = {}
        
        self.all_nodes.append(self)

    def dist (self, node_2):
        """Calculate the geometrical distance between the node and a seconde one
        Args : the second node
        Returns : the algebric distance 
        """
        return(sqrt( abs(self.x_pos - node_2.x_pos)**2 + abs(self.y_pos - node_2.y_pos)**2))
    
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
        block_nodes = []
        for i in range (len(self.all_nodes)) :
            if self.all_nodes[i].is_block_node () :
                block_nodes.append(self.all_nodes [i])
        return block_nodes

    def block_intersection (self, start_node, goal_node) :
        """Verify that a block is obstruing the path"""
        intersections = []
        block_nodes = self.get_all_block ()
        block_nodes_pos = [ [block_nodes [i].x_pos, block_nodes [i].y_pos] for i in range (len(block_nodes))]
        
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
        """create a notation based on the nature of the intersection (block node or else)"""
        
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
        """actualize real interaction through nodes (depending on block) in each node"""
        
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
            
    def djikstra_algo (self, starting_node, goal_node):
        graph = self.djikstra_format()
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

        goal_node_name = str(goal_node.id)
        
        print(f'The path between {goal_node_name} to {initial_id}')
        print(goal_node_name, end = '<-')
        
        while True :
            goal_node_name = adj_node[goal_node_name]
            if goal_node_name is None:
                print("")
                break
            print(goal_node_name, end = '<-')
    
### Programme principal

A = Node ('A', 0, 0, 'BCDEF', 'goal')
B = Node ('B', 30, 20, 'ACDEF', 'block')
C = Node ('C', 30, 40, 'ABDEF', 'block')
D = Node ('D', 50, 40, 'ABCEF', 'block')
E = Node ('E', 50, 20, 'ABCDF', 'block')
F = Node ('F', 60, 50, 'ABCDE', 'start')

### Programme principal

#initialize the graph path
A.knock_out_path()

formated_paths = A.djikstra_format()
print(A.djikstra_algo(F,A))
