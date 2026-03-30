"""
Step 3: Parser (構文解析) の実装

目的:
Lexerが作った「単語（トークン）」の一直線の配列を読み込み、
文法規則（グラマー）に従って、ツリー構造である「ASTノード」に変換します。

これがプログラミング言語の中で「言葉の意味を解釈し、エラーを弾く」一番重要なプロセスです。
"""

from dsl_01_lexer import lexer, Token
from dsl_02_ast_nodes import BlockNode, CommandNode, RepeatNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # 現在読んでいる配列のインデックス（カーソル）

    def current_token(self):
        """今見ているトークンを返す（末尾に達した場合は None を返す）"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type):
        """指定した種類のトークンであることを確認し、カーソルを次に進める処理
        もし間違ったトークン（文法違反）が来たらエラーにする"""
        token = self.current_token()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        
        # 例：数字が来るはずなのにアルファベットが来た等
        actual = token.type if token else "EOF(ファイル終端)"
        raise SyntaxError(f"文法エラー: '{expected_type}' が必要ですが、'{actual}' と書かれています。")

    # ==============================================================
    # ここから「パース（解析）」のメインロジック
    # プログラムは「複数の命令（Statements）」の集まりなので、それを解析します
    # ==============================================================
    
    def parse_program(self):
        """プログラム全体のパースを開始するスタート地点"""
        statements = self.parse_statements()
        # 全ての処理を束ねる大元（BlockNode）に入れて返す
        return BlockNode(statements)

    def parse_statements(self):
        """複数の命令を順番に読んで、リストにまとめる処理"""
        statements = []
        
        # 配列の最後まで行くか、もしくは ']' (ブロックの終わり) が来るまで解析を続ける
        while self.current_token() is not None and self.current_token().type != 'RBRACKET':
            token = self.current_token()
            
            # トークンの「文字」によって「どの構文か」を判断する
            if token.type == 'COMMAND':
                if token.value == 'REPEAT':
                    statements.append(self.parse_repeat())
                else:
                    statements.append(self.parse_command())
            else:
                raise SyntaxError(f"予期しない構文です: {token}")
                
        return statements

    def parse_command(self):
        """単純なコマンド (例: FORWARD 10) を解釈する箱づめ作業"""
        # 1. まず 'COMMAND' を消費 (例: 'FORWARD')
        cmd_token = self.consume('COMMAND')
        
        # 2. 構文のルール上、次は必ず 'NUMBER' が来るはずなので消費 (例: '10')
        val_token = self.consume('NUMBER')
        
        # Step2 で作った「末端のノード(CommandNode)」に入れて返す
        return CommandNode(cmd_token.value, int(val_token.value))

    def parse_repeat(self):
        """繰り返し処理 (例: REPEAT 3 [ ... ]) を解釈する箱づめ作業"""
        # 1. 'REPEAT' というコマンドを消費
        self.consume('COMMAND')
        
        # 2. 次に「回数」の数字が来るはずなので消費
        count_token = self.consume('NUMBER')
        
        # 3. ブロックの開始 '[' を消費
        self.consume('LBRACKET')
        
        # 4. 【最大のミソ】'[' と ']' の中身（別の命令群）を再帰的にパースする！
        # これによって階層（ツリー構造）が作られ、何重にもネストされたブロックが表現可能になります。
        inner_statements = self.parse_statements()
        
        # 5. ブロックの終わり ']' を消費
        # ※ もし ']' の閉じ忘れがあれば、ここで構文エラーが発生します
        self.consume('RBRACKET')
        
        # Step2 で作った「子を持つノード(RepeatNode)」に入れて返す
        return RepeatNode(int(count_token.value), inner_statements)


if __name__ == "__main__":
    # 意地悪して、ネスト（階層化）を含んだプログラムを組んでテストします
    test_code = """
    FORWARD 10
    LEFT 90
    REPEAT 3 [
        FORWARD 20
        REPEAT 2 [
            RIGHT 45
        ]
    ]
    """
    print("=== 1. 元のソースコード ===")
    print(test_code)
    
    print("\n=== 2. トークン化 (Lexer) ===")
    tokens = lexer(test_code)
    print(f"トークン一覧({len(tokens)}個):")
    print([t.value for t in tokens])
    
    print("\n=== 3. 抽象構文木の生成 (Parser) ===")
    parser = Parser(tokens)
    
    # ここでAST（ツリー構造）が一気に組み上がる！
    ast_tree = parser.parse_program()
    
    # ダンプして見やすく表示
    print(ast_tree)
