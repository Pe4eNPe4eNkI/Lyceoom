from parameters import *

# тут создается карта и всё связанное с ней

map_x = [
    '111111111111',
    '1..........1',
    '1....1111..1',
    '1..........1',
    '1..........1',
    '1..11......1',
    '1....11....1',
    '111111111111'
]
# координаты стен
mini_map = set()
txt_map = set()
for j, row in enumerate(map_x):
    for i, char in enumerate(row):
        if char == '1':
            txt_map.add((i * CELL, j * CELL))
            txt_map.add((i * MAP_CELL, j * CELL))
