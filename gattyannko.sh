#!/bin/bash

# ディレクトリ内の各ファイルに対してループ
for file in togo_csvs/*; do
    # ファイル名から "risyu" と ".csv" を取り除く
    modified_filename=$(basename "$file" .csv | sed 's/risyu//')

    # awkを使用して各行の先頭に変更したファイル名を追加
    awk -v fname="$modified_filename" '{print fname "," $0}' "$file"
done
