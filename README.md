# warehouse
Formalization of warehouse operation processes

[![Watch the video](https://img.youtube.com/vi/xYA5SwbZzCA/maxresdefault.jpg)](https://www.youtube.com/watch?v=xYA5SwbZzCA)


Данная работа выполнялась в рамках задачи оптимизации работы склада НМЖК (Нижегородский масло-жировой комбинат)

![Склад](https://user-images.githubusercontent.com/104506812/218085790-77c8fd75-94a0-4fb6-a405-27d1084ba9e7.jpg)

Для оценки выбранной стратегии (количество грузчиков, штабелёров в смене, порядок распределения задач, график приезда фур, зоны отгрузки, учёт срока годности и т.д.) предполагалось использование генетических алгоритмов.

Данная работа представляет собой инструмент, позволяющий сконструировать среду (environment) эмулирующую процессы отгрузки и приёмки товара на складе, а также ввести систему оценки эффективности этих процессов (простейший пример приведён в *logistics example.py*)

Навигация по складу осуществляется с помощью взвешенного ненаправленного графа (*graph.py*), вершины (vertices) которого расположены в необходиых ключевых точках (координаты стеллажей, проходов, зон погрузки и др.). Список вершин храниться в *GRAPH.vertex_dict*. Для загрузки объекта графа (*graph.gr*) используется библиотека joblib.

Агенты среды (грузчики штабелёры и т.д.) создаются как экземпляры класса Moving_agent (*agents.py*). Агенты имеют 4 базовых метода:
- *take_pallet* - взять паллету
- *give_pallet* - отдать паллету
- *go* - поехать в точку назначения
- *do_something* - включение таймера (метод позволяющий формализовать процессы, не требующие подробной эмуляции механики, а лишь учитывающий время выполнения)
Также агенту может быть задана последовательность действий с помощью метода *add_task*.
