"""

(1). 공장 설립
N개의 벨트를 설치하고, M개의 물건을 준비
각 벨트에는 물건이 오름차순으로 쌓임

(2). 물건 모두 옮기기
a벨트 물건을 b벨트로 옮기고 b벨트에 있는 선물 개수 출력
이 때, sort 되어야 함

(3). 앞 물건만 교체하기
a벨트 물건 중 맨 앞 물건을 b벨트의 맨 앞 물건과 교체
둘 중 하나에 아무것도 없으면 옮기기만 함

(4). 물건 나누기
a벨트에 있는 선물 개수를 n이라 할 때, n//2만큼의 선물을 앞에서부터 b벨트로 옮김
옮기고 나서 b벨트 선물 개수를 출력

(5). 선물 정보 얻기
선물 번호 p_num이 주어질 때 해당 선물의 앞/뒤 선물 번호가 a/b일 때, a+2*b를 출력
없는 경우에는 a/b가 각각 -1

(6). 벨트 정보 얻기
벨트 번호 b_num이 주어질 때, 맨 앞 선물, 맨 뒤 선물, 선물 총 개수를 각각 a/b/c라 할 때
a+2*b+3*c를 출력, a/b가 없는 경우 각각 -1

N,M,Q <= 100000
Q = 명령의 수
N = 벨트 수
M = 박스 수
"""
from collections import deque, defaultdict

def start(line):
    belts = defaultdict(deque)
    idx_to_belt = {}
    for idx in range(line[1]):
        belts[line[2+idx]].append(idx+1)
        idx_to_belt[idx+1] = line[2+idx]
    return belts, idx_to_belt

def send_all_boxes(belts, idx_to_belt, line):
    send, recv = line
    length = len(belts[send])
    if length == 0:
        return len(belts[recv])

    all_boxes = deque()
    for idx in range(length):
        all_boxes.appendleft(belts[send].popleft())

    while all_boxes:
        tmp = all_boxes.popleft()
        idx_to_belt[tmp] = recv
        belts[recv].appendleft(tmp)   
    return len(belts[recv])

def convert_front_box(belts, idx_to_belt, line):
    send, recv = line
    p1, p2 = None, None
    try:
        p1 = belts[send].popleft()
    except:
        pass
    try:
        p2 = belts[recv].popleft()
    except:
        pass

    if p1 is not None and p2 is not None:
        idx_to_belt[p1], idx_to_belt[p2] = recv, send
        belts[send].appendleft(p2)
        belts[recv].appendleft(p1)
    elif p1 is None:
        idx_to_belt[p2] = send
        belts[send].appendleft(p2)
    elif p2 is None:
        idx_to_belt[p1] = recv
        belts[recv].appendleft(p1)
    else:
        pass
    return len(belts[recv])

def send_half_len_boxes(belts, idx_to_belt, line):
    send, recv = line
    length = len(belts[send])

    if length == 0:
        return len(belts[recv])

    half = deque()
    for idx in range(length//2):
        half.appendleft(belts[send].popleft())
    
    for tmp in half:
        idx_to_belt[tmp] = recv
        belts[recv].appendleft(tmp)

    return len(belts[recv])

def get_box_info(belts, bpid, line):
    a, b = -1, -1
    idx = belts[bpid].index(line[0])
    if idx-1 >= 0:
        a = belts[bpid][idx-1]
    if idx+1 < len(belts[bpid]):
        b = belts[bpid][idx+1]
    return a+2*b

def get_conveyor_info(belts, line):
    a, b, c = None, None, len(belts[line[0]])
    try:
        a = belts[line[0]][0]
    except:
        a = -1
    try:
        b = belts[line[0]][-1]
    except:
        b = -1
    return a+2*b+3*c

if __name__ == '__main__':
    belts, idx_to_belt = None, None
    for _ in range(int(input())):
        cmd, *line = map(int, input().split())
        if cmd == 100:
            belts, idx_to_belt = start(line)
        elif cmd == 200:
            print(send_all_boxes(belts, idx_to_belt, line))
        elif cmd == 300:
            print(convert_front_box(belts, idx_to_belt, line))
        elif cmd == 400:
            print(send_half_len_boxes(belts, idx_to_belt, line))
        elif cmd == 500:
            print(get_box_info(belts, idx_to_belt[line[0]], line))
        else:
            print(get_conveyor_info(belts, line))