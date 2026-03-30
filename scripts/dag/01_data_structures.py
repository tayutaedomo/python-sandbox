"""
DAG (Directed Acyclic Graph: 有向非巡回グラフ) の基本データ構造

このスクリプトでは、以下のシンプルなDAGを3つの異なるデータ構造で表現します。
目的: プログラム上でDAGをどのように保持・管理できるかを比較して学びます。

[対象のDAG]
A ---> B ---> D
 \           /
  \-> C ----/
"""

# ==============================================================================
# 1. 隣接リスト (Adjacency List)
# ==============================================================================
# 辞書(dict)を使って、「あるノード」から「どのノードへ矢印が伸びているか」を表す形式。
# グラフアルゴリズムで最も一般的で、メモリ効率も良く、走査（探索）が容易です。

# キー: ノード名, 値: そのノードから直接遷移できるノードのリスト
adjacency_list = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

def show_adjacency_list():
    print("--- 1. 隣接リスト (Adjacency List) ---")
    for node, edges in adjacency_list.items():
        print(f"ノード {node} -> {edges if edges else '終点'}")
    print()

def show_mermaid():
    print("--- おまけ: 隣接リストからMermaidフローチャート生成 ---")
    print("graph TD")
    for node, edges in adjacency_list.items():
        for edge in edges:
            print(f"    {node} --> {edge}")
    print()


# ==============================================================================
# 2. オブジェクト指向表現 (Node Base / Object-Oriented)
# ==============================================================================
# ノードをクラスのインスタンスとして表現し、親や子の参照を持たせる形式。
# 個々のノードにタスクの実行関数や状態（成功・失敗・未実行など）を持たせやすいため、
# 実際のワークフローエンジン（Airflowなど）の内部構造に近いアプローチです。

class DagNode:
    def __init__(self, name):
        self.name = name
        self.children = [] # 子ノード（依存される側）のリスト
        self.parents = []  # 親ノード（依存する側）のリスト

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parents.append(self)
        
    def __repr__(self):
        return f"Node({self.name})"

# ノードのインスタンス化
node_a = DagNode('A')
node_b = DagNode('B')
node_c = DagNode('C')
node_d = DagNode('D')

# エッジ（依存関係）の定義
node_a.add_child(node_b)
node_a.add_child(node_c)
node_b.add_child(node_d)
node_c.add_child(node_d)

def show_object_oriented():
    print("--- 2. オブジェクト指向表現 (Object-Oriented) ---")
    nodes = [node_a, node_b, node_c, node_d]
    for n in nodes:
        parent_names = [p.name for p in n.parents]
        child_names = [c.name for c in n.children]
        print(f"ノード {n.name}: 親={parent_names}, 子={child_names}")
    print()


# ==============================================================================
# 3. 隣接行列 (Adjacency Matrix)
# ==============================================================================
# 2次元配列（行列）を使い、ノード間の接続関係を 0 (接続なし) と 1 (接続あり) で表現。
# 行列演算との相性が良く数学的アプローチに向いていますが、
# ノードが多く接続が少ない（疎なグラフ）場合はメモリの無駄が多くなります。

# ノード名とインデックスの対応付けが必要
# A: 0, B: 1, C: 2, D: 3
node_indices = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
index_to_node = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

# 4x4 の初期化（すべて0）
adjacency_matrix = [
    [0, 0, 0, 0],  # Aからの接続 (A->B, A->C を後で1にする)
    [0, 0, 0, 0],  # Bからの接続 (B->D を1にする)
    [0, 0, 0, 0],  # Cからの接続 (C->D を1にする)
    [0, 0, 0, 0]   # Dからの接続 (なし)
]

# 接続（エッジ）の定義
adjacency_matrix[node_indices['A']][node_indices['B']] = 1
adjacency_matrix[node_indices['A']][node_indices['C']] = 1
adjacency_matrix[node_indices['B']][node_indices['D']] = 1
adjacency_matrix[node_indices['C']][node_indices['D']] = 1

def show_adjacency_matrix():
    print("--- 3. 隣接行列 (Adjacency Matrix) ---")
    print("    A B C D")
    for i, row in enumerate(adjacency_matrix):
        print(f"{index_to_node[i]} | {' '.join(map(str, row))}")
    print()


if __name__ == "__main__":
    print("[目的のDAG構造]")
    print("A ---> B ---> D")
    print(" \\           /")
    print("  \\-> C ----/\n")
    
    show_adjacency_list()
    show_mermaid()
    show_object_oriented()
    show_adjacency_matrix()
