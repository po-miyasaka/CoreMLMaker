# CoreMLMaker
動画(movやmp4)から画像認識用のデータセットを作成、学習しmlmodelを出力する。


# 環境
requirement.textに記載


# 使用方法
```
python process.py <source folder名>   
```
## 入力
引数のフォルダには複数の動画含むことができ、各動画の名前が画像認識時の出力されるラベルとして使われます。
つまり、動画の数だけラベルが生成されます。

また、動画以外にも複数動画や画像が格納されたフォルダを入れることにより、そのフォルダ名をラベルとして使うこともできます。
例えば、以下のようなディレクトリ構成も有効です。この場合、`Tanuki`と`Kitsune`の2つのラベルが生成されます。

```
$ tree source_folder                                                       

source_folder
├── Kitsune.mov
└── Tanuki
    ├── ponpoko.mov
    └── tanuki.jpeg
```

### オプション
```
python process.py <source folder名> -m
```
データセットの元となる画像生成のみ行います。

```
python process.py <source folder名> -p 20230425100600
```
`20230425100600`は自動的に`outputs`フォルダ内に作られるフォルダ名の一例です。
`-m`オプションですでにデータセットを生成済みの場合に、学習とmlmodel作成のみを行いたい場合に有効です。

### 出力
`outputs`フォルダにすべてのoutputが格納されます。コマンドを叩くごとに`20230425100600`のようなフォルダ名を作成します。


### iPhoneで動作確認する

mlmodelがビルドできると`iOSSample`ディレクトリにも`ImageClassifier.mlmodel`が保存されるのでそのままアプリをビルドして簡単に試すことができます。