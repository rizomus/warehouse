from rack import put_product_to_rack
from agents import Moving_agent, Truck
from graph import GRAPH
import numpy as np

# Создать необходимое количество агентов и грузовиков

icon = np.full((16, 16, 3), fill_value=(np.array([0, 0, 225], dtype='int16')))
agent_1 = Moving_agent('Petrovich', vertex_key='G-10', speed=SPEED, graph=GRAPH, icon=icon)

icon = np.full((16, 16, 3), fill_value=(np.array([255, 0, 0])), dtype='int16')
agent_2 = Moving_agent('Michalych', vertex_key='H-15', speed=SPEED, graph=GRAPH, icon=icon)

icon = np.full((16, 16, 3), fill_value=(np.array([0, 255, 0])), dtype='int16')
agent_3 = Moving_agent('Kovalsky', vertex_key='M-89', speed=SPEED, graph=GRAPH, icon=icon)

AGENTS = [agent_1, agent_2, agent_3]

truck_icon = cv2.imread('/warehouse/truck.jpg')
truck_icon = cv2.resize(truck_icon, (36, 20))
truck_vertex = 'some_vertex'     # Площадка погрузки, на которую прибывает гурзовик.
TRUCKS = [Truck('Truck', truck_vertex, speed=0, graph=GRAPH, icon=truck_icon) for _ in range(20)]

# Создать таблицы с продуктами и грузовиками.

cols = ['Article', 'Vertex', 'Tier', 'Sell by date']   # таблица, 
DF_PROD = pd.DataFrame(columns=cols) 

cols = ['Arrival time', 'Truck', 'Product list']   # таблица, 
DF_TRUCK = pd.DataFrame(columns=cols) 

for i in range(1000):
    vertex = 'rack_index'             # Уникальный индекс стеллажа, например: 'A-23'
    prod = 'Some_product'             # 'Milk'
    date = 'Sell_by_date'             # '01.01.23'
    tier = 1
    put_product_to_rack(prod, date, vertex, tier, DF_PROD, DF_RACK)
