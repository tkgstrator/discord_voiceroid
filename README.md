# 導入方法

## voiceroid_daemon

[voiceroid_daemon](https://github.com/Nkyoku/voiceroid_daemon/releases/tag/v2.0)をダウンロードして`VoiceroidDaemon.exe`を起動する

また、インストール済みの試用版でない VoiceroidEditor を起動する。

- [システムの設定](http://127.0.0.1:8080/Home/SystemSetting)をひらき、「システムの設定」から「起動中の VOICEROID2 エディタから取得する」をクリックして認証コードのシード値を取得する。
- [話者の設定](http://127.0.0.1:8080/Home/SpeakerSetting)をひらき、ボイスライブラリと話者を設定する。
- [動作確認用 URL](http://127.0.0.1:8080/api/speechtext/%E8%AA%8D%E8%A8%BC%E7%A2%BA%E8%AA%8D%E3%81%97%E3%81%9F%E3%81%A7)をひらいて VOICEROID2 の音声が流れたら成功。

## discord_voiceroid

`config.json`を作成し Bot の token と通話に参加したい voice_channel_id を設定する。

```json
{
  "token": "XXXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
  "voice_channel_id": 000000000000000000
}
```
