"""
DAGのトポロジカルソート（Topological Sort）

目的:
「Aが終わらないとBに進めない」といった依存関係（隣接リスト）から、
「実際にどの順番でタスクを実行すれば成立するか」を計算するアルゴリズムを学びます。

ここでは、ワークフローエンジンでよく使われる「カーンのアルゴリズム(Kahn's algorithm)」
を実装します。これは「入次数（自分に向かってくる矢印の数）」の概念を使います。
"""

from collections import deque

def topological_sort(adjacency_list):
    """
    隣接リストから、正しい実行順序を計算して返す関数。
    循環（ループ）が発見された場合はエラーを送出します。
    """
    # -------------------------------------------------------------
    # 1. すべてのノードの「入次数（in-degree）」を計算する
    # -------------------------------------------------------------
    # 入次数とは「そのタスクを実行する前に、終わらせるべきタスクの数」です。
    
    # まず全ノードの入次数を 0 で初期化
    in_degrees = {node: 0 for node in adjacency_list.keys()}
    
    # 全ての矢印（エッジ）を数えて、向かっている先の入次数を +1 する
    for node, targets in adjacency_list.items():
        for target in targets:
            if target not in in_degrees:
                in_degrees[target] = 0 # グラフの終端ノードがキーに無い場合への対応
            in_degrees[target] += 1
            
    print("[1] 各ノードの初期入次数（待つ必要がある事前タスク数）:")
    for node, count in in_degrees.items():
        print(f"  - ノード {node}: {count} 個")

    # -------------------------------------------------------------
    # 2. 最初から実行可能な（入次数がゼロの）ノードをキューに入れる
    # -------------------------------------------------------------
    # 入次数が 0 ＝「誰も待つ必要がない」ので、すぐに開始できます。
    queue = deque([node for node, count in in_degrees.items() if count == 0])
    
    print(f"\n[2] 最初から実行可能なノード (入次数0): {list(queue)}")

    # -------------------------------------------------------------
    # 3. 順番に処理しながら、依存関係を解除していく
    # -------------------------------------------------------------
    sorted_result = []  # 最終的な実行順序を記録するリスト
    
    while queue:
        # キューから１つ取り出して「実行完了」とする
        current_node = queue.popleft()
        sorted_result.append(current_node)
        
        # 完了したタスクが指していた先（依存先）の入次数を 1 減らす
        # （事前タスクが１つ終わったため）
        for target in adjacency_list.get(current_node, []):
            in_degrees[target] -= 1
            
            # もし事前タスクがすべて終わった（入次数が0になった）ら、キューに入れる
            if in_degrees[target] == 0:
                queue.append(target)
                print(f"  -> タスク '{current_node}' 完了により、タスク '{target}' が実行可能になりました！")

    # -------------------------------------------------------------
    # 4. ループ（循環）のチェック
    # -------------------------------------------------------------
    # 取り出したノードの数が、グラフ全体のノード数と一致しなければ、
    # どこかで「お互いを待ち続けている（ループ）」状態が発生しています。（DAGではない）
    if len(sorted_result) != len(in_degrees):
        raise ValueError("循環参照（ループ）が検出されました！これはDAGではありません。")

    return sorted_result


def topological_sort_dfs(adjacency_list):
    """
    [おまけ] 深さ優先探索（DFS）ベースのトポロジカルソート
    再帰を用いて、「依存関係の一番奥（終点）」まで進んでからリストに追加していくアプローチです。
    """
    # グラフに含まれる全ノードを収集
    nodes = set()
    for node, edges in adjacency_list.items():
        nodes.add(node)
        for edge in edges:
            nodes.add(edge)
            
    visited = set()      # 訪問済み（完了）のノード
    visiting = set()     # 現在探索中のノード（循環チェック用）
    sorted_result = []   # 結果リスト

    def dfs(node):
        if node in visiting:
            raise ValueError(f"循環（ループ）が検出されました: '{node}'")
        if node in visited:
            return  # 既に処理済みならスキップ

        # 「現在探索中」マークをつける
        visiting.add(node)

        # 自分が依存している先（矢印の先）を、さらに奥へと再帰的に処理する
        for target in adjacency_list.get(node, []):
            dfs(target)

        # 依存先がすべて処理されたら「探索中」を解除して「完了」にする
        visiting.remove(node)
        visited.add(node)
        
        # 結果の末尾に追加する（最も奥＝末端のノードが最初に追加される）
        sorted_result.append(node)

    print("\n[DFS] 探索開始...")
    # どのノードから探索を始めてもOK
    for node in sorted(nodes): # 出力を安定させるためにソート
        if node not in visited:
            print(f" -> '{node}' から奥へ探索")
            dfs(node)

    # 依存先の奥から追加されているため、最後にリスト全体を反転(Reverse)して返す
    return sorted_result[::-1]


if __name__ == "__main__":
    # テスト用のDAG（Step 1 と同じ形）
    # A ---> B ---> D
    #  \           /
    #   \-> C ----/
    
    test_dag = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    
    print("=== 1. カーンのアルゴリズム (BFSベース) ===")
    order_kahn = topological_sort(test_dag)
    print(f"\n[結果] 正しい実行順序: {' -> '.join(order_kahn)}\n")

    print("=== 2. 深さ優先探索 (DFSベース) ===")
    order_dfs = topological_sort_dfs(test_dag)
    print(f"\n[結果] 正しい実行順序: {' -> '.join(order_dfs)}\n")
