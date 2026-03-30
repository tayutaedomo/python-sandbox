"""
Step 4: Evaluator (評価・実行エンジン) の実装

目的:
Step 3で作られた「AST（抽象構文木）」を上から下へ、
または階層に沿ってなぞり、実際の処理（プログラムの実行）を行います。

今回はASTの内容を使って、架空のロボットの「座標と向き」を計算します。
これが自分だけのプログラミング言語（DSL）の最終形態である「インタプリタ」です。
"""

import math
from dsl_01_lexer import lexer
from dsl_02_ast_nodes import BlockNode, CommandNode, RepeatNode
from dsl_03_parser import Parser

class Robot:
    """ASTの命令によって動く架空のロボット（状態の管理）"""
    def __init__(self):
        self.x = 0.0          # 現在のX座標
        self.y = 0.0          # 現在のY座標
        self.angle = 90.0     # 現在の向いている角度(度)。90度が真上(北)
        
    def move_forward(self, distance):
        # 角度から進む方向のX/Y成分を計算
        rad = math.radians(self.angle)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
        print(f"  🤖 [{distance}歩 進む] -> 現在地: ({self.x:.1f}, {self.y:.1f})")
        
    def turn_left(self, degrees):
        self.angle = (self.angle + degrees) % 360
        print(f"  🤖 [{degrees}度 左に回転] -> 現在の向き: {self.angle}度")
        
    def turn_right(self, degrees):
        self.angle = (self.angle - degrees) % 360
        print(f"  🤖 [{degrees}度 右に回転] -> 現在の向き: {self.angle}度")


class Evaluator:
    """ASTを読み取って実行するエンジン（インタプリタ）"""
    def __init__(self):
        self.robot = Robot()

    # ==============================================================
    # ASTの「箱の型」ごとにメソッドを振り分ける機構 (Visitorパターン)
    # ==============================================================
    
    def evaluate(self, node):
        """どんなノードが来ても、適切な実行メソッドに振り分ける入口"""
        # Nodeのクラス名を取得 (例えば 'CommandNode' や 'RepeatNode')
        node_name = type(node).__name__
        
        # 'eval_CommandNode' のように対応する関数を動的に呼び出す
        method_name = f'eval_{node_name}'
        eval_method = getattr(self, method_name, self.eval_unknown)
        return eval_method(node)

    def eval_unknown(self, node):
        raise RuntimeError(f"未対応の命令（ノード）です: {type(node).__name__}")

    # ==============================================================
    # 各ASTノードに対する「実際の処理（Evaluate）」
    # ==============================================================

    def eval_BlockNode(self, node: BlockNode):
        """ブロック（複数の命令）を上から順番に実行する"""
        for statement in node.statements:
            self.evaluate(statement)

    def eval_CommandNode(self, node: CommandNode):
        """単純なコマンドを解釈してロボットに命令を送る"""
        if node.command == 'FORWARD':
            self.robot.move_forward(node.value)
        elif node.command == 'LEFT':
            self.robot.turn_left(node.value)
        elif node.command == 'RIGHT':
            self.robot.turn_right(node.value)
        else:
            print(f"  [警告] 解釈できないコマンドです: {node.command}")

    def eval_RepeatNode(self, node: RepeatNode):
        """繰り返し（ループブロック）を実行する"""
        # ASTに書いてある「回数(count)」だけループを回る
        for i in range(node.count):
            print(f"--🔁 ループ開始 ({i+1}/{node.count}回目) --")
            # 中身として格納されている階層ノード(子要素たち)を再帰的に順番に実行する！
            for statement in node.body:
                self.evaluate(statement)
            print("--🔁 ループ終了 --\n")


# ==============================================================
# 実行エントリーポイント（今までの全行程をまとめて実行）
# ==============================================================
if __name__ == "__main__":
    
    # 1. あなたが書いたプログラムコード（ただの文字列）
    # 今回は「上に少し進んでから、四角形(正方形)を描くようにロボットを動かす」プログラム！
    source_code = """
    FORWARD 10
    REPEAT 4 [
        FORWARD 5
        RIGHT 90
    ]
    """
    
    print("=== 解析対象のソースコード ===")
    print(source_code)
    
    # 2. 字句解析 (Lexer) -> 文字列をトークンの配列（部品）にする
    tokens = lexer(source_code)
    
    # 3. 構文解析 (Parser) -> トークン配列からAST（階層化された木構造）を作る
    parser = Parser(tokens)
    ast_tree = parser.parse_program()
    
    print("\n=== 自作言語の実行（Evaluation）開始 ===")
    
    # 4. ASTの評価・実行 (Evaluator) -> ASTを読みながらPythonの命令を動かす！
    evaluator = Evaluator()
    evaluator.evaluate(ast_tree)
    
    print("🎉 自作言語（DSL）のインタプリタが完成しました！")
