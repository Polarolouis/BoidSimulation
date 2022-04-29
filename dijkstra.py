from math import sqrt
from operator import eq
from shapely.geometry import LineString, Point

    
def djikstra():
    graph = initial_graph()
    initial = 'F' #2

    path = {} #3

    adj_node = {} #4

    queue = [] #5

    graph = initial_graph() #6

    for node in graph:
        path[node] = float("inf")
        adj_node[node] = None
        queue.append(node)

    path[initial] = 0

    while queue:

        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                key_min = queue[n]
                min_val = path[key_min]
        cur = key_min
        queue.remove(cur)

        for i in graph[cur]:
            alternate = graph[cur][i] + path[cur]
            if path[i] > alternate:
                path[i] = alternate
                adj_node[i] = cur

    x = 'A'
    print('The path between A to F')
    print(x, end = '<-')
    while True:
        x = adj_node[x]
        if x is None:
            print("")
            break
        print(x, end='<-')

class Node () :
    
    all_nodes = []
    goal_node_id = 'A'
    stat_node_id = 'F'
    
    def __init__(self, id = str, x_pos = int, y_pos = int, neigh = str, node_type = str) : 
        
        self.id = id
        self.x_pos = x_pos
        self.y_pos = y_pos
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
    
    def get_all_block (self) :
        block_nodes = []
        for i in range (len(self.all_nodes)) :
            if self.all_nodes[i].is_block_node () :
                block_nodes.append(self.all_nodes [i])
        return block_nodes
        
    def djikstra_format (self) :
        #     return {

#         'A': {'B':36.055, 'C':50, 'E':53.852},
#         'B': {'A':36.055, 'E':20, 'C':20},
#         'C': {'A':50, 'B':20, 'D':20},
#         'D': {'C':20, 'E':20},
#         'E': {'B':20, 'D':20, 'A':53.852},
#         'F': {'A':sqrt(i[0]**2+i[1]**2),'B':sqrt((i[0]-20)**2+(i[1]-30)**2)'C':sqrt((i[0]-30)**2+(i[1]-40)**2), 'D':sqrt((i[0]-30)**2+(i[1]-40)**2), 'E':53.852}
#             }
        print("haha")

    def verify_block (self, start_node, goal_node) :
        """verify that a block is obtruing the path"""
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
                int_pt = line1.intersection(line2)
                intersections.append ([int_pt.x, int_pt.y])
            except AttributeError :
                pass
        return(intersections)
            
            

### Programme principal

A = Node ('A', 0, 0, 'BCE', 'goal')
B = Node ('B', 30, 20, 'ACE', 'block')
C = Node ('C', 30, 40, 'ADB', 'block')
D = Node ('D', 50, 40, 'CE', 'block')
E = Node ('E', 50, 20, 'DB', 'block')
F = Node ('F', 80, 60, 'ABCDE', 'start') #must be linked to all other nodes

# print(A.dist(B))

print(A.get_all_block())

print(A.verify_block(A,F))