#!/bin/bash

# 手書きノート永久保存プロジェクト - PDF生成スクリプト
# 使用方法: ./make_pdf.sh <ノートフォルダパス>

set -e  # エラー時にスクリプトを停止

# 引数チェック
if [ $# -ne 1 ]; then
    echo "使用方法: $0 <ノートフォルダパス>"
    echo "例: $0 ../Notebooks/ノート01"
    exit 1
fi

INPUT_DIR="$1"
NOTEBOOK_NAME=$(basename "$INPUT_DIR")

# 入力ディレクトリの存在確認
if [ ! -d "$INPUT_DIR" ]; then
    echo "エラー: ディレクトリ '$INPUT_DIR' が見つかりません"
    exit 1
fi

# 画像ファイルの存在確認
IMAGE_COUNT=$(find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.heic" -o -iname "*.png" \) | wc -l)
if [ $IMAGE_COUNT -eq 0 ]; then
    echo "エラー: '$INPUT_DIR' に画像ファイルが見つかりません"
    exit 1
fi

echo "処理開始: $NOTEBOOK_NAME"
echo "画像ファイル数: $IMAGE_COUNT"

# 出力ファイル名を設定
OUTPUT_PDF="$INPUT_DIR/${NOTEBOOK_NAME}.pdf"

# 既存のPDFファイルがある場合はバックアップ
if [ -f "$OUTPUT_PDF" ]; then
    BACKUP_FILE="${OUTPUT_PDF}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "既存のPDFファイルをバックアップ: $BACKUP_FILE"
    mv "$OUTPUT_PDF" "$BACKUP_FILE"
fi

# Python版のスクリプトを使用してPDF生成
echo "PDF生成中..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 仮想環境をアクティベートしてPythonスクリプトを実行
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    python "$SCRIPT_DIR/make_pdf.py" "$INPUT_DIR" --output "$(basename "$OUTPUT_PDF")" || {
        echo "エラー: PDF生成に失敗しました"
        exit 1
    }
else
    echo "エラー: 仮想環境が見つかりません。先に 'python3 -m venv venv' を実行してください"
    exit 1
fi

# 生成されたPDFファイルの確認
if [ -f "$OUTPUT_PDF" ]; then
    PDF_SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    echo "✅ PDF生成完了: $OUTPUT_PDF"
    echo "   ファイルサイズ: $PDF_SIZE"
    echo "   ページ数: $IMAGE_COUNT"
else
    echo "エラー: PDFファイルが生成されませんでした"
    exit 1
fi

echo "処理完了: $NOTEBOOK_NAME"
