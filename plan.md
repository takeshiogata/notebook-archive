以下は、これまでの検討内容と「手書きノート永久保存プロジェクト」の仕様を整理した **Markdown仕様書** です。
将来的にREADMEや設計書としても利用できる構成になっています。

---

# 📘 手書きノート永久保存プロジェクト仕様書

## 概要

150冊ほどの手書きB6ノート（各40ページ程度）を、
**iPhoneで撮影 → OCR処理 → テキスト検索可能なPDFとして保存** するプロジェクト。
長期保存と将来の再利用（AIによる検索・解析）を目的とする。

---

## 🎯 プロジェクト目標

| 項目    | 内容                           |
| ----- | ---------------------------- |
| 主目的   | 手書きノートをデジタル化して検索可能にする        |
| 保存形式  | 1冊＝1ファイルの検索可能PDF（画像＋OCRテキスト） |
| 処理方式  | ローカルOCRを基本、クラウドOCRを補助的に利用    |
| 将来対応  | 新しいOCR技術登場時に再処理可能な構成を維持      |
| データ構成 | フォルダ単位でノートを管理（再処理しやすく）       |

---

## 📸 入力データ仕様

| 項目     | 内容                                            |
| ------ | --------------------------------------------- |
| 入力媒体   | 手書きノート（B6サイズ）                                 |
| 撮影方法   | iPhone 17 カメラ（非破壊スキャン）                        |
| 撮影ファイル | JPEG / HEIC 形式（1冊ごとにフォルダ分け）                   |
| 例      | `Notebooks/ノート01/IMG_0001.jpg … IMG_0040.jpg` |

---

## 🧰 使用ツールと環境

| カテゴリ      | ツール / ライブラリ                                            | 用途                            |
| --------- | ------------------------------------------------------ | ----------------------------- |
| OCR（ローカル） | **Tesseract + ocrmypdf**                               | 無料・オープンソースOCR、PDF内に透明テキスト埋め込み |
| OCR（クラウド） | **Google Document AI**（またはAzure Document Intelligence） | 手書き・図表含む高精度OCR、必要箇所のみ補助的に利用   |
| PDF生成     | **img2pdf / ImageMagick / プレビュー.app**                  | 画像を結合して1冊のPDFを生成              |
| OS        | macOS (brew + Python3 環境)                              | 自動処理・スクリプト実行環境                |

---

## ⚙️ 処理フロー

### ① 撮影・転送

* iPhoneでノートを撮影（照明・傾き・影を整える）
* 1冊ごとにフォルダにまとめ、MacへAirDropまたはiCloud転送

### ② PDF結合（シェルスクリプト）

```bash
img2pdf "$INPUT_DIR"/*.jpg -o "$OUTPUT_PDF"
```

### ③ ローカルOCR付与

```bash
ocrmypdf --language jpn+eng --deskew --rotate-pages "$OUTPUT_PDF" "$OUTPUT_OCR"
```

### ④ クラウドOCR補助（必要に応じて）

```bash
python ocr_cloud.py Notebooks/ノート01_ocr.pdf
```

### ⑤ 保存・バックアップ

* `ノート01_ocr.pdf` … 検索可能PDF（画像＋OCRテキスト）
* `ノート01_raw.pdf` … OCR未処理の「生」PDF（再処理用）
* `ノート01_text.json` … クラウドOCRテキストデータ（AI解析用）

---

## 🧠 クラウドOCR利用の方針

| 項目     | 内容                                    |
| ------ | ------------------------------------- |
| 利用目的   | 図や特殊記号を含むページの高精度再処理                   |
| コスト目安  | 約 $1.5 / 1,000ページ（Google Document AI） |
| 処理方式   | 手動 or 信頼度スコアによる再処理スクリプト               |
| プライバシー | 手書きノート内容を外部送信するため限定利用                 |

---

## 📂 フォルダ構成（推奨）

```
Notebooks/
├─ ノート01/
│   ├─ IMG_0001.jpg
│   ├─ IMG_0002.jpg
│   ├─ ...
│   ├─ ノート01.pdf             ← 結合画像PDF
│   ├─ ノート01_ocr.pdf         ← 検索可能PDF
│   ├─ ノート01_text.json       ← クラウドOCRテキスト
│   └─ meta.yaml                ← メモやタグ等（任意）
├─ ノート02/
│   ├─ ...
└─ scripts/
    ├─ make_pdf.sh
    ├─ ocr_cloud.py
    └─ batch_run.sh
```

---

## 🧩 自動処理スクリプト概要

### make_pdf.sh

1冊フォルダを引数に受け取り、画像→PDF→OCR済PDFを生成。

```bash
ocrmypdf --language jpn+eng --deskew --rotate-pages "$OUTPUT_PDF" "$OUTPUT_OCR"
```

### ocr_cloud.py

Google Document AI APIを呼び出し、JSON形式でテキスト抽出。

### batch_run.sh

全ノートフォルダを順次処理するループスクリプト。

```bash
for d in Notebooks/*; do
  if [ -d "$d" ]; then
    sh scripts/make_pdf.sh "$d"
  fi
done
```

---

## 🔒 データ保全と再処理方針

* **画像付きPDF**を「一次データ」として必ず残す（再OCR可能にする）。
* OCR結果テキストは別途保存（再解析・AI連携用）。
* PDFにはOCRテキストレイヤーを埋め込み → macOS / iPhone上でも検索可能。
* クラウドOCRは部分利用（品質向上 or AI分析時のみ）。

---

## 💡 今後の発展

* AI（LLM）によるノート検索・要約（Document AI → RAG構築）
* OCR品質ログの自動収集と再処理優先順位付け
* JSONメタデータ（タグ・テーマ）による知識ベース化

---

## ✅ 現時点の結論

* メイン形式：**検索可能PDF（画像＋OCRテキスト）**
* 基盤OCR：**Tesseract + ocrmypdf（ローカル処理）**
* 補助OCR：**Google Document AI（必要部分のみ）**
* 保存方針：**非破壊撮影・1冊＝1フォルダ・再処理可能設計**
