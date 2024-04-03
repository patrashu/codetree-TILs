"""
1. 공격자 선정 (가장 약한 포탑이 공격자로 선정)
- 공격력이 가장 낮은 포탑 x
- 여러개면 가장 최근에 공격한 포탑 x
- 여러개면 행과 열의 합이 가장 큰 포탑 x
- 여러개면 열이 가장 큰 포탑 x
=> N+M만큼 공격력 상승

2. 공격자의 공격 (자신 제외 가장 강한 포탑을 공격)
- 공격력이 가장 높은 포탑 x
- 여러개면 공격한지 가장 오래된 포탑 x
- 여러개면 행과 열의 합이 가장 작은 포탑 x
- 여러개면 열이 가장 작은 포탑 x

레이저 공격 시도 후 포탄 공격
(1). 레이저 공격
- 상하좌우 4방향 이동 가능
- 부서진 포탑 자리는 지나갈 수 없음
- 가장자리에서 막힌 방향으로 이동하면 반대편으로 이동
- 최단 경로로 공격하는데, 경로가 있으면 레이저 공격 / 없으면 포탄 공격
- 경로가 여러개면 우하좌상 순서대로 먼저 움직인 경로 선택
- 공격 대상은 공격자의 공격력만큼 피해, 경로는 공격력 // 2 만큼 피해

(2). 포탄 공격
- 공격 대상은 공격자의 공격력만큼 피해
- 추가적으로 8방향 주위 포탑도 피해 입힘 => 공격자의 공격력 //2 만큼 피해
- 공격자는 공격을 받지 않음.
- 좌표 넘어가면 반대편으로

3. 포탑 부서짐
- 공격력 0이하 포탑은 부서짐

4. 포탑 정비
- 부서지지 않은 포탑 중 공격과 무관했던 포탑의 공격력이 1씩 올라감
- 공격자 / 피해자 둘 다 아닌 포탑에 해당

전체과정 종료 후 남아있는 포탑 중 가장 강한 포탑의 공격력 출력
N, M => 4~10까지
K => Turn => 1~1000까지
공격력 => 5000이하 
"""
from copy import deepcopy
from collections import deque, defaultdict

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
direc = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
attack_time = defaultdict(int)
alive = set()
for i in range(N):
    for j in range(M):
        attack_time[(i, j)] = 0
        if arr[i][j]:
            alive.add((i, j))

for time in range(K):
    if len(alive) == 1: # 공격자만 살아있는 경우
        break
    
    # step1: find attacker / receiver
    candits = []
    for x, y in alive:
        candits.append((arr[x][y], time-attack_time[(x, y)], x+y, y, x))

    _, _, _, ay, ax = sorted(candits, key=lambda x: (x[0], x[1], -x[2], -x[3]))[0]
    _, _, _, ry, rx = sorted(candits, key=lambda x: (-x[0], -x[1], x[2], x[3]))[0]
    attack_time[(ax, ay)] = time+1
    arr[ax][ay] += (N+M)

    # step2: find min direction
    # if -> lazer / if not -> bomb
    dq = deque([(ax, ay, [(ax, ay)])]) # x, y, direction
    visited = [[False]*M for _ in range(N)]
    visited[ax][ay] = True
    min_direc = None

    while dq:
        cx, cy, direction = dq.popleft()
        if (cx, cy) == (rx, ry):
            min_direc = direction
            break

        for i in range(0, 8, 2):
            dx, dy = direc[i]
            nx, ny = (cx+dx)%N, (cy+dy)%M
            if arr[nx][ny] == 0 or visited[nx][ny]: # 0이거나 방문했으면(최소가 아님)
                continue
            visited[nx][ny] = True
            dq.append((nx, ny, direction+[(nx, ny)]))
    
    # bomb
    if min_direc is None:
        min_direc = [(ax, ay), (rx, ry)]
        for dx, dy in direc:
            nx, ny = (rx+dx)%N, (ry+dy)%M
            if arr[nx][ny] == 0:
                continue
            min_direc.append((nx, ny))

    copy_alive = deepcopy(alive)
    # attack and healing
    for x, y in alive:
        if (x, y) in min_direc:
            if (x, y) == (ax, ay):
                continue
            elif (x, y) == (rx, ry):
                arr[x][y] -= arr[ax][ay]
            else:
                arr[x][y] -= (arr[ax][ay]//2)
            if arr[x][y] <= 0:
                arr[x][y] = 0
                copy_alive.discard((x, y))
        else:
            arr[x][y] += 1
    
    alive = copy_alive

max_value = 0
for row in arr:
    max_value = max(max(row), max_value)

print(max_value)