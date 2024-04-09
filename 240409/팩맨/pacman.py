"""
4x4 격자에 m개의 몬스터와 1개의 팩맨이 주어짐
각 몬스터는 8방향 중 하나를 가짐
팩맨은 턴단위로 진행되며, 한턴은 아래와 같음

(1). 몬스터 복제 시도 
- 현재 위치에서 자신과 같은 방향을 가진 몬스터를 복제하려함 x
- 복제된 몬스터는 부화하지 않아서 움직이지 못함 x
- 이전 state 상태 그대로 복사 (copy?) x

(2). 몬스터 이동 
- 각 몬스터가 자신이 향하는 방향으로 이동 x
- 칸에 시체가 있거나, 팩만이 있거나, 격자를 벗어나는 경우 반시계로 45도 회전 x
- 8방향 중 갈 곳이 있다면 즉시 이동, 없다면 stop x

(3). 팩맨 이동
- 맨해튼 거리로 3칸 이동함. 
- 가장 몬스터를 많이 잡아먹는 경로로 이동 
- 상/좌/하/우 우선순위 적용 => sort해서 이동 
- 경로에 있는 모든 몬스터를 먹어 치우고, 몬스터 시체를 남긴다. 
- 움직이기 전 같은 칸에 있는 몬스터나, 알은 먹지 않는다. 

(4). 몬스터 시체 소멸
- 시체는 2턴동안 유지 됨.

(5). 몬스터 복제 완성
- 복제했던 몬스터가 복사됨.

"""
from copy import deepcopy
from collections import deque, defaultdict





if __name__ == '__main__':
    M, T = map(int, input().split())
    px, py = map(int, input().split())
    px, py = px-1, py-1
    direc = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    monster = defaultdict(list)
    death = [[0]*4 for _ in range(4)]

    for _ in range(M):
        a, b, c = map(int,  input().split())
        monster[(a-1, b-1)].append(c-1)

    for _ in range(T):
        # copy
        copy_monster = deepcopy(monster)

        # monster move
        next_monster = defaultdict(list)
        for (cx, cy), values in monster.items():
            for cd in values:
                nx, ny, nd, flag = None, None, None, False
                for i in range(8):
                    nd = (cd+i)%8
                    dx, dy = direc[nd]
                    nx, ny = cx+dx, cy+dy
                    if nx < 0 or nx >= 4 or ny < 0 or ny >= 4 or death[nx][ny] or (px, py) == (nx, ny):
                        continue
                    flag = True
                    break
                if flag:
                    next_monster[(nx, ny)].append(nd)
                else:
                    next_monster[(cx, cy)].append(cd)

        # packman move
        max_cnt, max_move = -1, []
        dq = deque([(px, py, 0, 0, [])]) # cx, cy, cnt, depth, move
        
        while dq:
            cx, cy, cnt, depth, move = dq.popleft()
            if depth == 3:
                if max_cnt < cnt:
                    max_cnt, max_move = cnt, move
                continue
            
            for i in range(0, 8, 2):
                nx, ny = cx+direc[i][0], cy+direc[i][1]
                if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
                    continue
                if (nx, ny) not in move:
                    dq.append((nx, ny, cnt+len(next_monster[(nx, ny)]), depth+1, move+[(nx, ny)]))
                else:
                    dq.append((nx, ny, cnt, depth+1, move+[(nx, ny)]))

        # eat
        for nx, ny in max_move:
            px, py = nx, ny
            if next_monster[(px, py)]:
                death[px][py] = 3
                next_monster[(px, py)] = []

        # death - 1
        for i in range(4):
            for j in range(4):
                if death[i][j] == 0:
                    continue
                death[i][j] -= 1

        # paste
        for key, values in copy_monster.items():
            next_monster[key].extend(values)
        monster = next_monster

    res = 0
    for k, v in monster.items():
        res += len(v)
    print(res)