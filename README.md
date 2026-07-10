*This project has been created as part of the 42 curriculum by tsito, ksaotome.*

# A-Maze-ing

## Description

A-Maze-ingは、設定ファイルに従ってランダムな迷路を生成し、その構造を
16進数形式でファイルへ出力するとともに、迷路を視覚的に表示するプロジェクトである。

本プロジェクトの主な目標を以下に示す。

- seedによって再現可能な迷路をランダム生成する
- 完全迷路と非完全迷路の両方に対応する
- 壁、入口、出口、最短経路が整合した迷路を生成する
- 完全に閉じたセルを使い、迷路内に視認可能な「42」を配置する
- 各セルの壁を16進数1桁で表してファイルへ出力する
- 迷路と最短経路を視覚的に表示する
- 迷路生成処理を、別プロジェクトから利用できるPythonパッケージとして提供する

### 予定ディレクトリ構成

設計意図を明確にするため、未実装のファイルも含めている。

```text
.
├── .gitignore
├── .python-version
├── README.md
├── Makefile
├── a_maze_ing.py
├── config.txt
├── pyproject.toml
├── uv.lock
├── src/
│   └── mazegen/
│       ├── __init__.py
│       ├── generator.py
│       └── py.typed
├── tests/
└── mazegen-<version>-py3-none-any.whl
```

- `a_maze_ing.py`: 設定の読み込み、迷路生成、出力、視覚表示を統括する、
  課題指定のエントリーポイントである
- `config.txt`: 課題で求められているデフォルト設定ファイルである
- `src/mazegen/generator.py`: `MazeGenerator`クラスを含む、再利用可能な
  迷路生成モジュールである
- `src/mazegen/__init__.py`: `MazeGenerator`などの公開APIを外部へ公開する
- `src/mazegen/py.typed`: インストールしたパッケージが型情報を提供することを示す
- `tests/`: 迷路生成、検証、経路探索、設定解析、出力形式の開発用テストを置く
- `pyproject.toml`: プロジェクト情報、Python要件、依存関係、ビルド設定を記述する
- `uv.lock`: uvが生成する依存関係のロックファイルである
- `.python-version`: ローカル開発で使用するPythonバージョンを指定する
- `Makefile`: インストール、実行、デバッグ、クリーンアップ、lintを定義する
- `mazegen-<version>-py3-none-any.whl`: ビルド済みの再利用パッケージである。
  `.tar.gz`形式を使用することもできる

## Instructions

### 必要な環境

- Python 3.10以上
- uv
- Make

Pythonの最低対応バージョンは、課題要件に合わせて3.10とする予定。

```toml
requires-python = ">=3.10"
```

### インストール

依存関係と仮想環境はuvで管理する方針。

```bash
uv sync
```

Makefile実装後は、次のコマンドでもインストールできるようにする予定。

```bash
make install
```

### 実行

課題で指定されている実行形式は次のとおり。

```bash
python3 a_maze_ing.py config.txt
```

uv環境から実行する場合は次の形式を予定している。

```bash
uv run python a_maze_ing.py config.txt
```

`config.txt`は設定ファイルの例であり、別のファイル名やパスを指定できる。
コマンドライン引数として受け取るのは設定ファイル1個のみである。

```bash
uv run python a_maze_ing.py configs/large.txt
```

### デバッグ、lint、クリーンアップ

Makefileには、課題で指定された以下のルールを実装する予定。

```bash
make debug
make lint
make lint-strict
make clean
```

`lint`では次のコマンドを実行する。

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

`lint-strict`では次のコマンドを実行する予定。

```bash
flake8 .
mypy . --strict
```

### パッケージのビルド

再利用可能な`mazegen`パッケージは、次のコマンドでビルドできる構成にする予定。

```bash
uv build --out-dir .
```

生成予定の成果物は次のいずれか、または両方である。

```text
mazegen-<version>-py3-none-any.whl
mazegen-<version>.tar.gz
```

パッケージのビルド設定とソースは未実装である。

## Configuration

設定ファイルはプレーンテキストで、1行につき1個の`KEY=VALUE`を記述する。
`#`から始まる行はコメントとして無視する。

### 必須キー

| キー | 形式 | 説明 | 例 |
|---|---|---|---|
| `WIDTH` | 正の整数 | 迷路の幅をセル数で指定する | `WIDTH=20` |
| `HEIGHT` | 正の整数 | 迷路の高さをセル数で指定する | `HEIGHT=15` |
| `ENTRY` | `x,y` | 入口の座標を指定する | `ENTRY=0,0` |
| `EXIT` | `x,y` | 出口の座標を指定する | `EXIT=19,14` |
| `OUTPUT_FILE` | ファイルパス | 迷路の出力先を指定する | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True`または`False` | 完全迷路を生成するか指定する | `PERFECT=True` |

### 追加予定キー

seedによる再現性を提供する必要があるため、次の追加キーを採用する予定である。

| キー | 形式 | 説明 | 状態 |
|---|---|---|---|
| `SEED` | 整数 | 乱数生成のseedを指定する | 採用予定、詳細未決定 |

生成アルゴリズムや表示方式を設定ファイルから選択できるようにするかは未決定である。

### 設定例

```ini
# Default maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Team and Project Management

### チーム構成と役割

| メンバー | 役割 |
|---|---|
| tsito | 未決定 |
| ksaotome | 未決定 |

### 予定している開発計画

1. 課題要件を整理し、データ構造とディレクトリ構成を決定する
2. 設定ファイルのパース処理を実装する
3. 「42」を考慮した完全迷路生成を実装する
4. 非完全迷路生成と最短経路探索を実装する
5. 16進数形式の出力と検証を実装する
6. 視覚表示とユーザー操作を実装する
7. 再利用パッケージとドキュメントを完成させる
8. テスト、flake8、mypy、パッケージ再ビルドを確認する

### 計画の変化

開発開始前のため、当初計画からの変化はまだない。設計変更や予定との差異が発生した
時点で、理由と結果をこの節へ記録する。

### うまくいったこと

- 課題PDFの必須要件を実装前に整理した
- Python 3.10とuvを利用する開発環境の方針を決めた

### 改善できること

現時点では評価できない。開発中に発生した問題、
見積もりとの差、テスト不足などをプロジェクト完了前に追記する。

### 使用ツール

| ツール | 用途 |
|---|---|
| Python 3.10 | 実装と実行 |
| uv | Python、仮想環境、依存関係、ビルドの管理 |
| Git | バージョン管理 |
| flake8 | コーディング規約の検査 |
| mypy | 静的型検査 |
| pytest | 開発用テスト |
| Make | 必須コマンドの自動化 |

## Advanced Features

現時点で高度な追加機能は未実装である。

- 複数の迷路生成アルゴリズム: 未決定
- 迷路生成アニメーション: 未決定
- 複数の表示モード: 未決定
- 「42」専用色: 未決定

追加機能を実装した場合は、その使い方と技術的選択をこの節へ追記する。

## Resources

### 参考資料

- [uv公式ドキュメント](https://docs.astral.sh/uv/)

迷路生成アルゴリズムに関する参考資料は、アルゴリズム決定後に追加する。

### AIの利用

AIは現時点で、以下の作業に使用した。

- 課題PDFの日本語での整理と必須要件の確認
- 仮想環境およびuvの使い方の調査
- 主要な迷路生成アルゴリズムとトレードオフの比較
