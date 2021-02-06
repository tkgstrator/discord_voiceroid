import discord
import asyncio
import sys
import os
import json
import requests
import re
import zipfile
import shutil
from glob import glob
from datetime import datetime
from discord.ext import commands


def Log(str):  # ログ表示
    print(f'{datetime.now().strftime("%H:%M:%S")} {str}')


def FilePath(file):  # ファイルまでのパスを返す
    return f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/{file}"


def text2wav(text, id):  # テキストをWAVに変換
    url = f"http://127.0.0.1:8080/api/speechtext/{text}"
    res = requests.get(url)
    path = f"voices/{id}.wav"
    with open(path, "wb") as f:
        f.write(res.content)
    return path


def ffmpeg_download():
    filename = "ffmpeg-release-essentials.zip"
    url = f"https://www.gyan.dev/ffmpeg/builds/{filename}"
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename
    return False


def zip_extract(filename):
    target = "."
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target)


def json_build():
    with open("config.json", mode="w") as f:
        data = {
            "token": "XXXXXXXXXXXXXXXXXXXXXXXX.YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
            "voice_channel_id": 999999999999999999
        }
        json.dump(data, f, indent=4)


class VoiceroidBot():
    # クラス変数を定義
    token = None
    voice_channel_id = None

    # 初期化
    def __init__(self):
        try:
            with open(FilePath("config.json"), mode="r") as f:  # 設定ファイルがある場合
                params = json.load(f)
                self.token = params["token"]
                self.voice_channel_id = params["voice_channel_id"]
                if "voices" not in os.listdir():
                    os.mkdir("voices")
            if "ffmpeg.exe" not in os.listdir():
                Log("Downloading ffmpeg")
                zip_extract(ffmpeg_download())
                target = glob('ffmpeg-*_build')[0]
                ffmpeg = f"{target}/bin/ffmpeg.exe"
                shutil.move(ffmpeg, ".")
                shutil.rmtree(target)
                os.remove("ffmpeg-release-essentials.zip")
        except FileNotFoundError:  # 設定ファイルがない場合
            Log("設定ファイルがありません")
            Log("設定ファイルを再生成しました")
            json_build()
            sys.exit(1)
        except json.decoder.JSONDecodeError:  # 設定ファイルのフォーマットがおかしい場合
            Log("設定ファイルのフォーマットが間違っています")
            Log("設定ファイルを再生成しました")
            json_build()
            sys.exit(1)
        except Exception as error:
            Log(f"不明なエラー {error}")
            sys.exit(1)

    def main(self):
        try:
            bot = commands.Bot(command_prefix="!")

            @ bot.event
            async def on_ready():
                Log("接続完了")

            @ bot.command()
            async def leave(ctx):
                server = ctx.message.guild.voice_client
                await server.disconnect()

            @ bot.event
            async def on_message(message):
                # bot自身のメッセージは何もしない
                if message.author.bot:
                    return

                # 通話から抜ける
                if message.content in ["bye", "leave"]:
                    voice_client = message.guild.voice_client
                    await voice_client.disconnect()
                    return

                # ユーザーidが含まれる場合ユーザー名に変換する
                pattern = r"<@!(?P<user_id>\d+)>"
                m = re.match(pattern, message.content)
                if m:
                    user_name = bot.get_user(int(m.group("user_id"))).name
                    message.content = re.sub(pattern, user_name, message.content)

                # 文字が長すぎると区切る
                max_length = 30
                if len(message.content) > max_length:
                    message.content = message.content[:max_length] + " 以下略"

                # 通話に参加
                voice_client = message.guild.voice_client
                if not voice_client:
                    voice_client = await bot.get_channel(self.voice_channel_id).connect()

                # 喋っている途中は待つ
                while voice_client.is_playing():
                    await asyncio.sleep(0.5)

                # テキストをwavファイルに変換してボイチャに流す
                source = discord.FFmpegPCMAudio(text2wav(message.content, self.voice_channel_id))
                voice_client.play(source)

            bot.run(self.token)
        except UnicodeDecodeError:
            Log("入力された音声が不正です")
        except discord.errors.HTTPException:
            Log("入力されたトークンまたはIDが不正です")
        except discord.errors.LoginFailure:
            Log("入力されたトークンまたはIDが不正です")
        except RuntimeError:
            Log("イベントを開始できませんでした")
        except Exception as error:
            Log("イベントを開始できませんでした")


if __name__ == "__main__":
    try:
        bot = VoiceroidBot()
        bot.main()
    except KeyboardInterrupt:
        Log("終了します")
    except Exception as error:
        Log("イベントを開始できませんでした")
