# 2026-04-09 stale-then-fresh 関数化メモ

## 目的

「先に古いデータを返して画面を出し、あとで最新に差し替える」挙動を関数として再利用しやすくする。

## 追加した試験HTML

- `api-stale-then-fresh-demo.html`

## 関数の形

`staleThenFresh(options)` は以下の流れ:

1. 初回fetch（指数バックオフ付き）
2. `onInitial(initial)` を即呼び出し（古い可能性があるデータを先に表示）
3. `preparingNext=true` の場合だけ、予測待機して再fetch
4. `lastCollectAt` 変化で `updated` として解決
5. 変化しない場合は3秒再試行（最大10回）

返り値は Promise で `{ initial, updated }` を返す。
`updated` は取れないケースがあるので `null` を許容する。

## 補足

- 初回チェックは `FIRST_CHECK_RATIO=0.8` で前倒し
- `preparingNext=false` なら更新待機せず即終了
