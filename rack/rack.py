import numpy as np
    
class Product():
    def __init__(self, 	article, sell_by_date=None, vertex_index=None, place=None):
        self.article = article              
        self.sell_by_date = sell_by_date
        self.vertex_index = vertex_index

    def __repr__(self):
        return str(self.article)
      
      
class Pallet():
    '''
    products -      список товаров на паллете
    rack -          ссылка на стеллаж (class Rack)
    tier -          номер яруса (0-4)
    x, y -          абсолютные координаты палеты (координаты стеллажа + относительные координаты)
    DF_PROD -       таблица со списком всех товаров

    '''
    def __init__(self, 	products=[], rack=None, tier=None, DF_PROD=None):
        self.products = products              
        self.rack = rack                  
        self.tier = tier
        self.DF_PROD = DF_PROD

        if rack and tier:
            self.on_rack = True
            self.x = rack.x
            self.y = rack.y 
        else:
            self.on_rack = False

            
    def putting_to_rack(self, rack, tier):
            self.on_rack = True
            self.rack = rack
            self.tier = tier
            self.x = rack.x
            self.y = rack.y
            for prod in self.products:
                i = prod.index
                r = rack.r
                c = rack.c
                vertex = f'{r}-{c}' 
                self.DF_PROD.loc[i] = [prod, vertex, (tier), prod.sell_by_date]

                
    def getting_from_rack(self, agent=None):
            vertex_index = f'{self.rack.r}-{self.rack.c}'
            self.on_rack = False
            self.rack = None
            self.tier = None
            self.x = None
            self.y = None
            self.agent = agent

            for prod in self.products:
                i = prod.index
                self.DF_PROD.loc[i].Vertex = f'Оn going {agent}' 

                
    def __repr__(self):
        return f'[Pallet at ({self.tier})]'
      
      
      
class Rack():
    '''
    Класс стеллажа
    x, y -       координаты стеллажа в метрах
    r, c -       ряд и колонна по длине и ширине склада (индексы стеллажа)
    odevity -    чётность (для ориентировки, с какой стороны подъезжать)
    pallets -    список паллет на стеллаже
    put_pallet - положить паллету на стеллаж
    get_pallet - забрать паллету со стеллажа

    '''
    def __init__(self, x, y, r=None, c=None, od=None):
        self.x = x
        self.y = y
        self.r = r                          # избыточно?
        self.c = c                          # (по [r, c] можно получить индекс соответствующей вершины графа)
        self.pallets = np.full((5,), fill_value=None)


    def put_pallet(self, pallet, tier):                     # type(pallete) == __main__.Pallet
        assert tier in [0,1,2,3,4], 'wrong tier number'
        assert not(self.pallets[tier]), 'the place is occupied'
        assert not(pallet.on_rack), 'pallet, you try to put, is already on rack'
        pallet.putting_to_rack(self, tier)
        self.pallets[tier] = pallet


    def get_pallet(self, tier, agent=None):
        assert self.pallets[tier], 'no pallet'
        pallet = self.pallets[tier]
        pallet.getting_from_rack(agent=agent)
        self.pallets[tier] = None
        return pallet


    def __repr__(self):
        return f'Rack {self.r}-{self.c}'
      
      
      
      
class Temp_rack():
    def __init__(self, x, y, n):
        self.num = n
        self.pallet = None

    def put_pallet(self, pallet):
        if self.pallet:
            print(f'{self} already has {self.pallet}')
            ERRORS.loc[len(ERRORS)] = [f'{self} already has {self.pallet}', '']
        else:
            self.pallet = pallet

    def get_pallet(self):
        if self.pallet:
            pallet = self.pallet
            pallet.getting_from_rack()
            self.pallet = None
            return pallet
        else:
            print(f'{self} has no pallet')
            ERRORS.loc[len(ERRORS)] = [f'{self} has no pallet', '']

    def __repr__(self):
        return f'Tamp Rack {self.column}-{self.num}'
