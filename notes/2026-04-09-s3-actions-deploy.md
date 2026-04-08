# S3デプロイ用 Actions メモ

- 追加したワークフロー: `.github/workflows/deploy-s3.yml`
- トリガー:
  - `main` への push
  - 変更対象が `index.html` / `static/favicon.ico` / ワークフロー自身
  - 手動実行 (`workflow_dispatch`)
- 必要な Secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `S3_BUCKET`
- デプロイ内容:
  - `index.html` を `s3://<bucket>/index.html` へ
  - `static/favicon.ico` を `s3://<bucket>/static/favicon.ico` へ
