from parameters import *

# тут создается карта и всё связанное с ней

map_x = [
    '111111111111',
    '1..........1',
    '1......22..1',
    '1.......2..1',
    '1..3.......1',
    '1..3.......1',
    '1......33..1',
    '111111111111'
]
# координаты стен
mini_map = set()
txt_map = {}
for j, row in enumerate(map_x):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_CELL, j * MAP_CELL))
            if char == '1':
                txt_map[(i * CELL, j * CELL)] = '1'
            elif char == '2':
                txt_map[(i * CELL, j * CELL)] = '2'
            elif char == '3':
                txt_map[(i * CELL, j * CELL)] = '3'
