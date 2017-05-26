from random import randint
from argparse import ArgumentParser

class Point:
    def __init__(self, x, y, connect):
        self.x = x
        self.y = y
        self.connect = connect
 
    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.connect)
 
    def __repr__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.connect)
 
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
 
    def __hash__(self):
        return self.x ** self.y
 
def bfs(s, t, graph):
    if s == t:
        return {}
    queue = [s]
    visits = {}
    for i in graph.keys():
        visits[i] = False
    visits[s] = True
    path = { s: -1 }
    while queue:
        v = queue[0]
        queue = queue[1:]
        for u in graph[v]:
            if (not u.connect or visits[u]):
                continue
            visits[u] = True
            queue.append(u)
            path[u] = v
            if u == t:
                return path
    return path
 
def get_path(path, s, t):
    arr = [t]
    if not t in path:
        return []
    while t != s:
        arr.append(path[t])
        t = path[t]
    return arr[::-1]
 
def delete_node(graph, v):
    for node in graph[v]:
        node.connect = False
 
def start(N, M):
    all_nodes = M*(N-2)
    delete_nodes = 0
    max_x, max_y = [N, M] #or [int(i) for i in input().split()]
    points = []
    for y in range(max_y):
        for x in range(max_x):
            points.append(Point(x, y, True))
 
    graph = {}
 
    for point in points:
        graph[point] = []
        if point.x > 0:
            graph[point].append(Point(point.x-1, point.y, True))
        if point.x < max_x - 1:
            graph[point].append(Point(point.x+1, point.y, True))
        if point.y > 0:
            graph[point].append(Point(point.x, point.y-1, True))
        if point.y < max_y - 1:
            graph[point].append(Point(point.x, point.y+1, True))
 
 
    p = bfs(Point(0, 0, True), Point(max_x - 1, 0, True), graph)
    path = get_path(p, Point(0, 0, True), Point(max_x - 1, 0, True))
    while p:
        del_node = Point(randint(1, max_x - 2), randint(0, max_y - 1), True)
        check_connectivity = False
        for i in graph[del_node]:
            if i.connect:
                check_connectivity = True
                break
        if check_connectivity:
            delete_nodes += 1
            delete_node(graph, del_node)
            if del_node in path:
                p = bfs(Point(0, 0, True), Point(max_x - 1, 0, True), graph)
                path = get_path(p, Point(0, 0, True), Point(max_x - 1, 0, True))
            if not path:
                return delete_nodes/all_nodes

def argument_parser():
    '''работа с аргументами'''
    arg_parse = ArgumentParser(description=('''
        Дана матрица MxN, из неё строится граф G=(V, E), |V| = MxN, вершина (i, j)
        соединена с вершиной (i-1, j), (i+1, j), (i, j-1), (i, j+1), если эти вершины есть в графе.
        Строится путь от вершины (0, 0) до (N-1, 0). Затем случайным образом удаляется вершина (i, j),
        у которой i != 0 и i != N-1. Если текущий путь не включал эту вершину, то случайным образом удаляется
        еще одна вершина и т.д. Если же путь включал эту вершину, ищется новый путь от (0, 0) до (N-1, 0).
        Требуется посчитать сколько вершин надо удалить, для того чтобы путь перестал существовать.
        Таких экспериментов проводится несколько, затем считается среднее.
        '''))
    arg_parse.add_argument('--count_experiments', '-c', type=int, help=('количество экспериментов'), default=1000)
    arg_parse.add_argument('--height', '-M', type=int, help=('высота сетки'), default=20)
    arg_parse.add_argument('--width', '-N', type=int, help=('ширина сетки'), default=20)
    return arg_parse.parse_args()

if __name__ == '__main__':
    from time import time
    import sys
    args = argument_parser()
    N = args.width
    M = args.height
    count_experiments = args.count_experiments
    if N < 3:
        print('Ширина должна быть больше или равна 3')
        sys.exit()
    if M < 1:
        print('Высота должна быть больше или равна 1')
        sys.exit()
    if count_experiments < 1:
        print('Количество экспериментов должно быть больше или равно 1')
        sys.exit()
    start_time = time()
    sum_ = 0
    for i in range(count_experiments):
        sum_ += start(N, M)
    print('Доля удаленных вершин: ', sum_/count_experiments)
    print('Время: ', time() - start_time, 'сек')