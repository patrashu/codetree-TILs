from itertools import combinations
from collections import deque, defaultdict

def rotate(arr):
    return [list(matrix[::-1]) for matrix in zip(*arr)]

if __name__ == '__main__':
    n = int(input())
    arr = [list(map(int, input().split())) for _ in range(n)]
    half, score = n//2, 0
    sub_pos = [(0, 0), (0, half+1), (half+1, 0), (half+1, half+1)]
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for _ in range(4):
        # search
        groups, cnt = defaultdict(list), 0
        visited = [[False]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if visited[i][j]:
                    continue
                dq = deque([(i, j)])
                pos = set()
                pos.add((i, j))
                visited[i][j] = True

                while dq:
                    cx, cy = dq.popleft()
                    for k in range(4):
                        nx, ny = cx+direc[k][0], cy+direc[k][1]
                        if nx < 0 or nx >= n or ny < 0 or ny >= n or arr[nx][ny] != arr[i][j]:
                            continue
                        if not visited[nx][ny]:
                            visited[nx][ny] = True
                            dq.append((nx, ny))
                            pos.add((nx, ny))

                groups[cnt] = list(pos)
                cnt += 1
        
        combs = combinations(list(range(cnt)), 2)
        for g1, g2 in combs:
            g1, g2 = groups[g1], groups[g2]
            cnt = 0
            for x, y in g1:
                for k in range(4):
                    nx, ny = x+direc[k][0], y+direc[k][1]
                    if nx < 0 or nx >= n or ny < 0 or ny >= n:
                        continue
                    if (nx, ny) in g2:
                        cnt += 1

            score += (len(g1)+len(g2)) * arr[g1[0][0]][g1[0][1]] * arr[g2[0][0]][g2[0][1]] * cnt

        row, col = [], []
        # center rotate
        for i in range(n):
            row.append(arr[i][half])
            col.append(arr[half][i])

        for i in range(n):
            arr[i][half] = col[n-i-1]
            arr[half][i] = row[i]

        # sub arr rotate
        for sx, sy in sub_pos:
            sub_arr = [row[sy:sy+half] for row in arr[sx:sx+half]]
            sub_arr = rotate(sub_arr)

            for p in range(half):
                for q in range(half):
                    arr[sx+p][sy+q] = sub_arr[p][q]
    
    print(score)