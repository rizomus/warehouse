import numpy as np

X = np.array([0, 6, 18,  24,  30,  42,  48,  54,  66,  78,  90,  96, 108, 114, 126, 132]) + 1       # верхний левый угол
Y = np.hstack([np.arange(0.750, 99, 4.5), np.arange(4, 99, 4.5)])
Y.sort()

column_names = [str(i) for i in range(X[-1]//6 + 1)]
C = (X - 1) // 6                                                # Индексация каждого стеллажа = ряд + колонна (например "F-12")
rack_column_names = [str(C[i]) for i in range(len(C))]
row_names = [chr(i) for i in range(ord('A'), ord('W')+1)]

rack_coordinates = [list(zip(X , [[y]*len(X) for y in Y][i])) for i in range(len(Y))]  # ПЕРЕПИСАТЬ ПРОЩЕ!!!
rack_coordinates = np.array(rack_coordinates).reshape(44*16, 2)



Xt = np.array([12, 36, 60, 84, 102, 120]) + 1                # координаты стеллажей для временного хранения
Xt = [(x + 1.8, x + 3) for x in Xt]
Xt = np.array(Xt).flatten()
Yt = [3.75 + i * 0.8 for i in range(15)] + [100 - 3.75 - 1 - i * 0.8 for i in range(15)]
Yt.sort()

temp_rack_coordinates = [list(zip(Xt , [[y]*len(Xt) for y in Yt][i])) for i in range(len(Yt))]
temp_rack_coordinates = np.array(temp_rack_coordinates).reshape(30*12, 2)