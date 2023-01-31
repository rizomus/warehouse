import numpy as np
import cv2
from google.colab.patches import cv2_imshow
PIXELS_IN_METER = P = 10

def square(x1, y1, x2, y2, canvas, color=(0,0,0), thickness=3, P=P):
    x1 = round(x1 * P)
    x2 = round(x2 * P)
    y1 = round(y1 * P)
    y2 = round(y2 * P)
    canvas = cv2.rectangle(canvas, (x1,y1), (x2,y2), color, thickness)
    return canvas

def circle(x, y, r, canvas, color=(0,0,0), thickness=2, P=P):
    x = round(x * P)
    y = round(y * P)
    r = round(r)
    canvas = cv2.circle(canvas, (x, y), r, color, thickness)
    return canvas

def add_vertex_and_edge(name, x, y, p, offset_p, row_len, graph, left_pass=False, right_pass=False):
    global canvas
    vertex = Vertex(name, x, y)
    graph.add_vertex(vertex)
    canvas = circle(x, y, 1, canvas, (255,0,0), 1)

    if (p-offset_p != 0) and (p != 93):                         
        u = name                        # соединяет ребром текущую вершину и предыдущую
        v = name[:2] + str(p-1)
        weight = 1
        graph.add_edge_by_indice(u, v, weight)
        
canvas = np.ones((72*P, 182*P, 3)).astype('int8') * 255
canvas = cv2.rectangle(canvas, (0,0), (182*P,72*P), (0,0,0), 3)
graph = Graph({})

for x1, y1, x2, y2 in [(0, 0, 38, 12), (38, 0, 61, 12), (61, 0, 97, 12), (97, 0, 134, 12), (134, 12, 170, 24), (170, 12, 182, 24), (134, 24, 182, 72), (97, 0, 134, 72)]:
    canvas = square(x1, y1, x2, y2, canvas=canvas)
passes_x = [8,18,28,70,80,90,106,116,126]
for x in passes_x:
    canvas = cv2.line(canvas, (x*P, 12*P), ((x+2)*P, 12*P), (255,255,255), 3)
canvas = cv2.line(canvas, (150*P, 24*P), (156*P, 24*P), (255,255,255), 3)
canvas = cv2.line(canvas, (134*P, 0*P), (182*P, 0*P), (255,255,255), 3)
canvas = cv2.line(canvas, (182*P, 0*P), (182*P, 12*P), (255,255,255), 3)
canvas = cv2.line(canvas, (97*P, 12*P), (97*P, 16*P), (255,255,255), 3)
canvas = cv2.line(canvas, (97*P, 69*P), (97*P, 72*P), (255,255,255), 3)
canvas = cv2.line(canvas, (134*P, 12*P), (134*P, 16*P), (255,255,255), 3)
canvas = cv2.line(canvas, (134*P, 68*P), (134*P, 72*P), (255,255,255), 3)
canvas = square(140, 66, 146, 72, canvas=canvas, thickness=3)
canvas = square(146, 66, 152, 72, canvas=canvas, thickness=3)
canvas = square(46, 66, 52, 72, canvas=canvas, thickness=3)
canvas = square(52, 66, 58, 72, canvas=canvas, thickness=3)
empty_canvas = canvas.copy()
cv2_imshow(canvas)

canvas = empty_canvas.copy()
graph = Graph({})
alfa = [chr(ord('a')+i) for i in range(20)]

x1, y1 = 134, 24 + 4    
row_len = 16                        # Зона А слева
for p in range(row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas, thickness=1)
    name = f'{alfa[0]}-{p}'
    x = x1 + 0.5
    y = y1 - 1
    add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y - 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 2                                  #
    graph.add_edge_by_indice(u, v, weight)      # наверх к проходу
    
    canvas = square(x1, y1+2.8, x2, y1 + 2.8 + 1, canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 2.8 + 2
    name = f'{alfa[1]}-{p}'
    add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)

    x1 = x2


y1 = 39 - 3.4
for row in range(1,6+1):   
    x1 = 134
    for p in range(row_len):
        x2 = x1 + 1
        canvas = square(x1, y1, x2, y1 + 1.2, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 - 1
        name = f'{alfa[row*2]}-{p}'
        add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)
       
        canvas = square(x1, y1 + 1.2, x2, y1 + 2.4, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 + 2.4 + 1
        name = f'{alfa[row*2+1]}-{p}'
        add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)
        if row == 6:
            for i in range(2):
                pass_name = name[0] + '*'*(i+1) + '-' + str(p)         
                pass_y = y + 1.5 + 2 * i
                vertex = Vertex(pass_name, x, pass_y)
                canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
                graph.add_vertex(vertex)
                u = name                                    #                               
                v = pass_name              #
                weight = 2                                  #
                graph.add_edge_by_indice(u, v, weight)      # вниз к проходу            
        x1 = x2
    y1 += 4.4


row_len = 26 + 16

x1, y1 = 156, 24 + 4                            # Зона А справа
for p in range(16, row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1
    name = f'{alfa[0]}-{p}'
    add_vertex_and_edge(name, x, y, p, 16, row_len, graph, left_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y - 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 2                                  #
    graph.add_edge_by_indice(u, v, weight)      # наверх к проходу

    canvas = square(x1, y1 + 2.8, x2, y1 + 2.8 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 2.8 + 2
    name = f'{alfa[1]}-{p}'
    add_vertex_and_edge(name, x, y, p, 16, row_len, graph, left_pass=True)
    x1 = x2

y1 = 39 - 3.4
for row in range(1,8+1):    
    x1 = 156
    for p in range(16, row_len):
        x2 = x1 + 1
        canvas = square(x1, y1, x2, y1 + 1.2, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 - 1
        name = f'{alfa[row*2]}-{p}'
        add_vertex_and_edge(name, x, y, p, 16, row_len, graph, left_pass=True)

        canvas = square(x1, y1 + 1.2, x2, y1 + 2.4, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 + 2.4 + 1
        name = f'{alfa[row*2+1]}-{p}'
        add_vertex_and_edge(name, x, y, p, 16, row_len, graph, left_pass=True)
        x1 = x2
    y1 += 4.4

x1, y1 = 156, 71
for p in range(16, row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1.2
    name = f's-{p}'
    add_vertex_and_edge(name, x, y, p, 16, row_len, graph, left_pass=True)
    x1 = x2


alfa = [chr(ord('A')+i) for i in range(24)]
row_len = 41
# canvas = empty_canvas.copy()

x1, y1 = 0, 12 + 4                            # Зона Б слева
for p in range(row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1
    name = f'A-{p}'
    add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y - 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 1.5                                  #
    graph.add_edge_by_indice(u, v, weight)      # наверх к проходу

    canvas = square(x1, y1 + 2.8, x2, y1 + 2.8 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 2.8 + 2
    name = f'B-{p}'
    add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y + 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 1.5                                  #
    graph.add_edge_by_indice(u, v, weight)      # вниз к проходу
    x1 = x2


y1 = 24 + 3 - 3.2
x1 = 0
for p in range(row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 1 + 1.2
    name = f'C-{p}'
    add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)
    x1 = x2

y1 = 24 + 3
for row in range(2,10+2):    
    x1 = 0
    for p in range(row_len):
        if row > 9 and p > 34:
            continue

        x2 = x1 + 1
        canvas = square(x1, y1, x2, y1 + 1.2, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 - 1
        name = f'{alfa[row*2 - 1]}-{p}'
        add_vertex_and_edge(name, x, y, p, 0, row_len, graph, right_pass=True)

        if not(row+1 > 9 and p > 34):
            canvas = square(x1, y1 + 1.2, x2, y1 + 2.4, canvas=canvas, thickness=1)
            x = x1 + 0.5
            y = y1 + 2.4 + 1
            name = f'{alfa[row*2]}-{p}'
            add_vertex_and_edge(name, x, y, p, 0, row_len-6, graph, right_pass=True)
        x1 = x2
    y1 += 4.4


x1, y1 = 0, 71
for p in range(row_len-6):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1
    name = f'X-{p}'
    add_vertex_and_edge(name, x, y, p, 0, row_len-6, graph, right_pass=True)
    x1 = x2


row_len = 41+52+33
offset = 41
x1, y1 = 97 - 52, 12 + 4                            # Зона Б справа
for p in range(41, row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1
    name = f'A-{p}'
    add_vertex_and_edge(name, x, y, p, offset, row_len, graph, left_pass=True, right_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y - 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 1.5                                  #
    graph.add_edge_by_indice(u, v, weight)      # наверх к проходу

    canvas = square(x1, y1 + 2.8, x2, y1 + 2.8 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 2.8 + 2
    name = f'B-{p}'
    add_vertex_and_edge(name, x, y, p, offset, row_len, graph, left_pass=True, right_pass=True)

    pass_name = name[0] + '*-' + str(p) 
    pass_y = y + 1.5
    vertex = Vertex(pass_name, x, pass_y)
    canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
    graph.add_vertex(vertex)
    u = name                                    #                               
    v = pass_name              #
    weight = 1.5                                  #
    graph.add_edge_by_indice(u, v, weight)      # вниз к проходу
    x1 = x2


y1 = 24 + 3 - 3.2
x1 = 97 - 52
for p in range(41, row_len):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 + 1 + 1.2
    name = f'C-{p}'
    add_vertex_and_edge(name, x, y, p, offset, row_len, graph, right_pass=True)
    x1 = x2


y1 = 24 + 3
for row in range(2,10+2):    
    x1 = 97 - 52
    for p in range(41, row_len):
        if row > 8 and p < 41 + 20:
            offset = 41 + 20
            x1 = x1 + 1
            continue

        x2 = x1 + 1
        canvas = square(x1, y1, x2, y1 + 1.2, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 - 1
        name = f'{alfa[row*2 - 1]}-{p}'
        add_vertex_and_edge(name, x, y, p, offset, row_len, graph, left_pass=True, right_pass=True)
       
        canvas = square(x1, y1 + 1.2, x2, y1 + 2.4, canvas=canvas, thickness=1)
        x = x1 + 0.5
        y = y1 + 2.4 + 1
        name = f'{alfa[row*2]}-{p}'
        add_vertex_and_edge(name, x, y, p, offset, row_len, graph, left_pass=True, right_pass=True)

        if row==8 and p < 41+20:
            pass_name = name[0] + '*-' + str(p)         
            pass_y = y + 1.5
            vertex = Vertex(pass_name, x, pass_y)
            canvas = circle(x, pass_y, 1, canvas, (0,0,255), 1)
            graph.add_vertex(vertex)
            u = name                                    #                               
            v = pass_name              #
            weight = 2                                  #
            graph.add_edge_by_indice(u, v, weight)      # вниз к проходу  

        x1 = x2
    y1 += 4.4


x1, y1 = 97-52+20, 71
for p in range(41+20, 41+52+33):
    x2 = x1 + 1
    canvas = square(x1, y1, x2, y1 + 1, canvas=canvas, thickness=1)
    x = x1 + 0.5
    y = y1 - 1
    name = f'X-{p}'
    add_vertex_and_edge(name, x, y, p, offset, row_len, graph, left_pass=True, right_pass=True)
    x1 = x2

    
    
passes_x = [8,18,28,70,80,90,106,116,126]
for x in passes_x:
    pass_name = f'pass-{x+1}'
    vertex = Vertex(pass_name, x+1, 12)
    graph.add_vertex(vertex)
    canvas = circle(x+1, 12, 1, canvas, (0,0,255), 1)

    if x > 28:
        x -= 4
    u ='A*-'+str(x)
    v = pass_name
    weight = 2                                  # УТОЧНИТЬ 
    graph.add_edge_by_indice(u, v, weight)

    u = 'A*-'+str(x+1)
    v = pass_name
    weight = 2                                  # УТОЧНИТЬ 
    graph.add_edge_by_indice(u, v, weight)

points_x = np.arange(3,37,2)
for x in points_x:
    for y in [8, 10]:
        pass_name = f'take_over_A-{x, y}'
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)

points_x = np.arange(63,96,2)
for x in points_x:
    for y in [8, 10]:
        pass_name = f'take_over_B-{x, y}'
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)

points_x = np.arange(99,133,2)
for x in points_x:
    for y in [8, 10]:
        pass_name = f'take_over_C-{x, y}'
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)

points_x = np.arange(136,169,2)
for x in points_x:
    for y in [14, 18, 22]:
        pass_name = f'take_over_D-{x, y}'
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)
  
  
points_y = {25.5:'a*' ,27:'a', 32.7:'b', 34.6:'c', 39:'de', 43.4:'fg', 47.8:'hi', 52.2:'jk', 
            56.6:'lm', 61.1:'no', 62.5:'n*', 64.5:'n**'}
prev_names = {}
for y, alfa in points_y.items():
    point_names = {151:f'{alfa}>', 153:f'<{alfa}>', 155:f'<{alfa}'}
    for x in point_names:
        pass_name = point_names[x]
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)
    if prev_names:
        for u, v in zip(prev_names.values(), point_names.values()):
            weight = y - prev_y
            graph.add_edge_by_indice(u, v, weight)
    prev_names = point_names.copy()
    prev_y = y


prev_names = {}
points_y = {13.5:'A*', 15:'A', 20.8:'B', 22.3:'B*', 26:'CD', 30.4:'EF', 34.8:'GH', 39.2:'IJ', 43.6:'KL', 48:'MN', 52.4:'OP', 
            56.8:'QR', 61.2:'ST', 65.6:'UV', 70:'WX'}
for y, alfa in points_y.items():
    point_names = {42:f'{alfa}>', 44:f'<{alfa}', 131:f'{alfa}>>', 133:f'{alfa}>>>'}
    for x in point_names:
        pass_name = point_names[x]
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)
    if prev_names:
        for u, v in zip(prev_names.values(), point_names.values()):
            weight = y - prev_y
            graph.add_edge_by_indice(u, v, weight)
    prev_names = point_names.copy()
    prev_y = y


prev_names = {}
points_y = {61.2:'ST', 65.6:'UV', 70:'WX'}
for y, alfa in points_y.items():
  
  
 
prev_names = {}
points_y = {70:'area_0', 67:'area_1'}
for y, alfa in points_y.items():
    point_names = {136:f'{alfa}0', 138:f'{alfa}1'}
    for x in point_names:
        pass_name = point_names[x]
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)

prev_names = {}
points_y = {65.4:'pq', 69.8:'rs'}
for y, alfa in points_y.items():
    point_names = {155:f'<{alfa}', 153:f'<{alfa}>'}
    for x in point_names:
        pass_name = point_names[x]
        vertex = Vertex(pass_name, x, y)
        graph.add_vertex(vertex)
        canvas = circle(x, y, 1, canvas, (0,0,255), 1)
        
 

for i in range(1,16):
    u = 'a*-'+str(i-1)
    v = 'a*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)

for i in range(1,16):
    u = 'n*-'+str(i-1)
    v = 'n*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)

for i in range(1,16):
    u = 'n**-'+str(i)
    v = 'n**-'+str(i-1)
    graph.add_edge_by_indice(u, v, 1)

for i in range(16,42):
    u = 'a*-'+str(i-1)
    v = 'a*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)



for i in range(1,41):
    u = 'A*-'+str(i-1)
    v = 'A*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)

for i in range(41,126):
    u ='A*-'+str(i-1)
    v = 'A*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)

for i in range(42,61):
    u = 'Q*-'+str(i-1)
    v = 'Q*-'+str(i)
    graph.add_edge_by_indice(u, v, 1)
    
    
for litera in ['A', 'B', 'C']:
    A1 = []
    A2 = []
    for k in graph.vertex_dict.keys():
        if k[:11] == 'take_over_' + litera:
            if k[-2] == '8':
                A1.append(k)
            else:
                A2.append(k)
    print(A1)
    print(A2)
    print()

    u = A1[0]
    v = A2[0]
    graph.add_edge_by_indice(u, v, 2)
    for i in range(1, len(A1)):
        u = A1[i]
        v = A2[i]
        graph.add_edge_by_indice(u, v, 2)

        u = A1[i]
        v = A1[i-1]
        graph.add_edge_by_indice(u, v, 2)

        u = A2[i]
        v = A2[i-1]
        graph.add_edge_by_indice(u, v, 2)
        
        
A1 = []
A2 = []
A3 = []
for k in graph.vertex_dict.keys():
    if k[:11] == 'take_over_D':
        if k[-2] == '4':
            A1.append(k)
        elif k[-2] == '8':
            A2.append(k)
        else:
            A3.append(k)
print(A1)
print(A2)
print(A3)

for a1, a2 in [(A1, A2), (A2, A3)]:
    u = a1[0]
    v = a2[0]
    graph.add_edge_by_indice(u, v, 4)

for i in range(1, len(A1)):
    for a1, a2 in [(A1, A2), (A2, A3)]:
        u = a1[i]
        v = a2[i]
        graph.add_edge_by_indice(u, v, 4)

    for a in [A1, A2, A3]:
        u = a[i]
        v = a[i-1]
        graph.add_edge_by_indice(u, v, 2)
        
        
        
for i in ['9', '19', '29']:
    u = 'pass-'+i
    v = f'take_over_A-({i}, 10)'
    graph.add_edge_by_indice(u, v, 2)
for i in ['71', '81', '91']:
    u = 'pass-'+i
    v = f'take_over_B-({i}, 10)'
    graph.add_edge_by_indice(u, v, 2)
for i in ['107', '117', '127']:
    u = 'pass-'+i
    v = f'take_over_C-({i}, 10)'
    graph.add_edge_by_indice(u, v, 2)
for i in ['152', '154']:
    if i == '152':
        keys = ['a*>', '<a*>']
    else:
        keys = ['<a*>', '<a*']
    for k in keys:
        u = k
        v =f'take_over_D-({i}, 22)'
        graph.add_edge_by_indice(u, v, 5)
        
        
        
for key in ['a', 'b', 'c', 'de', 'fg', 'hi', 'jk', 'lm']:
    for k in key:
        u = k+'-15'
        v = key+'>'
        graph.add_edge_by_indice(u, v, 1.5)

    u = '<'+key+'>'
    v = key+'>'
    graph.add_edge_by_indice(u, v, 2)

    u = '<'+key+'>'
    v = '<'+key
    graph.add_edge_by_indice(u, v, 2)

    for k in key:
        u = k+'-16'
        v = '<'+key
        graph.add_edge_by_indice(u, v, 1.5)
        
        
        
for key in ['A', 'B','CD','EF', 'GH', 'IJ', 'KL', 'MN', 'OP']:
    for k in key:
        u = k +'-40'
        v = key + '>'
        graph.add_edge_by_indice(u, v, 1.5)

        u = key +'>'
        v = '<'+ key
        graph.add_edge_by_indice(u, v, 2)

        u = k +'-41'
        v = '<'+key
        graph.add_edge_by_indice(u, v, 1.5)
#----------------------------------------------------------------
        u = k +'-125'
        v = key + '>>'
        graph.add_edge_by_indice(u, v, 1.5)

        u = key +'>>'
        v = key + '>>>'
        graph.add_edge_by_indice(u, v, 2)

u = 'B*-40'
v = 'B*>'
graph.add_edge_by_indice(u, v, 1.5)

u = 'B*>'
v = '<B*'
graph.add_edge_by_indice(u, v, 2)

u = 'B*-41'
v = '<B*'
graph.add_edge_by_indice(u, v, 1.5)

u = 'B*-125'
v = 'B*>>'
graph.add_edge_by_indice(u, v, 1.5)

u ='B*>>'
v = 'B*>>>'
graph.add_edge_by_indice(u, v, 2)

key = 'QR'
for k in key:
    u = k +'-40'
    v = key + '>'
    graph.add_edge_by_indice(u, v, 1.5)

    u = key +'>'
    v = '<'+ key
    graph.add_edge_by_indice(u, v, 2)

u = 'Q-41'
v = '<QR'
graph.add_edge_by_indice(u, v, 1.5)
u = 'Q*-41'
v = '<QR'
graph.add_edge_by_indice(u, v, 2.1)


for key in ['ST', 'UV', 'WX']:
    for k in key:
        u = k +'-34'
        v = key + '->'
        graph.add_edge_by_indice(u, v, 3)

        u = key +'->'
        v = key + '>'
        graph.add_edge_by_indice(u, v, 4)

        u = key +'>'
        v = '<'+ key
        graph.add_edge_by_indice(u, v, 2)
#----------------------------------------------------------------
        u = k +'-125'
        v = key + '>>'
        graph.add_edge_by_indice(u, v, 1.5)

        u = key +'>>'
        v = key + '>>>'
        graph.add_edge_by_indice(u, v, 2)

        if key == "ST":
            u = '<'+ key
            v = '<-' + key
            graph.add_edge_by_indice(u, v, 16)

        u = '<-' + key
        v = k +'-61'
        graph.add_edge_by_indice(u, v, 5.5)

for i in ['54', '57']:
    u = '<-ST'
    v = 'Q*-' + i
    graph.add_edge_by_indice(u, v, 2.5)

u = '<ST'
v = 'Q*-41'
graph.add_edge_by_indice(u, v, 2)



for i in range(1,126):
    if not(i == 41 or i==93):
        u = 'B*-'+str(i)
        v = 'B*-'+str(i-1)
        weight = 1
        graph.add_edge_by_indice(u, v, weight)


graph.add_edge_by_indice('A-93', 'A-92', 1)
graph.add_edge_by_indice('X-93', 'X-92', 1)
graph.add_edge_by_indice('A*-125', 'A*>>', 1.5)
graph.add_edge_by_indice('A*>>', 'A*>>>', 2)
graph.add_edge_by_indice('WX>>>', 'area_00', 3)
graph.add_edge_by_indice('area_00', 'area_01', 2)
graph.add_edge_by_indice('area_10', 'area_11', 2)
graph.add_edge_by_indice('area_00', 'area_10', 3)
graph.add_edge_by_indice('area_01', 'area_11', 3)
graph.add_edge_by_indice('area_10', 'n**-1', 2)
graph.add_edge_by_indice('area_11', 'n**-4', 2)
graph.add_edge_by_indice('n-15', 'no>', 1.5)
graph.add_edge_by_indice('no>', '<no>', 2)
graph.add_edge_by_indice('<no>', '<no', 2)
graph.add_edge_by_indice('<no', 'n-16', 1.5)
graph.add_edge_by_indice('<pq>', '<pq', 2)
graph.add_edge_by_indice('<pq', 'p-16', 1.5)
graph.add_edge_by_indice('<pq', 'q-16', 1.5)
graph.add_edge_by_indice('<rs>', '<rs', 2)
graph.add_edge_by_indice('<rs', 'r-16', 1.5)
graph.add_edge_by_indice('<rs', 's-16', 1.5)
graph.add_edge_by_indice('<rs', '<pq', 4.4)
graph.add_edge_by_indice('<rs>', '<pq>', 4.4)
graph.add_edge_by_indice('<pq', '<n**', 0.5)
graph.add_edge_by_indice('<pq>', '<n**>', 0.5)
graph.add_edge_by_indice('<n**>', '<n**', 2)
graph.add_edge_by_indice('n**>', '<n**>', 2)
graph.add_edge_by_indice('n**-15', 'n**>', 1.5)
graph.add_edge_by_indice('A>>>', 'take_over_D-(136, 14)', 3)
graph.add_edge_by_indice('A*>>>', 'take_over_D-(136, 14)', 3)



for edges in graph.edge_dict.values():
    for e in edges:
        
        eu = graph.vertex_dict[e.u]
        ev = graph.vertex_dict[e.v]
        x1 = round(eu.x*PIXELS_IN_METER)
        x2 = round(ev.x*PIXELS_IN_METER)
        y1 = round(eu.y*PIXELS_IN_METER)
        y2 = round(ev.y*PIXELS_IN_METER)

        a = x1 - x2
        b = y1 - y2
        distanse = (a**2 + b**2)**0.5 / PIXELS_IN_METER
        if abs(distanse - e.weight) > 0.1:
            e.weight = distanse
            print("!!!")

        color = [0,255,0]
        canvas = cv2.line(canvas, [x1, y1], [x2, y2], color, 1,)

cv2_imshow(canvas)
