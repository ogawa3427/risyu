# 2026-04-09 サーバー/クライアント遷移可視化メモ

`api-viewer.html` にリアルタイム遷移可視化を追加した。

## サーバー状態（推定）

`/api` 応答から以下の優先で判定:

- `reason=initializing` -> `booting`（uninitiated / initializing を統合表示）
- `reason=cached && preparingNext=false && currentCollectStartedAt=null` -> `fresh`
- `reason=refreshing_in_background && preparingNext=true && currentCollectStartedAt=null` -> `stale(first)`
- `reason=refreshing_in_background && preparingNext=true && currentCollectStartedAt!=null` -> `refreshing`

注: `uninitiated` と `initializing` はレスポンスだけで厳密分離しづらいので統合ノード化。

## クライアント状態

- `initial_fetch`
- `waiting_prediction`
- `predicted_check`
- `retrying`
- `stopped`

内部遷移:

- 初回/手動取得 -> `initial_fetch`
- 予測時刻待機 -> `waiting_prediction`
- 予測時刻到達で再fetch -> `predicted_check`
- 未更新時 3秒再試行中 -> `retrying`
- `preparingNext=false` または打ち切り -> `stopped`

## 既存更新ロジックとの関係

- 初回の予測チェックは `FIRST_CHECK_RATIO=0.8` で前倒し
- 未更新なら `CHECK_RETRY_DELAY_MS=3000` で最大 `MAX_CHECK_RETRY=10`
- fetch失敗時指数バックオフ（最大30秒）
