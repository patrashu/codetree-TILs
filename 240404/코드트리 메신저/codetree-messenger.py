"""
이진 트리란 모든 노드의 자식이 2개 이하인 트리

(1). 사내 메신저 준비
- 0~N번까지 N+1개의 채팅방이 있으며, 회사의 메인 채팅방을 제외한 각 채팅방은 부모 채팅방이 있음
- 메인 : 항상 0, 각 채팅방의 부모 채팅방 번호는 parents로 주어짐
- 각 채팅방은 권한을 가지고 있음
- authority만큼 상위로 올라가서 알림을 보냄
- 0번 채팅방은 아무 관련 없음

(2). 알림망 설정 ON/OFF
- 첨엔 다 ON
- 기능 작동시 ON -> OFF / OFF -> ON으로 바꿔줌
- 알림 OFF면 나 포함 위로 알림올리지 않음

(3). 권한 세기 변경
- c번 채팅방 권한 세기를 power로 변경

(4). 부모 교환
- 동일 level의 c1 부모와 c2 부모를 서로 바꿈
- 자식도 함께 딸려감

(5). 알림을 받을 수 있는 채팅방 수 조회
- c번 채팅방까지 도달할 수 있는 서로 다른 채팅방 수를 출력
"""
from collections import deque, defaultdict

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_children(self, node):
        self.children.append(node)


class Tree:
    def __init__(self):
        self.head = Node(0)
        self.idx_to_node = {0: [None, self.head]}
        self.status = None
        self.authority = None

    def set_node(self, arr, authority):
        self.status = [True] * (len(arr)+1)
        self.authority = [0] + authority
        tmp = defaultdict(list)

        for idx, parent in enumerate(arr):
            tmp[parent].append(idx+1)

        dq = deque([self.head])
        while dq:
            cnode = dq.popleft()
            v = cnode.value
            for nnode in tmp[v]:
                new_node = Node(nnode)
                self.idx_to_node[nnode] = [v, new_node]
                cnode.children.append(new_node)
                dq.append(new_node)


def convert_status(tree, node):
    tree.status[node] = True if not tree.status[node] else False

def convert_power(tree, node, power):
    tree.authority[node] = power

def convert_parent(tree, node1, node2):
    pnode1, node1 = tree.idx_to_node[node1]
    pnode2, node2 = tree.idx_to_node[node2]
    pnode1 = tree.idx_to_node[pnode1][1]
    pnode2 = tree.idx_to_node[pnode2][1]

    if len(pnode1.children) == 2:
        if pnode1.children[0] == node1:
            pnode1.children[0] = node2
        else:
            pnode1.children[1] = node2
    else:
        pnode1.children[0] = node2

    if len(pnode2.children) == 2:
        if pnode2.children[0] == node2:
            pnode2.children[0] = node1
        else:
            pnode2.children[1] = node1
    else:
        pnode2.children[0] = node1

def search(tree, node):
    snode = tree.idx_to_node[node][1]
    dq = deque([(snode, 0)])
    cnt = 0

    while dq:
        cnode, depth = dq.popleft()
        for nnode in cnode.children:
            v = nnode.value
            if not tree.status[v]:
                continue
            if tree.authority[v] >= depth+1:
                cnt += 1
            dq.append((nnode, depth+1))
    return cnt


if __name__ == '__main__':
    N, Q = map(int, input().split())
    tree = None
    for _ in range(Q):
        cmd, *line = list(map(int, input().split()))
        if cmd == 100:
            tree = Tree()
            tree.set_node(line[:N], line[N:])
        elif cmd == 200:
            convert_status(tree, line[0])
        elif cmd == 300:
            convert_power(tree, line[0], line[1])
        elif cmd == 400:
            convert_parent(tree, line[0], line[1])
        elif cmd == 500:
            print(search(tree, line[0]))