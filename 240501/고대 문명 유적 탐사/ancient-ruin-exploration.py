"""
5x5 격자에 유물 조각이 배치되어 있음
1~7까지 총 7가지 종류로 표현됨

1. 탐사 진행
- 3x3 격자 선택해서 90/180/270도 회전할 수 있음.
- 가능한 회정 방법 중
    - 유물 1차 획득 가치를 최대화
    - 여러개일경우 회전한 각도가 가장 작은 방법
    - 여러개일 경우 회전 중심 좌표의 열이 가장 작은 구간
    - 여러개일 경우 행이 가장 작은 구간 선택

2. 유물 획득
- 상하좌우로 인접한 같은 종류의 유물 조각 (3개 이상) => 사라짐
- 유물의 가치는 모인 조각의 개수랑 같음
- 비어있는 곳을 채워나가야 함 (유리 조각과 함께)
    - 벽면 순서대로 새로운 조각이 생겨남    
    - 열 번호가 작은 순서대로, 행 번호가 큰 순서대로 조각이 생겨남

3. 유물 연쇄 획득
- 새 유물조각이 생겨나고 값을 채웠는데 3개 이상 엮인 유물이 있으면 2번 반복

4. K턴 동안 위 과정 반복
- 각 턴마다 획득한 유물 가치의 총 합을 출력하는 프로그램 작성
- 어떤 방법으로도 유물을 획득할 수 없다면 탐색 종료

-> 회전하고 전체탐색
-> 

"""
from collections import deque

def rotate(arr):
    return [list(matrix[::-1]) for matrix in zip(*arr)]

k, m = map(int, input().split())
field = [list(map(int, input().split())) for _ in range(5)]
wall_nums = deque(list(map(int, input().split())))
direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]

time = 0
tmp = 0
while time < k:
    candits = []

    for i in range(1, 4):
        for j in range(1, 4):
            for rot in range(4):
                sub_arr = [arr[j-1:j+2] for arr in field[i-1:i+2]]
                sub_arr = rotate(sub_arr)

                for p in range(3):
                    for q in range(3):
                        field[p+i-1][q+j-1] = sub_arr[p][q]

                if rot == 3:
                    continue

                cur_paths = []
                visit = [[False]*5 for _ in range(5)]
                for p in range(5):
                    for q in range(5):
                        if visit[p][q]:
                            continue
                        
                        path = [(p, q)]
                        dq = deque([(p, q)])
                        visit[p][q] = True

                        while dq:
                            cx, cy = dq.popleft()                            
                            for dx, dy in direc:
                                nx, ny = cx+dx, cy+dy
                                if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                                    continue
                                if visit[nx][ny] or field[nx][ny] != field[p][q]:
                                    continue
                                visit[nx][ny] = True
                                path.append((nx, ny))
                                dq.append((nx, ny))

                        if len(path) < 3:
                            continue
                        cur_paths.extend(path)
                candits.append((cur_paths, i, j, rot)) # path, cx, cy, rot

    # select 
    candits.sort(key=lambda x: (-len(x[0]), x[3], x[2], x[1]))
    paths, cx, cy, rot = candits[0]
    if len(paths) == 0:
        break

    tmp += len(paths)

    # update
    for _ in range(rot+1):
        sub_arr = [arr[cy-1:cy+2] for arr in field[cx-1:cx+2]]
        sub_arr = rotate(sub_arr)

        for p in range(3):
            for q in range(3):
                field[p+cx-1][q+cy-1] = sub_arr[p][q]
    
    paths.sort(key=lambda x: (x[1], -x[0]))
    for tx, ty in paths:
        field[tx][ty] = wall_nums.popleft()

    # check
    while True:
        n_paths = []
        visit = [[False]*5 for _ in range(5)]
        for p in range(5):
            for q in range(5):
                if visit[p][q]:
                    continue

                paths = [(p, q)]
                dq = deque([(p, q)])
                visit[p][q] = True
                while dq:
                    cx, cy = dq.popleft()                            
                    for dx, dy in direc:
                        nx, ny = cx+dx, cy+dy
                        if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                            continue
                        if visit[nx][ny] or field[nx][ny] != field[p][q]:
                            continue
                        visit[nx][ny] = True
                        paths.append((nx, ny))
                        dq.append((nx, ny))

                if len(paths) >= 3:
                    n_paths.extend(paths)

        if not n_paths:
            break

        tmp += len(n_paths)
        n_paths.sort(key=lambda x: (x[1], -x[0]))
        for tx, ty in n_paths:
            field[tx][ty] = wall_nums.popleft()

    print(tmp, end=" ")          
    tmp = 0
    time += 1