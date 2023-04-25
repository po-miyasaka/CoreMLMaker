
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

# CoreMLMaker

CoreMLMakerは、任意の動画（movやmp4）や画像から画像認識のためのデータセット作成し、学習済みモデルをmlmodel形式で出力するツールです。

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




<details>
  <summary><h1>README with English</h1></summary>

# CoreMLMaker

CoreMLMaker is a tool for creating image recognition datasets from videos (mov or mp4) and outputting the trained model in mlmodel format.

# Environment

The required packages are listed in `requirements.txt`. To install them, use the following command:

```
pip install -r requirements.txt
```

# Usage

```
python process.py <source folder name>
```

### Input

Specify a folder containing multiple videos as the source folder.  
The name of each video will be used as the label during image recognition. In other words, the number of labels generated will be equal to the number of videos.

In addition to videos, you can also use a folder containing multiple videos and images as the label by putting it in the source folder. For example, the following directory structure is also valid. In this case, two labels, `Tanuki` and `Kitsune`, will be generated.

```
$ tree source_folder

source_folder
├── Kitsune.mov
└── Tanuki
    ├── ponpoko.mov
    ├── omohide.mov
    └── kachikachiyama.jpeg
```

### Input Options

* If you only want to generate images for the dataset:

```
python process.py <source folder name> -m
```

* If you have already generated the dataset and only want to perform training and create an mlmodel:

```
python process.py <source folder name> -p 20230425100600
```
`20230425100600` is an example of a folder name automatically created in the `outputs` folder.

## Output

All outputs will be stored in the `outputs` folder. A unique folder name, such as `20230425100600`, will be generated each time the command is executed.

# How to test on an iPhone

Once the mlmodel is generated, the `ImageClassifier.mlmodel` will be saved in the Xcode project within the `iOSSample` folder. You can then build the app and easily test its functionality.

</details>