# voice_chat.py クラス概要

## AudioLoop クラス

### 概要
`AudioLoop` クラスは、Google Gemini APIを使用したリアルタイム音声・映像チャットシステムのメインクラスです。音声の録音・再生、映像の取得、テキスト入力を非同期で処理し、AIとのリアルタイム対話を実現します。

### 初期化パラメータ
- `video_mode: str` - 映像モード（デフォルト: "none"）
  - `"camera"`: Webカメラからの映像を使用
  - `"screen"`: スクリーンキャプチャを使用  
  - `"none"`: 映像なし

### 主要属性
- `video_mode`: 映像取得モード
- `audio_in_queue`: 受信音声データのキュー
- `out_queue`: 送信データのキュー
- `session`: Gemini Live APIセッション
- `send_text_task`: テキスト送信タスク
- `receive_audio_task`: 音声受信タスク
- `play_audio_task`: 音声再生タスク

### 主要メソッド

#### `async def send_text(self)`
- ユーザーからのテキスト入力を受け付け、AIに送信
- "q" 入力で終了

#### `def _get_frame(self, cap)`
- Webカメラからフレームを取得し、JPEG形式でエンコード
- BGR→RGB変換を行い、1024x1024にリサイズ
- Base64エンコードして返却

#### `async def get_frames(self)`
- Webカメラから継続的にフレームを取得
- 1秒間隔でフレームを出力キューに送信

#### `def _get_screen(self)`
- スクリーンキャプチャを取得し、JPEG形式でエンコード
- Base64エンコードして返却

#### `async def get_screen(self)`
- 継続的にスクリーンキャプチャを取得
- 1秒間隔でフレームを出力キューに送信

#### `async def send_realtime(self)`
- 出力キューからデータを取得し、AIセッションに送信

#### `async def listen_audio(self)`
- マイクから音声を録音
- PCM形式で出力キューに送信

#### `async def receive_audio(self)`
- AIからの音声レスポンスを受信
- テキストレスポンスがある場合は画面に出力
- 割り込み時は音声キューをクリア

#### `async def play_audio(self)`
- 受信した音声データを再生

#### `async def run(self)`
- メインの実行メソッド
- 各種タスクを並行実行
- エラーハンドリングとクリーンアップを実行

### 技術仕様

#### 音声設定
- フォーマット: 16-bit PCM
- チャンネル: モノラル
- 送信サンプルレート: 16kHz
- 受信サンプルレート: 24kHz
- チャンクサイズ: 1024

#### 使用ライブラリ
- `google.genai`: Gemini API
- `pyaudio`: 音声入出力
- `opencv-python`: 映像処理
- `PIL`: 画像処理
- `mss`: スクリーンキャプチャ
- `asyncio`: 非同期処理

#### AIモデル
- `models/gemini-2.5-flash-preview-native-audio-dialog`
- 音声応答モダリティ
- 中解像度メディア
- Leda音声設定
- コンテキストウィンドウ圧縮機能

### 使用方法
```bash
python voice_chat.py --mode [camera|screen|none]
```

### 特徴
- リアルタイム音声対話
- Webカメラまたはスクリーンキャプチャによる映像入力
- 非同期処理による高いレスポンス性
- 割り込み機能対応
- エラーハンドリング
