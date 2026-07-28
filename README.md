*This project has been created as part of the 42 curriculum by tsito, ksaotome.*

# A-Maze-ing

## Description

A-Maze-ingは、設定ファイルからランダムな迷路を生成し、壁情報と最短経路を
ファイルへ出力するとともに、ANSIカラー対応ターミナルへ迷路を表示する
Pythonプロジェクトである。

### Project Structure

アプリケーション固有の処理と、再利用可能な迷路生成処理を分離している。

```text
.
├── a_maze_ing.py
├── amazeing/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── display.py
│   ├── output.py
│   ├── parse.py
│   └── player.py
├── src/
│   └── mazegen/
│       ├── __init__.py
│       ├── generator.py
│       ├── maze.py
│       ├── py.typed
│       └── solve.py
├── tests/
├── config.txt
├── Makefile
├── pyproject.toml
└── uv.lock
```

- `a_maze_ing.py`: 課題指定のエントリーポイント
- `amazeing/`: 設定解析、ファイル出力、表示、操作などのアプリケーション処理
- `src/mazegen/`: pipでインストールできる再利用可能な迷路生成パッケージ
- `tests/`: 生成、経路探索、表示、設定解析、プレイヤー操作のテスト

### Mandatory

- seedを指定した再現可能な迷路生成
- 完全迷路と、複数経路を持つ非完全迷路の生成
- 外周壁、隣接セル間の壁、入口、出口の整合性維持
- 完全に閉じたセルによる「42」パターンの配置
- 各セルの壁を16進数1桁で表したファイル出力
- 幅優先探索による入口から出口までの最短経路
- 迷路、入口、出口、最短経路のターミナル表示
- 迷路の再生成、最短経路の表示切り替え、壁色変更
- 別プロジェクトへインストールできる`mazegen`パッケージ

### Bonus

- WASD操作による迷路探索
- 出口到達時のクリア画面

## Instructions

### Requirements

- Python 3.10以上
- uv
- Make
- ANSIカラーを表示できるターミナル

### Installation

依存関係と開発環境を準備する。

```bash
make install
```

同じ処理は次のコマンドでも実行できる。

```bash
uv sync
```

### Running the Application

課題指定の実行形式は次のとおりである。

```bash
python3 a_maze_ing.py config.txt
```

uv環境では次のコマンドを使用できる。

```bash
make run
```

別の設定ファイルを指定する場合は`CONFIG`を上書きする。

```bash
make run CONFIG=path/to/config.txt
```

引数の不足、ファイルの不存在、不正な設定値、生成不可能な条件などは、
エラーメッセージとして標準出力へ表示される。

### Interactive Controls

| キー | 動作 |
|---|---|
| `W` / `A` / `S` / `D` | プレイヤーを上下左右へ移動する |
| `1` | 新しい迷路を生成する |
| `2` | 最短経路の表示と非表示を切り替える |
| `3` | 壁の色を切り替える |
| `4` | 終了する |

プレイヤーが出口へ到達するとクリア画面を表示し、新しい迷路の生成または
終了を選択できる。

### Development Commands

```bash
make debug
make test
make lint
make lint-strict
make clean
```

- `debug`: Pythonの`pdb`でアプリケーションを起動する
- `test`: pytestのテストを実行する
- `lint`: 課題指定のflake8とmypyを実行する
- `lint-strict`: mypyのstrictモードを含む、より厳しい検査を実行する
- `clean`: Pythonとテストのキャッシュを削除する

## Configuration

設定ファイルはプレーンテキストで、1行につき1個の`KEY=VALUE`を記述する。
空行と`#`から始まるコメント行は無視される。キーの重複、未知のキー、
不正な型、迷路外の座標はエラーになる。

| キー | 必須 | 形式 | 説明 | 例 |
|---|---|---|---|---|
| `WIDTH` | 必須 | 1以上の整数 | 迷路の幅 | `WIDTH=20` |
| `HEIGHT` | 必須 | 1以上の整数 | 迷路の高さ | `HEIGHT=15` |
| `ENTRY` | 必須 | `x,y` | 入口の座標 | `ENTRY=0,0` |
| `EXIT` | 必須 | `x,y` | 出口の座標 | `EXIT=19,14` |
| `OUTPUT_FILE` | 必須 | ファイルパス | 生成結果の出力先 | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | 必須 | `True`または`False` | 完全迷路を生成するか | `PERFECT=True` |
| `SEED` | 任意 | 整数 | 乱数のseed | `SEED=42` |

`ENTRY`と`EXIT`は迷路内の異なるセルでなければならない。同じ設定とseedを
使用すると同じ迷路が生成される。`SEED`を省略した場合は実行ごとに異なる
乱数系列を使用する。

設定例:

```ini
# Default maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

### Maze Representation and Output

各セルは0から15までの整数で表し、各ビットが閉じた壁を示す。

| ビット | 値 | 方角 |
|---|---:|---|
| 0 | `0x1` | North |
| 1 | `0x2` | East |
| 2 | `0x4` | South |
| 3 | `0x8` | West |

ビットが1なら壁は閉じており、0なら開いている。例えば`3`は北と東、
`a`は東と西に壁がある。

出力ファイルにはセルを行ごとに16進数で保存する。その後に空行を置き、
入口、出口、最短経路を記録する。経路は`N`、`E`、`S`、`W`で表す。

```text
<hexadecimal maze rows>

0,0     # entry (x, y)
19,14     # exit (x, y)
EESS...
```

## Maze Generation Algorithm

### Perfect Maze

完全迷路の生成には、ランダム化深さ優先探索による
バックトラッキング法を使用する。この方式は一般に
`recursive backtracker`とも呼ばれるが、本実装では再帰関数の代わりに
リストをスタックとして使い、同じ探索を反復的に行う。

1. 全セルを4方向の壁で閉じる
2. 「42」を構成するセルを訪問済みとして扱う
3. 入口から未訪問の隣接セルをランダムに選ぶ
4. 現在セルと隣接セルの共有壁を両側から開く
5. 行き止まりでは直前のセルへ戻る
6. 到達可能な全セルを訪問するまで繰り返す

このアルゴリズムは、訪問済みセルへ新しい通路を開かないため、
非パターンセルをつなぐ通路が木構造になる。その結果、任意の2セル間の
経路が1つだけの完全迷路を生成できる。

### Imperfect Maze

`PERFECT=False`の場合は、完全迷路の生成後に閉じた共有壁をランダムに
追加で開き、複数経路を作る。壁を開いた結果、壁のない3×3領域ができる
場合はその変更を取り消す。「42」のセルと外周壁は開かない。

### Shortest Path

最短経路は幅優先探索で求める。入口から通行可能な隣接セルを順番に探索し、
各セルへ到達した直前のセルを保存する。出口へ到達後、その記録を逆向きに
たどって`Maze.solution`を構築する。

### The “42” Pattern

「42」は迷路中央付近の完全に閉じたセルで構成する。迷路が小さく配置できない
場合は、コンソールへエラーメッセージを表示してパターンを省略する。

## Why This Algorithm

この方法を採用した理由は、実装が比較的単純で、
外周壁と共有壁の整合性を保ちやすく、seedによる再現も容易だからである。
また、明示的なスタックを使うことで、深い再帰によるPythonの
再帰上限を避けている。

## Code Reusability

迷路生成処理は`src/mazegen`へ分離されており、A-Maze-ing本体に依存しない。
標準的なPythonパッケージとしてwheelまたはsource distributionを生成できる。

### Building

```bash
make build
```

成果物はリポジトリ直下へ生成される。

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```

wheelを別の仮想環境へインストールする例:

```bash
python3 -m pip install ./mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    perfect=True,
    seed=42,
)

maze = generator.generate()

print(maze.cells)
print(maze.solution)
```

`width`と`height`で迷路の大きさ、`entry`と`exit_`で入口と出口、
`perfect`で完全迷路かどうか、`seed`で再現性を指定する。

### Maze Data Model

`MazeGenerator.generate()`は、生成結果を`Maze`として返す。`Maze`は
迷路の壁、入口、出口、最短経路、「42」のセルをまとめて保持する
不変のデータモデルである。作成時に、セルの行幅が揃っていることと、
各座標が迷路の範囲内にあることを検証する。

生成された`Maze`から次の情報へアクセスできる。

| 属性 | 内容 |
|---|---|
| `maze.cells` | 壁情報を持つ行優先の不変な2次元タプル |
| `maze.entry` | 入口の`(x, y)`座標 |
| `maze.exit` | 出口の`(x, y)`座標 |
| `maze.solution` | 入口から出口までの最短経路 |
| `maze.pattern_cells` | 「42」を構成するセル座標 |
| `maze.width` | 迷路の幅 |
| `maze.height` | 迷路の高さ |

壁を個別に調べる場合は`Wall`を使用できる。

```python
from mazegen import Wall

first_cell = maze.cells[0][0]

if first_cell & Wall.NORTH:
    print("The north wall is closed.")
```

`mazegen`は`py.typed`を含み、インストール先でも型情報を利用できる。

## Team and Project Management

### Roles

| メンバー | 主な担当 |
|---|---|
| tsito | config解析、データモデル、表示とCLI、非完全迷路、プレイヤー操作、パッケージ構成、テストと統合 |
| ksaotome | 完全迷路生成、最短経路探索、ファイル出力処理、テストと統合 |

両メンバーでPull Requestを確認し、命名、型、データ構造、テストを調整した。

### Planning and Evolution

当初は、設定解析、迷路生成、経路探索、出力、表示、再利用パッケージの順に
実装する計画を立てた。開発中は各機能を小さなブランチに分けて統合し、
完全迷路を基礎としてから非完全迷路と表示機能を追加した。

最短経路探索は当初のクラス構成から単純な幅優先探索関数へ整理した。
表示機能では迷路と最短経路の表示を先に完成させ、その後にWASD操作と
クリア判定を追加した。終盤ではアプリケーション用の`amazeing`と、
配布対象の`src/mazegen`を分離し、wheelへ必要なコードだけが入るようにした。

### What Worked Well

- 開発前に全体の見通しを立て、ペアで実装方針と分担の
  コンセンサスを取れた
- 機能ごとにブランチを分け、変更範囲を明確にしながら開発できた
- 生成、探索、表示、操作を分離したため、機能ごとにテストできた
- seedを利用し、生成結果を再現しながら問題を調査できた
- 型ヒント、mypy、flake8を継続して利用し、統合時の不整合を減らせた
- 完全迷路を基礎に非完全迷路を追加し、実装の重複を避けられた

### What Could Be Improved

- READMEが実装より遅れて更新され、「予定」の記述が長く残った
- 表示とプレイヤー移動で通路グリッドの構築処理が似ており、変更時には
  両方の整合性を確認する必要があった
- CLI全体の操作テストを早い段階で追加すれば、機能統合をさらに安全にできた

### Tools

| ツール | 用途 |
|---|---|
| Python 3.10 | 実装と実行 |
| uv | 仮想環境、依存関係、Python、ビルドの管理 |
| Git / GitHub | バージョン管理、ブランチ開発、Pull Request |
| Make | 必須コマンドの自動化 |
| pytest | 単体テストとCLIテスト |
| flake8 | コーディング規約の検査 |
| mypy | 静的型検査 |
| Pydantic | 設定値と迷路データの検証 |

## Resources

### References

- [深さ優先探索 — Wikipedia](https://ja.wikipedia.org/wiki/深さ優先探索)
- [幅優先探索 — Wikipedia](https://ja.wikipedia.org/wiki/幅優先探索)
- [random — 疑似乱数を生成する](https://docs.python.org/ja/3/library/random.html)
- [collections.deque — 両端キュー](https://docs.python.org/ja/3/library/collections.html#collections.deque)
- [enum.IntFlag — ビットフラグ用の列挙型](https://docs.python.org/ja/3/library/enum.html#enum.IntFlag)
- [Python Packaging User Guide 日本語版](https://packaging.python.org/ja/latest/)

### Use of AI

AIは次の作業を補助するために使用した。

- 課題PDFの要件整理と、実装・提出物との照合
- ディレクトリ構成とPythonパッケージ公開範囲のレビュー
- WASD操作、境界値、CLI遷移に対するレビュー観点の洗い出し
- テストケースとREADME構成の検討
- ビルド成果物、flake8、mypy、pytestの検証結果の整理

AIの提案はそのまま採用せず、実装、テスト、生成したwheelの内容を確認した上で
プロジェクトへ反映した。
