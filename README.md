# 📘 手書きノート永久保存プロジェクト

手書きノートをiPhoneで撮影し、OCR処理によって検索可能なPDFとして保存するプロジェクトです。

## 🚀 クイックスタート

### 1. 必要なソフトウェアのインストール

```bash
# Pythonパッケージのインストール
pip install -r requirements.txt

# img2pdfのインストール（PDF生成用）
pip install img2pdf

# システムレベルのツール（macOS）
brew install tesseract  # OCR処理用（将来の機能）
```

### 2. サンプル画像の生成

```bash
# テスト用のサンプル画像を作成
python scripts/create_sample_images.py
```

### 3. 画像をPDFに変換

#### Python版（推奨）
```bash
# 基本的な使用方法
python scripts/make_pdf.py Notebooks/サンプルノート01

# カスタム出力ファイル名を指定
python scripts/make_pdf.py Notebooks/サンプルノート01 --output カスタム名.pdf

# 詳細な出力
python scripts/make_pdf.py Notebooks/サンプルノート01 --verbose
```

#### Bash版
```bash
# 基本的な使用方法
./scripts/make_pdf.sh Notebooks/サンプルノート01
```

## 📁 プロジェクト構成

```
notebook-archive/
├── Notebooks/                    # ノートブック保存ディレクトリ
│   ├── サンプルノート01/           # 各ノートブックは個別のフォルダに保存
│   │   ├── IMG_0001.jpg
│   │   ├── IMG_0002.jpg
│   │   ├── ...
│   │   └── サンプルノート01.pdf    # 生成されたPDF
│   └── サンプルノート02/
├── scripts/                      # 処理スクリプト
│   ├── make_pdf.py              # Python版PDF生成スクリプト
│   ├── make_pdf.sh              # Bash版PDF生成スクリプト
│   └── create_sample_images.py  # サンプル画像生成スクリプト
├── requirements.txt             # Python依存関係
└── README.md                    # このファイル
```

## 🛠️ 機能

### 現在実装済み
- ✅ 画像ファイルの一括PDF変換
- ✅ 複数の画像形式対応（JPG, PNG, HEIC等）
- ✅ ファイル名の自然順序ソート
- ✅ 既存PDFの自動バックアップ
- ✅ エラーハンドリング

### 今後の予定
- 🔄 OCR処理による検索可能PDF生成
- 🔄 バッチ処理スクリプト
- 🔄 クラウドOCR連携

## 📸 対応画像形式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- HEIC (.heic)
- TIFF (.tiff)
- BMP (.bmp)

## 🎯 使用方法の詳細

### 画像の準備
1. iPhoneでノートを撮影
2. 1冊ごとにフォルダに整理
3. ファイル名は連番（例：IMG_0001.jpg, IMG_0002.jpg）

### PDF生成
```bash
# 基本的な変換
python scripts/make_pdf.py /path/to/notebook/folder

# オプション付き
python scripts/make_pdf.py /path/to/notebook/folder \
    --output カスタム名.pdf \
    --verbose
```

## 📋 トラブルシューティング

### よくある問題

**Q: "img2pdfが見つかりません"エラーが出る**
```bash
pip install img2pdf
```

**Q: 画像ファイルが読み込めない**
- ファイル形式が対応していない
- ファイルが破損している
- ファイル名に特殊文字が含まれている

**Q: PDFが生成されない**
- ディレクトリに書き込み権限があるか確認
- 十分なディスク容量があるか確認

## 📞 サポート

詳細な仕様については `plan.md` を参照してください。

## 📄 ライセンス

このプロジェクトは個人利用を目的としています。
