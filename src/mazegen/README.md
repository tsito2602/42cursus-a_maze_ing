# mazegen

`mazegen`は、入口から出口までの最短経路を持つ迷路を生成する
再利用可能なPythonパッケージである。

## Installation

リポジトリ直下でビルドしたwheelをインストールする。

```bash
python3 -m pip install ./mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

`MazeGenerator`を作成し、`generate()`を呼び出すと`Maze`が返る。

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
)

maze = generator.generate()

print(maze.cells)
print(maze.solution)
```

## Custom Parameters

生成条件は`MazeGenerator`の引数で指定する。

```python
generator = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit_=(29, 19),
    perfect=False,
    seed=42,
    wall_break_ratio=0.3,
)
```

| 引数 | 内容 |
|---|---|
| `width` | 迷路の幅 |
| `height` | 迷路の高さ |
| `entry` | 入口の`(x, y)`座標 |
| `exit_` | 出口の`(x, y)`座標 |
| `perfect` | `True`なら完全迷路、`False`なら複数経路を持つ迷路を生成する |
| `seed` | 乱数のseed。同じ設定とseedからは同じ迷路が生成される |
| `wall_break_ratio` | 非完全迷路で開く壁の目標割合。デフォルトは`0.3` |

`perfect`のデフォルトは`True`、`seed`のデフォルトは`None`である。
`seed=None`の場合、生成結果は実行ごとに変わる。

## Accessing the Generated Maze

`MazeGenerator.generate()`は、生成済みの迷路を表す`Maze`を返す。
`Maze`は、壁情報、入口、出口、最短経路、「42」のセルを保持する
不変のデータモデルである。生成後に各属性を書き換えることはできない。

```python
from mazegen import Maze, MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
)

maze: Maze = generator.generate()
```

座標はすべて`(x, y)`形式で表す。一方、`maze.cells`は行優先の
2次元タプルなので、特定の座標のセルには`maze.cells[y][x]`でアクセスする。
最短経路の`maze.solution`には、入口と出口を含む座標が順番に格納される。

```python
cells = maze.cells
solution = maze.solution

entry_cell = cells[maze.entry[1]][maze.entry[0]]

print(entry_cell)
print(solution[0])   # maze.entry
print(solution[-1])  # maze.exit
```

| 属性 | 内容 |
|---|---|
| `maze.cells` | 壁情報を持つ行優先の2次元タプル |
| `maze.entry` | 入口の座標 |
| `maze.exit` | 出口の座標 |
| `maze.solution` | 入口から出口までの最短経路を表す座標のタプル |
| `maze.pattern_cells` | 「42」を構成するセルの座標 |
| `maze.width` | 迷路の幅 |
| `maze.height` | 迷路の高さ |

`maze.cells[y][x]`は、そのセルの閉じた壁を表す0から15までの整数である。
壁は`Wall`のビットフラグを使って調べられる。

```python
from mazegen import Wall

cell = maze.cells[0][0]

if cell & Wall.NORTH:
    print("The north wall is closed.")
```

| フラグ | 値 | 方角 |
|---|---:|---|
| `Wall.NORTH` | `0b0001` | 北 |
| `Wall.EAST` | `0b0010` | 東 |
| `Wall.SOUTH` | `0b0100` | 南 |
| `Wall.WEST` | `0b1000` | 西 |
