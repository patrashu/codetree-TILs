import sys

n = int(input())
field = [list(map(int, input().split())) for _ in range(n)]
dp = [[sys.maxsize]*(n+1) for _ in range(n+1)]

for i in range(1, n+1):
    for j in range(n-1, -1, -1):
        v1, v2 = dp[i-1][j], dp[i][j+1]
        if v1 == sys.maxsize and v2 == sys.maxsize:
            dp[i][j] = field[i-1][j]
        elif v1 == sys.maxsize:
            dp[i][j] = v2 + field[i-1][j]
        elif v2 == sys.maxsize:
            dp[i][j] = v1 + field[i-1][j]
        else:
            dp[i][j] = min(v1, v2) + field[i-1][j]

print(dp[-1][0])