#!/usr/bin/env python3
"""
手書きノート永久保存プロジェクト - PDF生成スクリプト（Python版）
画像ファイルを1つのPDFにまとめる機能を提供
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import img2pdf

def get_image_files(directory):
    """指定されたディレクトリから画像ファイルを取得"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.tiff', '.bmp'}
    image_files = []
    
    for file_path in Path(directory).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    # ファイル名でソート（自然順序）
    image_files.sort(key=lambda x: x.name)
    return image_files

def validate_images(image_files):
    """画像ファイルの妥当性をチェック"""
    valid_images = []
    invalid_files = []
    
    for image_file in image_files:
        try:
            with Image.open(image_file) as img:
                # 画像が開けるかチェック
                img.verify()
                valid_images.append(image_file)
        except Exception as e:
            print(f"警告: {image_file.name} を読み込めませんでした: {e}")
            invalid_files.append(image_file)
    
    return valid_images, invalid_files

def create_pdf_from_images(image_files, output_path):
    """画像ファイルからPDFを作成"""
    try:
        # 画像ファイルを絶対パスに変換
        image_paths = [str(img.resolve()) for img in image_files]
        
        # PDF生成
        with open(output_path, 'wb') as f:
            f.write(img2pdf.convert(image_paths))
        
        return True
    except Exception as e:
        print(f"エラー: PDF生成に失敗しました: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='画像ファイルを1つのPDFにまとめる',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python make_pdf.py ../Notebooks/ノート01
  python make_pdf.py ../Notebooks/ノート01 --output custom_name.pdf
        """
    )
    
    parser.add_argument('input_dir', help='画像ファイルが格納されたディレクトリ')
    parser.add_argument('--output', '-o', help='出力PDFファイル名（省略時は自動生成）')
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細な出力')
    
    args = parser.parse_args()
    
    # 入力ディレクトリの確認
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"エラー: ディレクトリ '{input_path}' が見つかりません")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"エラー: '{input_path}' はディレクトリではありません")
        sys.exit(1)
    
    notebook_name = input_path.name
    
    # 画像ファイルを取得
    image_files = get_image_files(input_path)
    if not image_files:
        print(f"エラー: '{input_path}' に画像ファイルが見つかりません")
        print("対応形式: .jpg, .jpeg, .png, .heic, .tiff, .bmp")
        sys.exit(1)
    
    if args.verbose:
        print(f"見つかった画像ファイル数: {len(image_files)}")
        for img in image_files:
            print(f"  - {img.name}")
    
    # 画像ファイルの妥当性をチェック
    valid_images, invalid_files = validate_images(image_files)
    
    if invalid_files:
        print(f"警告: {len(invalid_files)}個のファイルをスキップしました")
        if args.verbose:
            for img in invalid_files:
                print(f"  - {img.name}")
    
    if not valid_images:
        print("エラー: 有効な画像ファイルが見つかりませんでした")
        sys.exit(1)
    
    # 出力ファイル名を決定
    if args.output:
        output_path = input_path / args.output
    else:
        output_path = input_path / f"{notebook_name}.pdf"
    
    # 既存ファイルのバックアップ
    if output_path.exists():
        backup_path = output_path.with_suffix(f'.backup.{Path().cwd().name}.pdf')
        print(f"既存のPDFファイルをバックアップ: {backup_path}")
        output_path.rename(backup_path)
    
    print(f"処理開始: {notebook_name}")
    print(f"有効な画像ファイル数: {len(valid_images)}")
    print(f"出力先: {output_path}")
    
    # PDF生成
    if create_pdf_from_images(valid_images, output_path):
        # 生成されたファイルの情報を表示
        file_size = output_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ PDF生成完了!")
        print(f"   ファイル: {output_path}")
        print(f"   サイズ: {file_size_mb:.2f} MB")
        print(f"   ページ数: {len(valid_images)}")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
