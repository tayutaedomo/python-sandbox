"""
Step 3: DAGに基づく順次タスクランナー (Sequential Runner)

目的: Step 2 で得た「トポロジカルソート（正しい実行順序）」を利用して、
実際にダミーの処理（関数）を正しい順番で呼び出していく仕組みを作ります。
"""
import time
from collections import deque

# ==============================================================================
# 1. 各ノードごとの「実際の処理（タスク）」を定義する
# ==============================================================================
# 分かりやすくするために、よくあるデータ処理の工程に見立てています。
def task_a():
    print("  [実行中] タスク A: データのダウンロードを開始...")
    time.sleep(1.0) # 処理に1秒かかると仮定
    print("  [完了] タスク A")

def task_b():
    print("  [実行中] タスク B: データのフォーマット変換...")
    time.sleep(1.5) # 処理に1.5秒かかると仮定
    print("  [完了] タスク B")

def task_c():
    print("  [実行中] タスク C: データのマスキング処理...")
    time.sleep(1.0) # 処理に1秒かかると仮定
    print("  [完了] タスク C")

def task_d():
    print("  [実行中] タスク D: データベースへの保存...")
    time.sleep(0.5) # 処理に0.5秒かかると仮定
    print("  [完了] タスク D")

# ノード名(文字列)と、実行する関数(オブジェクト)のマッピング辞書
task_registry = {
    'A': task_a,
    'B': task_b,
    'C': task_c,
    'D': task_d,
}

# 対象のDAG（これまでと同じ構造）
# A (ダウンロード) ---> B (変換) -------> D (保存)
#  \                               /
#   \-> C (マスキング) -------------/
adjacency_list = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

# ==============================================================================
# 2. カーンのアルゴリズム（Step 2で作成したものと同じ）
# ==============================================================================
def get_execution_order(graph):
    """グラフ(隣接リスト)をトポロジカルソートして、実行順序を返す"""
    in_degrees = {node: 0 for node in graph.keys()}
    for targets in graph.values():
        for target in targets:
            if target not in in_degrees:
                in_degrees[target] = 0
            in_degrees[target] += 1
            
    queue = deque([node for node, count in in_degrees.items() if count == 0])
    sorted_result = []
    
    while queue:
        current = queue.popleft()
        sorted_result.append(current)
        for target in graph.get(current, []):
            in_degrees[target] -= 1
            if in_degrees[target] == 0:
                queue.append(target)
                
    if len(sorted_result) != len(in_degrees):
        raise ValueError("循環（ループ）を検出しました！")
    return sorted_result

# ==============================================================================
# 3. 順次実行ランナー本体
# ==============================================================================
def run_sequential_dag(graph, registry):
    print("=== DAG 順次実行エンジン 起動 ===")
    
    # [1] 実行順序を計算
    print("[1] 依存関係から実行順序を計算しています...")
    execution_order = get_execution_order(graph)
    print(f"  -> 計算完了: {' -> '.join(execution_order)}\n")
    
    start_time = time.time()
    
    # [2] 算定された順序に沿って、順番に(forループで)関数を呼び出す
    print("[2] タスクの順次実行を開始します")
    for task_name in execution_order:
        func = registry.get(task_name)
        if callable(func):
            func() # 関数を実行 ()
        else:
            print(f"  [エラー] タスク '{task_name}' に対応する関数が見つかりません！")
            
    end_time = time.time()
    
    # [3] フィニッシュ
    print(f"\n=== 全タスク完了 ===")
    print(f"総実行時間: {end_time - start_time:.2f} 秒")
    # ここでの総実行時間は、各タスクの処理時間（1.0 + 1.5 + 1.0 + 0.5 = 約 4.0秒）の合計になります。

if __name__ == "__main__":
    run_sequential_dag(adjacency_list, task_registry)
