from collections import deque

n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
dp = [[1]*n for _ in range(n)]

for i in range(n):
    for j in range(n):

        # bfs
        dq = deque([(i, j)])
        visit = set()
        visit.add((i, j))

        while dq:
            cx, cy = dq.popleft()
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nx, ny = cx+dx, cy+dy
                if nx < 0 or nx >= n or ny < 0 or ny >= n or (nx, ny) in visit:
                    continue

                # 값이 작으면서 경로를 갱신할 수 있을 때
                if (arr[i][j] < arr[nx][ny]) and (dp[nx][ny] < dp[i][j] + 1):
                    dp[nx][ny] = dp[i][j]+1
                    visit.add((nx, ny))
                    dq.append((nx, ny))

max_value = 0    
for i in range(n):
    max_value = max(max_value, max(dp[i]))
print(max_value)