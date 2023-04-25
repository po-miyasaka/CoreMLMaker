


# CoreMLMaker

CoreMLMakerは、動画（movやmp4）から画像認識用のデータセットを作成し、学習したモデルをmlmodel形式で出力するツールです。

# 環境

必要なパッケージは`requirements.txt`に記載されています。インストール方法は以下の通りです。

```
pip install -r requirements.txt
```

# 使用方法

```
python process.py <ソースフォルダ名>
```

### 入力

ソースフォルダ名には、複数の動画が含まれるフォルダを指定してください。各動画の名前が画像認識時のラベルとして使用されます。つまり、動画の数だけラベルが生成されます。

動画以外にも、複数の動画や画像が格納されたフォルダを入れることで、そのフォルダ名をラベルとして使用できます。例えば、以下のようなディレクトリ構成も有効です。この場合、`Tanuki`と`Kitsune`の2つのラベルが生成されます。

```
$ tree source_folder

source_folder
├── Kitsune.mov
└── Tanuki
    ├── ponpoko.mov
    ├── omohide.mov
    └── kachikachiyama.jpeg
```

### 入力オプション

* データセットの元となる画像生成のみを行いたい場合：

```
python process.py <ソースフォルダ名> -m
```

* データセットを生成済みで、学習とmlmodel作成のみを行いたい場合：

```
python process.py <ソースフォルダ名> -p 20230425100600
```
`20230425100600`は、自動的に`outputs`フォルダ内に作られるフォルダ名の一例です。


## 出力

`outputs`フォルダにすべての出力が格納されます。コマンドを実行するごとに`20230425100600`のようなユニークな名前のフォルダを生成します。

# iPhoneで動作確認する方法

mlmodelが生成されると、`iOSSample`内のXcodeプロジェクトに`ImageClassifier.mlmodel`が保存されます。
そのままアプリをビルドし、簡単に動作確認ができます。