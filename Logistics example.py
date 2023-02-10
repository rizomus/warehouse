'''
Упрощённый пример построения логистической цепочки работы склада

'''

from  warehouse.rack import put_product_to_rack
from  warehouse.agents import Moving_agent, Truck
from  warehouse.graph import GRAPH
import numpy as np
from IPython.display import clear_output
SECONDS_IN_FRAME = 1


# Создать необходимое количество агентов


icon = np.full((16, 16, 3), fill_value=(np.array([0, 0, 225], dtype='int16')))
agent_1 = Moving_agent('Petrovich', vertex_key='G-10', speed=SPEED, graph=GRAPH, icon=icon, sec_in_frame=SECONDS_IN_FRAME)

icon = np.full((16, 16, 3), fill_value=(np.array([255, 0, 0])), dtype='int16')
agent_2 = Moving_agent('Michalych', vertex_key='H-15', speed=SPEED, graph=GRAPH, icon=icon, sec_in_frame=SECONDS_IN_FRAME)

icon = np.full((16, 16, 3), fill_value=(np.array([0, 255, 0])), dtype='int16')
agent_3 = Moving_agent('Kovalsky', vertex_key='M-89', speed=SPEED, graph=GRAPH, icon=icon, sec_in_frame=SECONDS_IN_FRAME)

AGENTS = [agent_1, agent_2, agent_3]


# Создать таблицы с полным перечнем продукции на складе и списками продуктов подлежащих погрузке


cols = ['Article', 'Vertex', 'Tier', 'Sell by date']   # Полный перечень (на стеллажах)
DF_PROD = pd.DataFrame(columns=cols) 

cols = ['Arrival time', 'Truck', 'Product list']   # Подлежащие погрузке
DF_TRUCK = pd.DataFrame(columns=cols) 


#  Заполнить стеллажи продуктами


for i in range(1000):
    vertex = 'A-23'             # Уникальный индекс стеллажа (в соответствии с GRAPH.vertex_dict)
    prod = 'Some_product'             # 'Milk'
    date = 'Sell_by_date'             # '01.01.23'
    tier = 1
    put_product_to_rack(prod, date, vertex, tier, DF_PROD, DF_RACK)

    
# Заполнить таблицу с расписанием прибытия фур и списком продуктов подлежащих загрузке


n_trucks = 10

for i in range(n_trucks):
    time = 'hh.mm.ss'                   # время прибытия фуры
    indexes = None                      # индексы товаров, подлежащих загрузке
    products = DF_PROD.iloc[indexes]
    DF_TRUCK.loc[len(DF_TRUCK)] = [time, products]
    
    
# Основной цикл


reward = 0          # Награда (положительная за полную загрузку фуры, отрицательная за простой)
truck_n = 0         # Номер фуры по счёту
trucks = []         # Список всех прибывших фур, ожидающих загрузки

prod_list = pd.DataFrame(columns=['Article', 'Vertex', 'Tier', 'Sell by date', 'Target truck'])     # Очередь товаров подлежащих загрузке

text=''     # Информация для вывода на экран визуализации

for sec in range(0, 60*60*8, SECONDS_IN_FRAME):
    
    time = pd.to_datetime(sec, unit='s')

    if truck_n < len(DF_TRUCK) and time >= DF_TRUCK['Arrival time'][truck_n]:       # Если подошло время прибытия очередной фуры
        truck_vertex = 'Dray-A1'                                                    # Площадка погрузки (в соответствии с GRAPH.vertex_dict)
        truck = Truck('Truck', truck_vertex, speed=0, graph=GRAPH, icon=truck_icon)                                       # 
        truck.n = truck_n
        trucks.append(truck)                # Список фур ожидающих загрузки
        DF_TRUCK['Truck'][truck_n] = truck
        print('New truck arrived to ' + truck.vertex)
        products = DF_TRUCK['Product list'][truck_n].copy()                         # Список продуктов, подлежащих погрузке
        products['Target truck'] = [truck for _ in range(min(10, len(products)))]
        prod_list = pd.concat([prod_list, products], axis=0)                        # Список продуктов добавляется в общую очередь
        truck_n += 1
        render([*trucks, *AGENTS])

    for agent in AGENTS:
        if agent.busy() or agent.tasks:
            agent.continue_()
        else:                                                               # Если агент свободен
            if len(prod_list) != 0:                                         
                pallet_vertex = prod_list['Vertex'].iloc[0]                 # "Адрес" стеллажа с товаром (в соответствии с GRAPH.vertex_dict)
                target_truck = prod_list['Target truck'].iloc[0]            # Кому грузить
                tier = prod_list['Tier'].iloc[0]                            # Номер яруса стеллажа
                letter, num = pallet_vertex.split('-')
                num = int(num)
                rack = DF_RACK[letter][num]                                 # Объект сталлажа, хранящий паллету
                agent.add_task('go', pallet_vertex,)                                # Поехать к стеллажу
                agent.add_task('do_something', 60, 'taking pallet from rack')       # Среднее время снятия паллеты
                agent.add_task('take_pallet', rack, None, tier)                     # Паллета снята
                agent.add_task('go', target_truck.vertex,)                          # Поехать к фуре
                agent.add_task('do_something', 60, 'putting pallet to truck')       # Среднее время погрузки на фуру
                agent.add_task('give_pallet', target_truck,)                        # Погрузка завершена
                index_0 = prod_list.index[0]
                prod_list = prod_list.drop(index_0, axis=0)                         # Погруженный товар удаляется из списка
            else:                                                           # Если агент свободен, но нет задач - неэффективное использование рабочей силы
                reward -= 0.05                                              # начисляем отрицательную награду

    for truck in trucks:
        print(f'Truck {truck.n} loaded: {len(truck.pallets)/10*100:.0f}%, prod_list: {len(prod_list)}, reward: {reward:.0f}')
        if len(truck.pallets) == 10:            # Условие, при котором фура считается загруженной
            reward += 200
            trucks.remove(truck)        
        else:
            reward -= 0.1                       # Пока фура не загружена, начисляется отрицательная награда за простой

    text = f'Reward: {reward:.1f}'
    render([*trucks, *AGENTS], text=text)

    print()
    if len(ERRORS) != 0:
        print(ERRORS)
    print(sec // 3600,'h,', (sec - (sec//3600)*3600)//60, 'min')
    clear_output(wait=True)
