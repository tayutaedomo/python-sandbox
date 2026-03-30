"""
Step 4: asyncioを用いた並列タスクランナー (Async Runner)

目的: Step 3 の順次実行の欠点（無駄な待ち時間）を解消するため、
依存関係（矢印）がないタスク同士は、同時に並行して実行する仕組みを作ります。
"""
import asyncio
import time

# ==============================================================================
# 1. 各ノードごとの「実際の処理（タスク）」を定義する（非同期版）
# ==============================================================================
# 順次実行(time.sleep)と違い、asyncio.sleep()を使うことで、
# 待機中に別のタスクへ処理を譲ることができます。

async def task_a():
    print("  [実行中] タスク A: データのダウンロードを開始...")
    await asyncio.sleep(1.0)
    print("  [完了] タスク A")

async def task_b():
    print("  [実行中] タスク B: データのフォーマット変換...")
    await asyncio.sleep(1.5) # Cの1.0秒よりも長くかかるタスク
    print("  [完了] タスク B")

async def task_c():
    print("  [実行中] タスク C: データのマスキング処理...")
    await asyncio.sleep(1.0)
    print("  [完了] タスク C")

async def task_d():
    print("  [実行中] タスク D: データベースへの保存...")
    await asyncio.sleep(0.5)
    print("  [完了] タスク D")

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
# 2. 並列エンジンのコア機能
# ==============================================================================
# これまでのように前もって「A -> B -> C -> D」という配列は作りません。
# リアルタイムで「その瞬間に実行できる状態になっているもの」を動かします。

async def run_async_dag(graph, registry):
    print("=== DAG [非同期・並列] 実行エンジン 起動 ===")
    start_time = time.time()
    
    # [準備1] 全ノードの初期入次数（待つべき事前タスク数）を計算
    in_degrees = {node: 0 for node in graph.keys()}
    for targets in graph.values():
        for target in targets:
            if target not in in_degrees:
                in_degrees[target] = 0
            in_degrees[target] += 1
            
    # [準備2] 現在実行中のタスクを管理する辞書
    # 形式: { asyncio.Taskオブジェクト : "タスク名('A'など)" }
    running_tasks = {}
    
    def spawn_ready_tasks():
        """現在の入次数が「0」のタスクを探して、実行を開始する関数"""
        for node, count in list(in_degrees.items()):
            if count == 0:
                func = registry.get(node)
                # asyncio.create_task() で、裏側（バックグラウンド）で関数を実行開始させる
                task_obj = asyncio.create_task(func())
                running_tasks[task_obj] = node
                
                # 「実行開始済み」として扱うため、カウントを -1 に落として二重実行を防ぐ
                in_degrees[node] = -1

    # -------------------------------------------------------------
    # 実行スタート
    # -------------------------------------------------------------
    # まず、最初から入次数0のもの（今回は 'A'）を起動する
    spawn_ready_tasks()
    
    # 実行中のタスクが1つでもある限り、ループして見守る
    while running_tasks:
        
        # [ポイント] 動いているタスクのうち、「どれか1つでも完了するまで」待つ
        done_tasks, pending_tasks = await asyncio.wait(
            running_tasks.keys(),
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # 今回完了したタスクについて、後処理を行う
        for task_obj in done_tasks:
            node_name = running_tasks.pop(task_obj) # 管理リストから外す
            
            # このタスクが終わったことで、依存先の入次数をそれぞれ -1 する
            for target in graph.get(node_name, []):
                in_degrees[target] -= 1
                
        # 誰かが終わって入次数が減ったため、新しく起動できるようになったタスクがないか探して起動する
        spawn_ready_tasks()

    end_time = time.time()
    print("\n=== 全タスク完了 ===")
    print(f"総実行時間: {end_time - start_time:.2f} 秒")
    # A(1.0) + [B(1.5) と C(1.0) を並行] + D(0.5) ＝ 理想的には約 3.0秒 になる！

if __name__ == "__main__":
    # Pythonの非同期エンジンのエントリーポイント
    asyncio.run(run_async_dag(adjacency_list, task_registry))
