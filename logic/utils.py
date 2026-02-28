import json
from enum import Enum, auto

class Move(str, Enum):
    ATT_L = "ATT_L"
    ATT_R = "ATT_R"
    DEF_L = "DEF_L"
    DEF_R = "DEF_R"
    COU_L = "COU_L"
    COU_R = "COU_R"

moves = [move.value for move in Move]
def get_action_matrix():
    with open('data.json', 'r') as file:
        data = json.load(file)
    ans = {(i,j):None for i in moves for j in moves}
    for i in moves:
        for j in moves[moves.index(i):]:
            result = data[i][j]
            # TODO
            pass

