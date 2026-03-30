"""
Step 2: ASTノード（クラス）の定義

目的: 
Lexerで切り分けたトークンたちを、意味のある「構造体」として組み立てる際に使う
「入れ物（クラス）」の設計図を定義します。

今回作る言語には以下の要素があります：
1. 一般的なコマンド (例: FORWARD 10)
2. 繰り返しブロック (例: REPEAT 3 [ ... ])
3. プログラム全体の集まり (複数行をまとめるブロック)
"""
from dataclasses import dataclass
from typing import List

# =========================================================
# 1. 基底となるノードクラス
# =========================================================
class ASTNode:
    """すべてのASTノードの親クラス（共通の目印）"""
    pass

# =========================================================
# 2. 個別のノードの設計図
# =========================================================

@dataclass
class CommandNode(ASTNode):
    """単一のコマンドを表す「葉（末端）」のノード
    例: FORWARD 10
    """
    command: str  # 例: 'FORWARD'
    value: int    # 例: 10
    
    def __repr__(self):
        return f"CommandNode('{self.command}', {self.value})"

@dataclass
class RepeatNode(ASTNode):
    """繰り返し処理を表す「枝（子を持つ）」のノード
    例: REPEAT 3 [ ... ]
    
    ここに「子ノード（body）」をリスト構造として持たせることで、
    言語の構文が「木（深さを持つツリー構造）」に成長します！
    """
    count: int            # 繰り返す回数 (例: 3)
    body: List[ASTNode]   # [...] の中身のノード（階層構造になる！）
    
    def __repr__(self):
        # 階層が深くなった時に見やすく出力するための工夫
        body_str = ",\n        ".join(repr(node) for node in self.body)
        return f"RepeatNode(count={self.count}, body=[\n        {body_str}\n    ])"

@dataclass
class BlockNode(ASTNode):
    """プログラム全体、または複数行の処理を束ねるノード"""
    statements: List[ASTNode]
    
    def __repr__(self):
        stmt_str = ",\n    ".join(repr(node) for node in self.statements)
        return f"BlockNode([\n    {stmt_str}\n])"


# =========================================================
# 3. ダミーデータを使って「手動で」ASTを組み立ててみる
# =========================================================
if __name__ == "__main__":
    # 📝 解析対象とするソースコードのイメージ:
    # FORWARD 10
    # REPEAT 2 [
    #     LEFT 90
    # ]
    
    # 手作業で上のコードのAST（ツリー構造）を作ってみる
    # (次の Step 3 では、これを自動的に組み立てるパーサーを作ります)
    
    manual_ast = BlockNode(
        statements=[
            CommandNode("FORWARD", 10),
            RepeatNode(
                count=2,
                body=[
                    CommandNode("LEFT", 90)
                ]
            )
        ]
    )
    
    print("=== AST（抽象構文木）の構造 ===")
    print(manual_ast)
