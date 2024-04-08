"""
NxN 격자에 나무 있음
제초제를 뿌려 성장을 억제하고자 한다
제초제는 K 범위만큼 대각선으로 퍼진다 (벽은 전파 x)

(1). 나무 성장 (o)
- 인접한 칸 중 나무가 있는 칸만큼 성장
- 성장은 동시에 일어남

(2). 번식 진행 (o)
- 인접한 4칸 중 다른 나무나 제초제가 모두 없는 칸에 번식을 진행
- 41일때 번식 가능한 칸이 두개면 각 칸에 20씩 들어감
- 번식은 동시에 일어남

(3). 제초제 뿌림
- 제추제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제를 뿌림
- 나무 없는 칸에 제초제 뿌리면 나무가 없는 상태로 끝남
- 나무 있는 칸에 제초제 뿌리면 4개의 대각선 방향으로 K만큼 전파 됨.
- 중간에 벽이거나 나무가 없으면 그 칸까지는 뿌림
- c년만큼 제초제가 남아있다가 c+1이 될 때 사라지게 됨.
- 제초제 있는데 또 뿌리면 c로 초기화

벽: -1이거나 out of bound일 경우
나무 matrix 하나랑, 제초제 matrix 하나?
"""
from collections import defaultdict

def growth(arr, N, direc):
    g_mat = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if arr[i][j] <= 0: # not tree
                continue
            
            for k in range(0, 8, 2):
                nx, ny = i+direc[k][0], j+direc[k][1]
                if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] <= 0:
                    continue
                g_mat[i][j] += 1

    for i in range(N):
        for j in range(N):
            arr[i][j] += g_mat[i][j]

def seed(arr, med, N, direc):
    s_mat = [[0]*N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if arr[i][j] <= 0:
                continue
            candits = []
            for k in range(0, 8, 2):
                nx, ny = i+direc[k][0], j+direc[k][1]
                if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] == -1: # if wall
                    continue

                if arr[nx][ny] == 0 and med[nx][ny] == 0:
                    candits.append((nx, ny))
            
            for tx, ty in candits:
                s_mat[tx][ty] += arr[i][j] // len(candits)

    for i in range(N):
        for j in range(N):
            arr[i][j] += s_mat[i][j]

def remove(arr, med, N, direc, K, C):
    ans = defaultdict(list)

    for i in range(N):
        for j in range(N):
            if arr[i][j] <= 0:
                continue

            cnt, candits = arr[i][j], [(i, j)]
            for k in range(1, 8, 2):
                nx, ny, dx, dy = i, j, *direc[k]
                time = 0

                while time < K:
                    nx, ny = nx+dx, ny+dy
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        break
                    candits.append((nx, ny))
                    if arr[nx][ny] <= 0:
                        break
                    cnt += arr[nx][ny]
                    time += 1

            ans[cnt].append((i, j, candits))

    cnt, r_mat = sorted(ans.items(), key=lambda x: (-x[0]))[0]
    r_mat.sort(key=lambda x: (x[0], x[1]))
    for tx, ty in r_mat[0][2]:
        med[tx][ty] = C+1
        if arr[tx][ty] > 0:
            arr[tx][ty] = 0
    return cnt

def release(med, N):
    for i in range(N):
        for j in range(N):
            if med[i][j] == 0:
                continue
            med[i][j] -= 1

if __name__ == '__main__':
    N, M, K, C = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    med = [[0]*N for _ in range(N)]
    direc = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    res = 0
    for _ in range(M):
        growth(arr, N, direc)
        seed(arr, med, N, direc)
        res += remove(arr, med, N, direc, K, C)
        release(med, N)

    print(res)