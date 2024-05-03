import heapq
from collections import defaultdict
INF = int(1e9)

def preprocess(cmds):
    # create edges
    n, m = cmds[0], cmds[1]
    graph = defaultdict(int)
    for i in range(2, len(cmds), 3):
        v, u, w = cmds[i: i+3]
        if graph[(v, u)] == 0:
            graph[(v, u)] = w
            graph[(u, v)] = w
        elif graph[(v, u)] > w:
            graph[(v, u)] = w
            graph[(u, v)] = w
    
    new_graph = defaultdict(list)
    for (st, et), v in graph.items():
        new_graph[st].append((et, v))
    return new_graph, n
    
def find_min_dist(new_graph, n, pnid):
    dist = [INF]*n
    dist[pnid] = 0
    hq = [(pnid, 0)]

    while hq:
        cnode, ccost = heapq.heappop(hq)
        if dist[cnode] < ccost:
            continue
    
        for nnode, ncost in new_graph[cnode]:
            if ccost + ncost < dist[nnode]:
                dist[nnode] = ccost+ncost
                heapq.heappush(hq, (nnode, ncost+ccost))
    return dist

def create_candits_from_cur_node(items, min_dist, cur_node):
    _hq = []
    for pid, (rev, dst) in items.items():
        if min_dist[cur_node][dst] != INF:
            heapq.heappush(_hq, (-(rev - min_dist[cur_node][dst]), pid))
    return _hq

def create_item(items, cmds):
    items[cmds[0]] = tuple(cmds[1:])

def remove_item(items, cmds):
    try:
        del items[cmds[0]]
    except:
        pass

def sell_optimal_item(items, candits):
    npid = None
    while candits:
        cost, pid = heapq.heappop(candits)
        if cost <= 0 and items.get(pid, -1) != -1:
            npid = pid
            break

    if npid is None:
        return -1
    
    del items[npid]
    return npid

if __name__ == '__main__':
    graph, min_dist, items = None, dict(), dict()
    n, cur_node, candits = None, 0, []
    for time in range(int(input())):
        cmds = list(map(int, input().split()))
        if cmds[0] == 100:
            graph, n = preprocess(cmds[1:])
            min_dist[0] = find_min_dist(graph, n, 0)
            candits = create_candits_from_cur_node(items, min_dist, cur_node)
        elif cmds[0] == 200:
            create_item(items, cmds[1:])
            if min_dist[cur_node][cmds[3]] != INF:
                heapq.heappush(candits, (-(cmds[2] - min_dist[cur_node][cmds[3]]), cmds[1]))
        elif cmds[0] == 300:
            remove_item(items, cmds[1:])
        elif cmds[0] == 400:
            print(sell_optimal_item(items, candits))
        elif cmds[0] == 500:
            cur_node = cmds[1]
            if min_dist.get(cur_node, -1) == -1:
                min_dist[cur_node] = find_min_dist(graph, n, cur_node)
            candits = create_candits_from_cur_node(items, min_dist, cur_node)