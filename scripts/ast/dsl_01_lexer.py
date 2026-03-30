"""
Step 1: Lexer (字句解析) の実装

目的: 
独自の言語（文字列）をプログラムが扱いやすいように、意味のある最小単位である「トークン(Token)」のリストに切り分けます。
これがAST（抽象構文木）を作り上げるための重要な下準備（ブロックの部品化）になります。

今回解析するDSL (Domain Specific Language) は、カメやロボットの制御コマンド風です。
"""

import re
from dataclasses import dataclass

# トークンの種類を明確にするための「型」を定義
@dataclass
class Token:
    type: str  # 'COMMAND', 'NUMBER', 'LBRACKET'(= [), 'RBRACKET'(= ])
    value: str # 実際の文字（'FORWARD', '10', '[', ']' など）
    
    def __repr__(self):
        # 画面に出力したときに見やすく表示するための関数
        return f"Token({self.type:8s}, {repr(self.value)})"

def lexer(source_code):
    """ただの文字列を受け取り、Tokenオブジェクトのリストにして返す関数"""
    tokens = []
    
    # =========================================================
    # 1. コードの文字列を、改行・空白を無視して1単語ずつ切り出す
    # =========================================================
    # 今回のルール: [, ], 英語の文字列, 数字の連続 のいずれかを取り出す
    raw_words = re.findall(r'\[|\]|[a-zA-Z]+|[0-9]+', source_code)
    
    # =========================================================
    # 2. 取り出した単語に「種類(Type)」を紐付けていく
    # =========================================================
    for word in raw_words:
        if word == '[':
            tokens.append(Token('LBRACKET', word))
        elif word == ']':
            tokens.append(Token('RBRACKET', word))
        elif word.isdigit():  # すべて数字の場合
            tokens.append(Token('NUMBER', word))
        elif word.isalpha():  # すべてアルファベットの場合
            tokens.append(Token('COMMAND', word.upper()))
        else:
            raise SyntaxError(f"未知の単語（非対応のトークン）です: {word}")
            
    return tokens

if __name__ == "__main__":
    # 解析するプログラム（ただの文字列変数）
    test_code = """
    FORWARD 10
    LEFT 90
    REPEAT 3 [
        FORWARD 20
    ]
    """
    
    print("=== 解析対象のソースコード ===")
    print(test_code)
    
    print("=== Lexer (字句解析) 実行結果 ===")
    tokens_list = lexer(test_code)
    
    for i, token in enumerate(tokens_list):
        print(f"[{i:02d}] {token}")
