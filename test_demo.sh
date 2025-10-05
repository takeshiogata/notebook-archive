#!/bin/bash

# 手書きノート永久保存プロジェクト - デモスクリプト
# 画像ファイルをPDFに変換する機能のデモンストレーション

echo "📘 手書きノート永久保存プロジェクト - デモ"
echo "=============================================="
echo

# 仮想環境をアクティベート
if [ -f "venv/bin/activate" ]; then
    echo "✅ 仮想環境をアクティベート中..."
    source venv/bin/activate
else
    echo "❌ 仮想環境が見つかりません。先に 'python3 -m venv venv' を実行してください"
    exit 1
fi

echo
echo "📸 サンプル画像の生成..."
python scripts/create_sample_images.py

echo
echo "🔧 Python版スクリプトのテスト..."
python scripts/make_pdf.py Notebooks/サンプルノート01 --verbose

echo
echo "🔧 Bash版スクリプトのテスト..."
./scripts/make_pdf.sh Notebooks/サンプルノート02

echo
echo "📊 生成されたファイルの確認..."
echo "Notebooks/サンプルノート01/:"
ls -lh Notebooks/サンプルノート01/

echo
echo "Notebooks/サンプルノート02/:"
ls -lh Notebooks/サンプルノート02/

echo
echo "🎉 デモ完了!"
echo "生成されたPDFファイルを確認してください。"
echo "実際の手書きノートの画像ファイルを同じようにフォルダに配置して、"
echo "以下のコマンドでPDFに変換できます："
echo
echo "  python scripts/make_pdf.py <ノートフォルダパス>"
echo "  ./scripts/make_pdf.sh <ノートフォルダパス>"
