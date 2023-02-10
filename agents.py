import numpy as np
import pandas as pd
import cv2
import joblib
from copy import deepcopy
from sklearn.neighbors import KDTree
from sortedcontainers import SortedList

class Point():

    def __init__(self, name, vertex, speed, graph, x=None, y=None, icon=None, sec_in_frame=1):
        if vertex:
            x = graph.vertex_dict[vertex].x
            y = graph.vertex_dict[vertex].y

        self.name = name
        self.speed = speed
        self.step_length = speed * sec_in_frame
        self.graph = graph
        self.x = x
        self.y = y
        self.vertex = vertex    # type == str

        self.target = None      # type == str
        self.offset = 0
        self.path = []
        if icon is None:
            self.icon_w = 16
            self.icon_h = 16
            self.icon_main = np.full((self.icon_w,self.icon_h,3), fill_value=(np.array([0, 0, 255])), dtype='int16')
        else:
            self.icon_main = icon.copy()
            self.icon_w = icon.shape[0]
            self.icon_h = icon.shape[1]
        self.icon = self.icon_main.copy()
        self.pallet = None
        self.tasks = []
        self.doing = None
        self.timer = 0
        self.moving_pause = False


    def take_pallet(self, source=None, pallet=None, *args):
        if not(self.pallet):
            if source:
                pallet = source.give_pallet(*args)
            self.pallet = pallet
            self.icon = self.icon_full.copy()
        else:
            print(f'{self.name} already has a {self.pallet}')
            ERRORS.loc[len(ERRORS)] = [f'{self.name} already has a {self.pallet}', f'vertex = {self.vertex}']


    def give_pallet(self, receiver=None, *args):
        if self.pallet:
            pal = self.pallet
            self.pallet = None
            if receiver:
                receiver.take_pallet(source=None, pallet=pal, *args)
                self.icon = self.icon_empty.copy()
            else:
                self.icon = self.icon_empty.copy()
                return pal
        else:
            print(f'{self.name} has no pallet')
            ERRORS.loc[len(ERRORS)] = [f'{self.name} has no pallet', f'vertex = {self.vertex}']


    def add_task(self, task, *args):
        self.tasks.append({task: args})


    def busy(self):
        return self.doing
    

    def set_icon_timer(self):
        empty_icon = np.ones((self.icon_h, self.icon_w, 3), dtype='uint8') * 255
        self.icon = cv2.rectangle(empty_icon, (0,0), (self.icon_h, self.icon_w-1), (0,125,255), 2)
        self.icon = cv2.putText(self.icon, str(self.timer), (1,10), cv2.FONT_HERSHEY_DUPLEX, 0.3, (0,0,0), 1)

    
    def continue_(self):
        pass


    def __repr__(self):
        return self.name





class Truck(Point):
    def __init__(self, name, vertex_key, speed, graph, x=None, y=None, icon=None, product_list=[], sec_in_frame=1):
        Point.__init__(self, name, vertex_key, speed, graph, x, y, icon, sec_in_frame)
        self.product_list = product_list
        self.pallets = []
        self.icon_empty = icon
        self.icon_full = icon

    def take_pallet(self, source=None, pallet=None, *args):
        Point.take_pallet(self, source, pallet, *args)
        self.pallets.append(pallet)
        self.pallet = None

    def give_pallet(self, receiver=None, *args):
        if self.pallets:
            self.pallet = self.pallets.pop(0)
        Point.give_pallet(*args)





class Moving_agent(Point):
    
    def __init__(self, name, vertex_key, speed, graph, x=None, y=None, icon=None, sec_in_frame=1):
        Point.__init__(self, name, vertex_key, speed, graph, x, y, icon, sec_in_frame)
        self.icon_empty = self.icon.copy()
        self.icon_full = cv2.rectangle(self.icon, (self.icon_h//4,self.icon_w//4), (int(self.icon_h*0.75), int(self.icon_w*0.7)), (0,255,255), -1)
        self.icon = self.icon_empty.copy()

        ALL_X = set()                       # список всех координат вершин графа для поиска ближайшей
        ALL_Y = set()
        self.ALL_XY = []

        for value in self.graph.vertex_dict.values():
            ALL_X.add(value.x)
            ALL_Y.add(value.y)
            self.ALL_XY.append([value.x, value.y])

        ALL_X = SortedList(ALL_X)           # для быстрого поиска индекса заданного элемента в массиве
        ALL_Y = SortedList(ALL_Y)

        self.df_XY = pd.DataFrame(columns=['X', *ALL_X], index=['Y', *ALL_Y])

        for key, value in self.graph.vertex_dict.items():
            self.df_XY[value.x][value.y] = key


    def direction(self):            
        if self.target is None:
            return (0, 0)
        else:
            target_x = self.graph.vertex_dict[self.target].x
            target_y = self.graph.vertex_dict[self.target].y

            if self.x == target_x:
                dir_x = 0

            elif self.x < target_x:
                dir_x = 1

            elif self.x > target_x:
                dir_x = -1

            if self.y == target_y:
                dir_y = 0

            elif self.y < target_y:
                dir_y = 1

            elif self.y > target_y:
                dir_y = -1    
        return dir_x, dir_y  


    def graph_search(self):         # сканирует граф 'g'
        start = self.vertex
        g = self.graph
        first_vertex = g.vertex_dict[start]
        distances = {key: None for key in g.vertex_dict.keys()}
        distances[start] = 0
        path_dict = {}                                                  #
        pq = PriorityQueue()
        pq.push(Node(first_vertex, distance=0))

        while not pq.empty:
            current_node = pq.pop()
            u = current_node.vertex.name        
            dist_u = distances[u]                       # from

            for edge in g.neighbors_for_vertex(u):
                v = edge.v
                dist_v =  distances[v]        # to

                if dist_v and dist_v == dist_u + edge.weight:
                    distances[v] = dist_v
                    path_dict[v].append(edge)

                if dist_v is None or dist_v > dist_u + edge.weight:         # если расстояние до вершины не определено или найден более короткий путь,
                    distances[v] = dist_u + edge.weight                         # то обновляем значение дистанции до вершины
                    path_dict[v] = [edge]
                    new_vertex = g.vertex_dict[v]
                    pq.push(Node(new_vertex, distances[v], prev_node=current_node))
        return path_dict


    def find_min_path(self, start, end):        # ищет минимальный муть от start до end
        path_dict = self.graph_search()
        self.path_dict = path_dict
        if not(end in path_dict.keys()):
            print(f'{self.name}: Path not find')
            self.path = []
            return None

        if len(path_dict) == 0:
            return []

        for edge in path_dict[end]:
            if edge.u == start:
                self.path = [edge]
                return
        path = []
        edge = path_dict[end][0]
        orientation = edge.orientation
        path.append(edge)
        if len(path_dict[edge.u]) == 1:
            while edge.u != start:
                edge = path_dict[edge.u][0]
                path.append(edge)
        else:
            while edge.u != start:
                ed = None
                for e in path_dict[edge.u]:
                    if e.weight == 0:
                        continue
                    if e.orientation != orientation:
                        pass
                    else:
                        ed = e
                        break
                if ed is None:
                    edge = path_dict[edge.u][0]
                else:
                    edge = ed
                path.append(edge)
                orientation = edge.orientation
        self.path = deepcopy(list(reversed(path)))
        self.path_link = path
        path_distances = [p.weight for p in path]
        self.path_distances = list(np.cumsum(path_distances))
        if self.path_distances[-1] > 9999:
            self.path = []
        return self.path


    def distance_xy(self, x1, y1, x2, y2):
        a = x1 - x2
        b = y1 - y2
        if not(a) and not(b):
            return 0
        return(a**2 + b**2)**0.5


    def trunc_step(self):
        i = False
        dist = 0
        edge = self.path[0].weight
        while dist + edge < self.step_length:
            dist += edge
            i = True
            vertex_index = self.path.pop(0).v
            vertex = self.graph.vertex_dict[vertex_index]
            if self.path:
                edge = self.path[0].weight
            else:
                self.vertex = vertex.name
                self.x = self.graph.vertex_dict[self.vertex].x
                self.y = self.graph.vertex_dict[self.vertex].y
                self.doing = None
                return 0
        if i:
            self.x = vertex.x
            self.y = vertex.y
            if self.path:
                next_vertex_key = self.path[0].v
                self.target = next_vertex_key
            else:
                pass
        return self.step_length - dist


    def move_XY(self, final_edge=False):
        step = self.trunc_step()
        target_x = self.graph.vertex_dict[self.target].x
        target_y = self.graph.vertex_dict[self.target].y
        a = target_x - self.x
        b = target_y - self.y
        if not(a) and not(b):
            return
        distanse = (a**2 + b**2)**0.5

        if abs(b) < 0.001:
            dx = step * self.direction()[0]
            dy = 0
        elif abs(a) < 0.001:
            dx = 0
            dy = step * self.direction()[1]
        else:
            dx = step / ((b / a)**2 + 1)**0.5 * self.direction()[0]
            dy = step / ((a / b)**2 + 1)**0.5 * self.direction()[1]
        offset = (dx**2 + dy**2)**0.5
       
        if self.path:
            self.path[0].weight = distanse - offset
        self.x += dx
        self.y += dy


    def move_across_path(self):
        if self.path:
            self.move_XY()
        else:
            self.doing = None
            print('Приехали')


    def go(self, target_vertex_key):
        if not(self.vertex):                                # Find nearest vertex, and make edge to it
            temp_vertex_key = f'temp({self.x} {self.y})'
            self.graph.vertex_dict[temp_vertex_key] = Vertex(temp_vertex_key, self.x, self.y)
            self.graph.edge_dict[temp_vertex_key] = []
            u =self.graph.vertex_dict[temp_vertex_key].name
            v, distance = self.find_nearest_vertex()
            self.graph.add_edge_by_indice(u, v, weight=distance)
            self.vertex = temp_vertex_key

        if self.vertex == target_vertex_key:
            print(f'{self.name}: Already in point')
            return

        self.find_min_path(self.vertex, target_vertex_key)
        if self.path:
            self.vertex = None
            self.target = self.path[0].v
            self.move_across_path()
            self.doing = 'go'
        else:
            print(f'{self.name}: GO command interrupted')


    def do_something(self, time, doing='doing_something'):
        if time > 0:
            if self.doing == 'go':
                self.doing = 'MOVING PAUSE: ' + doing
                self.moving_pause = True
                self.timer = time // SECONDS_IN_FRAME
                self.set_icon_timer()
            else: 
                self.doing = doing
            self.timer = time // SECONDS_IN_FRAME
            self.set_icon_timer()


    def continue_(self):
        if (self.doing is None) and self.tasks:
            current_task, args = [*self.tasks.pop(0).items()][0]
            getattr(self, current_task)(*args)
            if current_task in ['go', 'do_something']:
                pass
            else:
                self.doing = None

        if self.doing == 'go':
            if self.path:
                self.move_across_path()
            else:
                print(f'{self.name}: No path')
                ERRORS.loc[len(ERRORS)] = [f'{self.name} No path', 'continue method']
                self.doing = None

        elif self.doing:
            self.timer -= 1
            if self.timer <= 0:
                if self.moving_pause:
                    self.icon = self.icon_main
                    self.moving_pause = False
                    self.doing = 'go'
                else:
                    self.doing = None
                    self.icon = self.icon_main
            else:
                 self.set_icon_timer()


    def find_nearest_vertex(self):
        tree = KDTree(ALL_XY)
        dist, ind = tree.query([[self.x, self.y]])
        x = self.ALL_XY[ind[0,0]][0]
        y = self.ALL_XY[ind[0,0]][1]
        return self.df_XY[x][y], dist[0,0]
            

    def __repr__(self):
        return self.name

    
    
with open('/warehouse/empty_canvas.np', 'rb') as f:
    empty_canvas = joblib.load(f)
    
def render(agents=[], text=None, return_img=False):
    canvas = empty_canvas.copy()
    for agent in agents:
        agent_shape = agent.icon.shape
        x, y = int(agent.x * PIXELS_IN_METER), int(agent.y * PIXELS_IN_METER)
        x = max(agent_shape[1]//2, x)
        y = max(agent_shape[0]//2, y)
        canvas[y - agent_shape[0]//2 : y + agent_shape[0]//2, x - agent_shape[1]//2 : x + agent_shape[1]//2] = agent.icon
    if text:
        canvas = cv2.putText(canvas, text, (140*P , 6*P), cv2.FONT_HERSHEY_DUPLEX, 1, [50,50,50],2,)
    if return_img:
        return canvas
    cv2_imshow(canvas)
