"""
m명의 사람이 빵을 구하고 싶음
1번은 1분에, 2번은 2분에, m번은 m분에 각 base에서 출발해서 편의점으로 이동

(1). 이동
- 격자에 있는 사람들 모두가 (time <= M) 가고 싶은 편의점을 향해 1칸 움직임 (최단거리로)
- 편의점에 도착하면 멈추고, 다른 사람들이 해당 칸을 지나갈 수 없게 됨 (벽 처리, 동시에 진행)
- 현재가 t분이고 t<=m을 만족하면, t번 사람은 편의점과 가장 가까운 basecamp로 이동함
- 베이스 캠프가 여러개면 행/열이 작은 순서대로, 시간이 소요되지 않음
"""
from collections import deque

def move(arr, candit, basecamps, direc):
    cx, cy, ct = candit
    ex, ey = basecamps[ct]
    dq = deque([(cx, cy, [(cx, cy)])])
    visited = [[False]*N for _ in range(N)]
    visited[cx][cy] = True

    ways = None
    while dq:
        cx, cy, way = dq.popleft()
        if (cx, cy) == (ex, ey):
            ways = way
            break
        for k in range(4):
            nx, ny = cx+direc[k][0], cy+direc[k][1]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] == -1:
                continue
            if not visited[nx][ny]:
                visited[nx][ny] = True
                dq.append((nx, ny, way+[(nx, ny)]))
    
    return [ways[1][0], ways[1][1], ct]

def find_store(arr, sx, sy, direc):
    candits, depth = [], 10000
    dq = deque([(sx, sy, 0)])
    visited = [[False]*N for _ in range(N)]
    visited[sx][sy] = True

    while dq:
        cx, cy, cost = dq.popleft()
        if depth < cost:
            continue
        if arr[cx][cy] == 1:
            if depth > cost:
                depth = cost
                candits = [(cx, cy, cost)]
            else:
                candits.append((cx, cy, cost))
        
        for k in range(4):
            nx, ny = cx+direc[k][0], cy+direc[k][1]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] == -1:
                continue
            if not visited[nx][ny]:
                visited[nx][ny] = True
                dq.append((nx, ny, cost+1))

    candits.sort(key=lambda x: (x[2], x[0], x[1]))
    tx, ty, _ = candits[0]
    return [tx, ty]

if __name__ == '__main__':
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    direc = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    basecamps, camp_flag = [], [True]*M
    for i in range(M):
        a, b = map(int, input().split())
        basecamps.append((a-1, b-1))

    time, cnt = 0, M
    q = []
    while cnt > 0:
        # move
        nt = min(time, M)
        cmds = []

        for i in range(0, nt):
            if not camp_flag[i]:
                continue
            cmds.append(move(arr, q[i], basecamps, direc))

        for nx, ny, nt in cmds:
            q[nt][0], q[nt][1] = nx, ny
            if (nx, ny) == basecamps[nt]:
                arr[nx][ny] = -1
                camp_flag[nt] = False
                cnt -= 1

        # new person
        if time < M:
            sx, sy = basecamps[time]
            nx, ny = find_store(arr, sx, sy, direc)
            arr[nx][ny] = -1
            q.append([nx, ny, time])
        time += 1

    print(time)