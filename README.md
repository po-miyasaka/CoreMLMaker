
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Python 3.8.16](https://img.shields.io/badge/python-3.8.16-blue.svg)](https://www.python.org/downloads/release/python-3816/)


![logo](logo.png)

# CoreML Maker

CoreML Makerは、任意の動画（mov/mp4）や画像から画像認識のためのデータセット作成し、学習済みモデルをmlmodel形式で出力するツールです。

<p align="center">
  <img src="sample.gif" alt="operation image">
</p>

# 動作環境

* Mac x86_64 (Ventura 13.0)
* Python 3.8.16

必要なパッケージは`requirements.txt`に記載されています。  
インストール方法は以下の通りです。
```
$ pip install -r requirements.txt
```
### 動作確認環境
* Xcode 14.2
* iPhone11 Pro (iOS 16.3.1)



# 使用方法
### 入力
```shell
$ python process.py <ソースフォルダ名>
```
ソースフォルダ名には、複数の動画が含まれるフォルダを指定してください。各動画の名前が画像認識時のラベルとして使用されます。つまり、動画の数だけラベルが生成されます。

動画以外にも、複数の動画や画像が格納されたフォルダをソースフォルダ入れることで、そのフォルダ名をラベルとして使用できます。
再帰的にフォルダを読み込むので、Kaggleなどでダウンロードしたデータセットを気軽にフォルダごと格納することも可能です。

例えば、以下のようなディレクトリ構成も有効です。
この場合、`Tanuki`と`Kitsune`の2つのラベルが生成されます。

```shell
$ tree source_folder

source_folder
├── Kitsune.mov
└── Tanuki
    ├── ponpoko.mov
    ├── doutanuki.jpg
    └── Kachikachiyama
        ├── chagama.jpg
        ├── konohagakure.jpg
        └── shigarakiyaki.mp4
```

### 入力オプション

* データセットの元となる画像生成のみを行いたい場合：

```shell
python process.py <ソースフォルダ名> -m
```

* データセットを生成済みで、学習とmlmodel作成のみを行いたい場合：

```shell
python process.py <ソースフォルダ名> -p 20230425100600
```
`20230425100600`は、自動的に`outputs`フォルダ内に作られるフォルダ名の一例です。

### config.py
アウトプットの画像のパラメータや学習用の関数をconfig.pyに切り出してあるので調整できます。

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

* Mac x86_64 (Ventura 13.0)
* Xcode 14.2
* iPhone11 Pro (iOS 16.3.1)
* Python 3.8.16

The required packages are listed in `requirements.txt`. To install them, use the following command:

```shell
$ pip install -r requirements.txt
```

# Usage
### Input

```shell
$ python process.py <source folder name>
```

Specify a folder containing multiple videos as the source folder.  
The name of each video will be used as the label during image recognition. In other words, the number of labels generated will be equal to the number of videos.

In addition to videos, you can also use a folder containing multiple videos and images as the label by putting it in the source folder. For example, the following directory structure is also valid. In this case, two labels, `Tanuki` and `Kitsune`, will be generated.

```shell
$ tree source_folder

source_folder
├── Kitsune.mov
└── Tanuki
    ├── ponpoko.mov
    ├── omohide.jpg
    └── kachikachiyama
        ├── one.jpg
        ├── two.jpg
        └── three.mov
```

### Input Options

* If you only want to generate images for the dataset:

```shell
$ python process.py <source folder name> -m
```

* If you have already generated the dataset and only want to perform training and create an mlmodel:

```
$ python process.py <source folder name> -p 20230425100600
```
`20230425100600` is an example of a folder name automatically created in the `outputs` folder.

## Output

All outputs will be stored in the `outputs` folder. A unique folder name, such as `20230425100600`, will be generated each time the command is executed.

# How to test on an iPhone

Once the mlmodel is generated, the `ImageClassifier.mlmodel` will be saved in the Xcode project within the `iOSSample` folder. You can then build the app and easily test its functionality.

</details>
