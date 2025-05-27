# voice_chat.py デバッグガイド

## 問題の調査方法

「勝手に一人で話し始めて止まらない」問題を調査するために、以下のデバッグ機能を追加しました：

### 1. 音声レベル監視
- マイクからの音声レベルを監視し、一定の閾値以上の場合のみAIに送信
- 現在の閾値: `500` (調整可能)
- 音声レベルが低い場合は送信をスキップ

### 2. デバッグログ出力
以下の情報がコンソールに出力されます：
- `[DEBUG] Using microphone: [マイク名]` - 使用中のマイクデバイス
- `[DEBUG] Audio volume level: [数値]` - 約3秒ごとの音声レベル
- `[DEBUG] Sending audio chunk (volume: [数値])` - 音声データ送信時
- `[DEBUG] Audio too quiet, not sending (volume: [数値])` - 音声が小さすぎて送信しない場合
- `[DEBUG] Sending audio data to AI` - AIへの音声データ送信
- `[DEBUG] Waiting for AI response...` - AIからの応答待ち
- `[DEBUG] Received audio data from AI (length: [数値])` - AIからの音声データ受信
- `[DEBUG] AI text response: [テキスト]` - AIからのテキスト応答
- `[DEBUG] AI turn completed` - AIのターン完了

## 実行方法

```bash
python voice_chat.py --mode none
```

## 問題の特定方法

### 1. 音声フィードバックループの確認
以下のログパターンが連続して出力される場合、フィードバックループが発生している可能性があります：
```
[DEBUG] Sending audio data to AI
[DEBUG] Received audio data from AI (length: XXXX)
[DEBUG] Sending audio data to AI
[DEBUG] Received audio data from AI (length: XXXX)
```

### 2. 環境音の誤認識確認
静かな環境でも以下のログが頻繁に出力される場合、環境音を誤認識している可能性があります：
```
[DEBUG] Sending audio chunk (volume: XXX)
```

### 3. マイクの感度確認
`[DEBUG] Audio volume level:` の値を確認して、適切な閾値を設定してください：
- 通常の環境音: 100-300程度
- 話し声: 1000-5000程度
- 現在の閾値: 500

## 対処方法

### 1. 音声閾値の調整
`voice_chat.py` の193行目の閾値を調整：
```python
if volume > 500:  # この値を調整
```

### 2. マイクの変更
別のマイクデバイスを使用する場合は、デバッグログでマイク名を確認し、必要に応じてコードを修正

### 3. 音声フィードバック対策
- ヘッドフォンを使用してスピーカーからの音をマイクが拾わないようにする
- マイクとスピーカーの距離を離す
- マイクの感度を下げる

### 4. 一時的な対処
問題が解決するまで、以下の方法で音声入力を無効化できます：

`voice_chat.py` の242行目付近をコメントアウト：
```python
# tg.create_task(self.listen_audio())  # 音声入力を無効化
```

## 追加の調査項目

1. **使用中のマイクデバイス**: ログで確認
2. **音声レベルの変動**: 静寂時と話し声時の数値差
3. **AIの応答パターン**: 連続して応答が来るかどうか
4. **環境音の影響**: 静かな環境での動作確認

## 元に戻す方法

デバッグ機能を削除して元のコードに戻したい場合は、gitを使用してリセットするか、デバッグログの出力部分を削除してください。
