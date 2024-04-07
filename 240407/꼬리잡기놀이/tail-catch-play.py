from collections import deque

if __name__ == '__main__':
    N, M, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    direc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    groups = {}

    # grouping
    visited = [[False]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if arr[i][j] != 1:
                continue
            dq, group = deque([(i, j)]), [1]
            nd, ways = 0, deque([(i, j)])
            visited[i][j] = True
            
            while dq:
                cx, cy = dq.popleft()
                candits = []
                for k in range(4):
                    nx, ny = cx+direc[k][0], cy+direc[k][1]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N or arr[nx][ny] == 0:
                        continue
                    if not visited[nx][ny]:
                        candits.append((arr[nx][ny], nx, ny, k))

                if not candits:
                    break

                # 맨 처음일 경우  방향 select
                candits.sort(key=lambda x: x[0])
                _, nx, ny, cd = candits[0]
                if arr[cx][cy] == 1:
                    if cd in [0, 3]:
                        nd = 1
                    else:
                        nd = -1
                
                visited[nx][ny] = True
                dq.append((nx, ny))
                group.append(arr[nx][ny])
                ways.append((nx, ny))

            cnt = len(list(filter(lambda x: x<4, group)))
            groups[(cx, cy)] = [ways, cnt, nd]

    # shoot candits 
    shoots = []
    for i in range(N):
        shoots.append((i, 0, 1))
    for i in range(N):
        shoots.append((N-1, i, 0))
    for i in range(N):
        shoots.append((N-i, N-1, 3))
    for i in range(N):
        shoots.append((0, N-i, 2))

    ans = 0
    for time in range(K):
        # move
        group_candits = {}
        for (cx, cy), (ways, cnt, nd) in groups.items():
            ways.rotate(nd)
            group_candits[(cx, cy)] = [list(ways)[:cnt], nd]
        
        time = time % (4*N)
        tx, ty, td = shoots[time]

        flag, ckey, cvalue = True, None, None
        while flag and 0 <= tx < N and 0 <= ty < N:
            for key, value in group_candits.items():
                if (tx, ty) in value[0]:
                    ckey, cvalue = key, value
                    flag = False
                    break
            if flag:
                tx, ty = tx+direc[td][0], ty+direc[td][1]
        
        # 맞은게 없는 경우
        if ckey is None:
            continue

        idx = cvalue[0].index((tx, ty))
        # 순방향인 경우
        if cvalue[1] == 1:
            ans += ((idx+1)**2)
            groups[ckey][2] = -1
        else:
            ans += ((len(cvalue[0])-idx)**2)
            groups[ckey][2] = 1

    print(ans)