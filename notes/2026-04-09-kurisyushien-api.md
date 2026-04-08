# kurisyushien API メモ

- 確認日: 2026-04-09
- エンドポイント: `https://kurisyushien.org/api`
- `curl` 実行時の応答例:

```json
{
  "ok": true,
  "reason": "initializing",
  "preparingNext": true,
  "message": "initial refresh started; retry after a few seconds"
}
```

- 補足: ルートの `https://kurisyushien.org` はこの環境からだと `AccessDenied` が返るが、`/api` は応答する。
