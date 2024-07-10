from collections import deque

n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
dp = [[1]*n for _ in range(n)]
direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]


for i in range(n):
    for j in range(n):
        flag = False
        for dx, dy in direction:
            nx, ny = i+dx, j+dy
            if 0 <= nx < n and 0 <= ny < n and arr[i][j] < arr[nx][ny]:
                flag = True
                break

        if not flag:
            continue

        # bfs
        dq = deque([(i, j)])

        while dq:
            cx, cy = dq.popleft()
            for dx, dy in direction:
                nx, ny = cx+dx, cy+dy
                # 범위에 벗어날 때 
                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue

                # 값이 작으면서 경로를 갱신할 수 있을 때
                if (arr[cx][cy] < arr[nx][ny]) and (dp[nx][ny] < dp[cx][cy]+1):
                    dp[nx][ny] = dp[cx][cy]+1
                    dq.append((nx, ny))

max_value = 0    
for i in range(n):
    max_value = max(max_value, max(dp[i]))
print(max_value)