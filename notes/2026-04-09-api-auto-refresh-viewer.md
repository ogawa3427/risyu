# 2026-04-09 API自動更新ビューワー実装メモ

## 追加で確定した `/api` レスポンス解釈

- `reason`: `cached` / `refreshing_in_background` / `initializing`
- `preparingNext=true` は、バックグラウンド更新中または起動済みを示す
- `currentCollectStartedAt`:
  - `null` ならまだ実際のスクレイピング開始前（invoke直後など）
  - ISO8601文字列ならスクレイピング実行中
- `lastCollectAt` は差し替え判定キーとして使える
- `rows[0]` はメタ行 (`[日付文字列, valid|test]`)
- `rows[1]` はヘッダー行
- `rows[2...]` はデータ行

## 次回更新予測ロジック

- 成功履歴 (`recentRefreshes.success===true`) の先頭5件平均を使う
- 平均が取れない場合は `15000ms`
- `currentCollectStartedAt` がある場合:
  - `startedAt + avgDuration`
- ない場合:
  - `now + avgDuration + 3000ms`（コールドスタート余裕）
- 待機時間は `max(predictedFinishAt - now, 1000ms)`

## 自動更新ループ仕様

- 予測待機後に `/api` 再fetch
- `lastCollectAt` が変われば表示更新
- 変わらなければ3秒ごとに最大10回再試行
- `preparingNext=false` になったら自動更新停止
- fetch失敗時は指数バックオフ（1s,2s,4s...最大30s）

