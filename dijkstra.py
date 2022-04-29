from math import sqrt
from operator import eq

    
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
        
    def equation (self, node_2) :
        """Calculate the equation of the line between the node and a second node
        Args : the second node
        Returns : [slope, intersect] or ['vertical', x] in case of vertical lines
        """
        flag = False
        try :
            coeff = (node_2.y_pos - self.y_pos)/(abs(node_2.x_pos - self.x_pos))
        except ZeroDivisionError :
            coeff = 'vertical'
            flag = True
    
        try : 
            if flag :
                ord = node_2.x_pos
            else :
                ord = self.y_pos - ((node_2.y_pos - self.y_pos)/(node_2.x_pos - self.x_pos))*self.x_pos
        except ZeroDivisionError :
            ord = 0
        
        equa = [coeff, ord, self, node_2]
        return (equa)
        
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
        
    
    def inv_equation (self, node_2) :
        """Calculate the inverse equation of the droite between the two nodes
        Corresponds to a pi/2 anti trigonometric translation of the axis"""
        
        norm_equation = self.equation(node_2)
        try :  
            if norm_equation[0] == 0 :
                return 
            inv_equation = [1/norm_equation[0], norm_equation[1]]
        except TypeError :
            return (norm_equation)
        return (inv_equation)

    def all_equations_block (self) :
        """Calculates the equations of the block nodes"""
        equations = {}
        for i in range (len (self.all_nodes)) :
            for j in range (len(self.all_nodes)) :
                if i == j :
                    pass
                else :
                    #verify that the calculated equations are for block node type only and if the nodes are neighbours 
                    if self.all_nodes[i].node_type == 'block' and self.all_nodes[j].node_type == 'block' \
                        and self.all_nodes[i].id in self.all_nodes[j].neigh and self.all_nodes[j].id in self.all_nodes[i].neigh :
                        node_1 = self.all_nodes[i]
                        node_2 = self.all_nodes[j]
                        equations [f'{node_1.id}{node_2.id}'] =  node_1.equation(node_2) 
                        equations [f'{node_2.id}{node_1.id}'] =  node_1.inv_equation(node_2)
        return equations
    

    # def verif_block (self, node_goal) :
        
    #     equations = self.all_equations()
        
    #     for i in range (len(equations)) :
    #         if equations[i][0].is_goal_node() and equations[i][1].is_start_node() :
    #             print("lol")
            
            

### Programme principal

A = Node ('A', 0, 0, 'BCE', 'goal')
B = Node ('B', 30, 20, 'ACE', 'block')
C = Node ('C', 30, 40, 'ADB', 'block')
D = Node ('D', 50, 40, 'CE', 'block')
E = Node ('E', 50, 20, 'DB', 'block')
F = Node ('F', 80, 60, 'ABCDE', 'start') #must be linked to all other nodes

# print(A.dist(B))
# print(A.equation(B))
# print(A.all_equations_block())

print(A.get_all_block())

    