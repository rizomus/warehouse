'''
Модифицированный алгоритм Дейкстры.
Суть модификации: сохранить все минимальные пути равной длинны, 
а потом при построении маршрута выбирать тот вариант, который не изменяет направление движения
'''

def graph_search(g, start):         # сканирует граф 'g'

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
    
    # path_dict['start'] = [edge for edge in g.edge_dict[start]]
    return path_dict


  
def min_path(path_dict, start, end):        # ищет минимальный муть от start до end
    if len(path_dict) == 0:
        return []
    for edge in path_dict[end]:             # если между конечной и начальной точкой 1 ребро - это и есть весь путь (иначе будет key error)
        if edge.u == start:
            return [edge]
    path = []
    edge = path_dict[end][0]
    orientation = edge.orientation()
    path.append(edge)
    if len(path_dict[edge.u]) == 1:
        while edge.u != start:
            edge = path_dict[edge.u][0]
            path.append(edge)
    else:
        while edge.u != start:
            ed = None
            for e in path_dict[edge.u]:
                if e.orientation() != orientation:
                    pass
                else:
                    ed = e
                    break
            if ed is None:
                edge = path_dict[edge.u][0]
            else:
                edge = ed
            path.append(edge)
            orientation = edge.orientation()

    return list(reversed(path))

path_dict = graph_search(GRAPH, 'U-15(p-1)')
path = min_path(path_dict, 'U-15(p-1)', 'C-5(p-1)')
path_distances = [p.weight for p in path]
path_distances = np.cumsum(path_distances)
