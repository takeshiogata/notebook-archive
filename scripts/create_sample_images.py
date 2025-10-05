#!/usr/bin/env python3
"""
手書きノート永久保存プロジェクト - サンプル画像生成スクリプト
テスト用のサンプル画像を作成して動作確認を行う
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_notebook(directory, notebook_name, page_count=5):
    """サンプルノートブックの画像ファイルを作成"""
    
    # ディレクトリを作成
    notebook_dir = Path(directory) / notebook_name
    notebook_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"サンプルノートブック作成: {notebook_name}")
    print(f"ページ数: {page_count}")
    print(f"保存先: {notebook_dir}")
    
    # 各ページの画像を作成
    for i in range(1, page_count + 1):
        # B6サイズに近いサイズ（182×128mm → 約515×363ピクセル @ 72DPI）
        # より高解像度で作成（実際のiPhone撮影を想定）
        width, height = 1030, 726  # 2倍の解像度
        
        # 白い背景の画像を作成
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # ページ番号を描画
        try:
            # システムフォントを使用（日本語対応）
            font_large = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", 48)
            font_small = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", 24)
        except:
            # フォールバック
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # ページタイトル
        title = f"ページ {i}"
        draw.text((50, 50), title, fill='black', font=font_large)
        
        # サンプルテキスト
        sample_texts = [
            "これは手書きノートのサンプルです。",
            "実際のノートでは手書きの文字や図表が含まれます。",
            "OCR処理により、これらの文字を検索可能にします。",
            "日本語と英語の混在テキストも処理できます。",
            "図や表、数式なども認識対象となります。"
        ]
        
        y_pos = 150
        for text in sample_texts:
            draw.text((50, y_pos), text, fill='black', font=font_small)
            y_pos += 40
        
        # サンプル図形を描画
        # 矩形
        draw.rectangle([50, y_pos, 200, y_pos + 50], outline='blue', width=2)
        draw.text((60, y_pos + 10), "図形例", fill='blue', font=font_small)
        
        # 円
        draw.ellipse([250, y_pos, 350, y_pos + 50], outline='red', width=2)
        draw.text((270, y_pos + 10), "円形", fill='red', font=font_small)
        
        # 線
        draw.line([(400, y_pos), (500, y_pos + 50)], fill='green', width=3)
        draw.text((510, y_pos + 10), "直線", fill='green', font=font_small)
        
        # ランダムな点を追加（手書き風の表現）
        for _ in range(20):
            x = random.randint(50, width - 50)
            y = random.randint(300, height - 100)
            draw.point([x, y], fill='gray')
        
        # ファイル名を生成（実際のiPhone撮影を想定）
        filename = f"IMG_{i:04d}.jpg"
        filepath = notebook_dir / filename
        
        # 画像を保存
        img.save(filepath, 'JPEG', quality=95)
        print(f"  作成: {filename}")
    
    print(f"✅ サンプルノートブック作成完了: {notebook_name}")
    return notebook_dir

def main():
    # プロジェクトルートディレクトリ
    project_root = Path(__file__).parent.parent
    
    # Notebooksディレクトリを作成
    notebooks_dir = project_root / "Notebooks"
    notebooks_dir.mkdir(exist_ok=True)
    
    # 複数のサンプルノートブックを作成
    sample_notebooks = [
        ("サンプルノート01", 3),
        ("サンプルノート02", 5),
        ("テストノート", 2)
    ]
    
    print("手書きノート永久保存プロジェクト - サンプル画像生成")
    print("=" * 50)
    
    for notebook_name, page_count in sample_notebooks:
        create_sample_notebook(notebooks_dir, notebook_name, page_count)
        print()
    
    print("🎉 すべてのサンプルノートブック作成完了!")
    print(f"保存場所: {notebooks_dir}")
    print()
    print("次のステップ:")
    print("1. Pythonスクリプト: python scripts/make_pdf.py Notebooks/サンプルノート01")
    print("2. Bashスクリプト: ./scripts/make_pdf.sh Notebooks/サンプルノート01")

if __name__ == '__main__':
    main()
