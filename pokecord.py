import discord
import random
import os
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#環境変数をファイルから読み込み
with open('.env') as f:
    for line in f:
        # 空行やコメントをスキップ
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value


BOT_TOKEN = os.environ["BOT_TOKEN"]

# ポケモンとバトルスタイルの対応表 (辞書型を使用)
pokemon_data = {
    "アタック型": [
        "ゲッコウガ",
        "ルカリオ",
        "ザシアン",
        "リザードン",
        "ガブリアス",
    ],  # 例として追加
    "ディフェンス型": [
        "カビゴン",
        "バリヤード",
        "レジスチル",
        "ナットレイ",
        "ランドロス",
    ],  # 例として追加
    "スピード型": [
        "ゼラオラ",
        "ゲンガー",
        "ニンフィア",
        "ミミッキュ",
        "シャドウ",
    ],  # 例として追加
    "バランス型": [
        "カメックス",
        "バンギラス",
        "ブラッキー",
        "エルフーン",
        "ミュウツー",
    ],  # 例として追加
    "サポート型": [
        "エルレイド",
        "キノガッサ",
        "ヤドラン",
        "マリルリ",
        "オーロンゲ",
    ],  # 例として追加
}

roles = list(pokemon_data.keys())  # バトルスタイルのリスト

# 各バトルスタイル色の定義
# 色は通常の16進数のカラーコードの先頭に0xをつけることで指定できる
COLOR_ATTACK = 0xF46A4E  # アタック型
COLOR_DEFENSE = 0x91FD32  # ディフェンス型
COLOR_SPEED = 0x48BDCC  # スピード型
COLOR_BALANCE = 0xD374D4  # バランス型
COLOR_SUPPORT = 0xFDFF3A  # サポート型

"""
Embedメッセージの説明
Embedメッセージは、botのみが使える形式のメッセージです。
画像も表示できるので工夫すればポケモンの画像も表示できます。

title=f"任意のタイトルが入ります",
description=f"任意の説明文が入ります",
color=色を16進数で指定します
"""


# 起動時の処理
@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")
    await tree.sync()  # スラッシュコマンドを同期
    print("スラッシュコマンドを同期しました")


"""
@tree.command(name="test",description="ここに入力した文章が/testと入力した際の説明文になります")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)
    
    send_messageの最後にephemeral=Trueを追加することでコマンドを入力した人だけが結果を見ることができ、他の人には入力したコマンドも結果も見えません。
"""


# 完全ランダム用のコマンド
@tree.command(
    name="ランダム", description="バトルスタイルとポケモンをランダムに選択します"
)
async def random_command(interaction: discord.Interaction):
    """バトルスタイルとポケモンをランダムに選択するスラッシュコマンド,random"""
    try:
        selected_role = random.choice(roles)
        selected_pokemon = random.choice(pokemon_data[selected_role])

        # 選ばれたバトルスタイルによって色を変える
        if selected_role == "アタック型":
            color = COLOR_ATTACK
        elif selected_role == "ディフェンス型":
            color = COLOR_DEFENSE
        elif selected_role == "スピード型":
            color = COLOR_SPEED
        elif selected_role == "バランス型":
            color = COLOR_BALANCE
        elif selected_role == "サポート型":
            color = COLOR_SUPPORT
        else:
            color = 0x000000  # もしバトルスタイルが登録されていない場合は黒色にする

        # Embedメッセージ、botのみが使える形式のメッセージ。画像も表示できるので工夫すればポケモンの画像も表示できる
        embed = discord.Embed(
            title=f"{selected_role}", description=f"{selected_pokemon}", color=color
        )

        if selected_role == "アタック型":
            embed.set_thumbnail(
                url="https://img.icons8.com/?size=100&id=5336&format=png&color=000000"
            )
        elif selected_role == "ディフェンス型":
            embed.set_thumbnail(
                url="https://img.icons8.com/?size=100&id=qti4884q4Rcz&format=png&color=000000"
            )
        elif selected_role == "スピード型":
            embed.set_thumbnail(
                url="https://img.icons8.com/?size=100&id=41152&format=png&color=000000"
            )
        elif selected_role == "バランス型":
            embed.set_thumbnail(
                url="https://img.icons8.com/?size=100&id=43399&format=png&color=000000"
            )
        elif selected_role == "サポート型":
            embed.set_thumbnail(
                url="https://img.icons8.com/?size=100&id=5359&format=png&color=000000"
            )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# アタック型のポケモンを選択するコマンド
@tree.command(name="アタック型", description="アタック型のポケモンを選択します(attack)")
async def attack_command(interaction: discord.Interaction):
    """アタック型のポケモンを選択するスラッシュコマンド,attack"""
    try:
        selected_pokemon = random.choice(pokemon_data["アタック型"])
        embed = discord.Embed(
            title=f"アタック型", description=f"{selected_pokemon}", color=COLOR_ATTACK
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# ディフェンス型のポケモンを選択するコマンド
@tree.command(
    name="ディフェンス型", description="ディフェンス型のポケモンを選択します(defense)"
)
async def defense_command(interaction: discord.Interaction):
    """ディフェンス型のポケモンを選択するスラッシュコマンド"""
    try:
        selected_pokemon = random.choice(pokemon_data["ディフェンス型"])
        embed = discord.Embed(
            title=f"ディフェンス型",
            description=f"{selected_pokemon}",
            color=COLOR_DEFENSE,
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# スピード型のポケモンを選択するコマンド
@tree.command(name="スピード型", description="スピード型のポケモンを選択します(speed)")
async def speed_command(interaction: discord.Interaction):
    """スピード型のポケモンを選択するスラッシュコマンド"""
    try:
        selected_pokemon = random.choice(pokemon_data["スピード型"])
        embed = discord.Embed(
            title=f"スピード型", description=f"{selected_pokemon}", color=COLOR_SPEED
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# バランス型のポケモンを選択するコマンド
@tree.command(
    name="バランス型", description="バランス型のポケモンを選択します(balance)"
)
async def balance_command(interaction: discord.Interaction):
    """バランス型のポケモンを選択するスラッシュコマンド"""
    try:
        selected_pokemon = random.choice(pokemon_data["バランス型"])
        embed = discord.Embed(
            title=f"バランス型", description=f"{selected_pokemon}", color=COLOR_BALANCE
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# サポート型のポケモンを選択するコマンド
@tree.command(
    name="サポート型", description="サポート型のポケモンを選択します(support)"
)
async def support_command(interaction: discord.Interaction):
    """サポート型のポケモンを選択するスラッシュコマンド"""
    try:
        selected_pokemon = random.choice(pokemon_data["サポート型"])
        embed = discord.Embed(
            title=f"サポート型", description=f"{selected_pokemon}", color=COLOR_SUPPORT
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}")


# ボイスチャットの参加者から5vs5のチームを作成するコマンド
# ユーザー名表示を表示名からメンションに変更したい場合は、member.display_nameからmember.mentionに変更する。逆もしかり
@tree.command(
    name="vcチーム", description="ボイスチャットの参加者から均等に2チームを作成します"
)
async def vc_team_command(interaction: discord.Interaction):
    """ボイスチャットの参加者からできる限り均等な2チームを作成するスラッシュコマンド"""

    # ボイスチャンネルに参加しているか確認
    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message(
            "ボイスチャンネルに参加していません。", ephemeral=True
        )
        return

    # ボイスチャンネルに参加しているメンバーのリストを取得
    members = interaction.user.voice.channel.members

    # メンバー数が2人未満の場合、チームを作成できないためエラーを表示
    if len(members) < 2:
        await interaction.response.send_message(
            "ボイスチャンネルに2人以上参加している必要があります。", ephemeral=True
        )
        return

    # メンバーをランダムに並び替える
    random.shuffle(members)

    # メンバーリストを半分に分ける
    midpoint = (len(members) + 1) // 2  # 奇数の場合は片方が1人多くなる
    team1 = members[:midpoint]
    team2 = members[midpoint:]

    # チーム1のメンバーを表示
    team1_text = "チーム1:\n"
    for i, member in enumerate(team1, 1):
        team1_text += f"{i}. {member.display_name}\n"

    # チーム2のメンバーを表示
    team2_text = "チーム2:\n"
    for i, member in enumerate(team2, 1):
        team2_text += f"{i}. {member.display_name}\n"

    # Embedメッセージを作成
    embed = discord.Embed(
        title="チーム分け", description=f"{team1_text}\n{team2_text}", color=0x17A168
    )

    # Embedメッセージを送信
    await interaction.response.send_message(embed=embed)


# チーム数を指定してメンバーをランダムに振り分けるコマンド
@tree.command(
    name="チーム分け",
    description="ボイスチャットの参加者を指定したチーム数に振り分けます",
)
async def split_teams(interaction: discord.Interaction, team_count: int):
    """指定したチーム数でボイスチャット参加者をランダムに分ける"""

    # ボイスチャンネルに参加しているか確認
    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message(
            "ボイスチャンネルに参加していません。", ephemeral=True
        )
        return

    # ボイスチャンネルの参加メンバーを取得
    members = interaction.user.voice.channel.members

    # メンバー数がチーム数より少ない場合はエラーを表示
    if len(members) < team_count:
        await interaction.response.send_message(
            "チーム数が参加者数を上回っています。", ephemeral=True
        )
        return

    # メンバーをランダムにシャッフルしてチームに分ける
    random.shuffle(members)
    teams = [[] for _ in range(team_count)]
    for i, member in enumerate(members):
        teams[i % team_count].append(member)

    # 各チームをテキストに変換
    result_text = ""
    for i, team in enumerate(teams):
        team_text = f"チーム{i + 1}:\n"
        for member in team:
            team_text += f"- {member.display_name}\n"
        result_text += f"{team_text}\n"

    # Embedメッセージを作成して送信
    embed = discord.Embed(
        title="チーム分け結果", description=result_text, color=0x17A168
    )
    await interaction.response.send_message(embed=embed)


# オンラインのメンバーから5人チームを作成するコマンド
@tree.command(
    name="オンラインチーム",
    description="コマンド実行チャンネルにアクセスできるオンラインメンバーをランダムにチーム分けします",
)
async def online_team(interaction: discord.Interaction, team_count: int):
    """コマンド実行チャンネルにアクセスできるオンラインメンバーを指定したチーム数に振り分ける"""

    # コマンド実行チャンネルにアクセス可能なオンラインメンバーを取得
    online_members = [member for member in interaction.channel.members if member.status == discord.Status.online and not member.bot]

    # メンバー数がチーム数より少ない場合はエラーを表示
    if len(online_members) < team_count:
        await interaction.response.send_message(
            "チーム数がオンラインメンバー数を上回っています。", ephemeral=True
        )
        return

    # メンバーをランダムにシャッフルしてチームに分ける
    random.shuffle(online_members)
    teams = [[] for _ in range(team_count)]
    for i, member in enumerate(online_members):
        teams[i % team_count].append(member)

    # 各チームをテキストに変換
    team_text = ""
    for i, team in enumerate(teams):
        team_text += f"チーム{i + 1}:\n"
        for member in team:
            team_text += f"- {member.display_name}\n"

    # Embedメッセージを作成して送信
    embed = discord.Embed(
        title="ランダムチーム", description=team_text, color=0x17A168
    )
    await interaction.response.send_message(embed=embed)


# コマンドのリストを表示するコマンド
@tree.command(name="help", description="ヘルプを表示します")
async def help_command(interaction: discord.Interaction):
    """ヘルプを表示するスラッシュコマンド"""

    help_embed = discord.Embed(
        title="ヘルプ",
        description="/(スラッシュ)の後にコマンド名を入力することでコマンドを実行できます",
        color=0x17A168,
    )
    help_embed.set_thumbnail(
        url="https://img.icons8.com/?size=100&id=6644&format=png&color=000000"
    )

    # チーム分け関連のコマンド
    help_embed.add_field(
        name="🔹 チーム分けコマンド",
        value=(
            "**/vcチーム**\n"
            "ボイスチャットの参加者から均等に2チームを作成します\n\n"
            "**/チーム分け**\n"
            "ボイスチャットの参加者を指定したチーム数に振り分けます\n\n"
            "**/オンラインチーム**\n"
            "現在オンラインのメンバーからランダムで5人のチームを作成します"
        ),
        inline=False,
    )

    # ランダムピック関連のコマンド
    help_embed.add_field(
        name="🔹 ランダムピックコマンド",
        value=(
            "**/ランダム**\n"
            "バトルスタイルとポケモンをランダムに選択します\n\n"
            "**/アタック型**\n"
            "アタック型のポケモンをランダムに選択します\n\n"
            "**/ディフェンス型**\n"
            "ディフェンス型のポケモンをランダムに選択します\n\n"
            "**/スピード型**\n"
            "スピード型のポケモンをランダムに選択します\n\n"
            "**/バランス型**\n"
            "バランス型のポケモンをランダムに選択します\n\n"
            "**/サポート型**\n"
            "サポート型のポケモンをランダムに選択します"
        ),
        inline=False,
    )

    help_embed.set_footer(
        text="made by udondon1478",
        icon_url="https://pbs.twimg.com/profile_images/1809495176894902272/TrVVuTPz_400x400.jpg",
    )

    await interaction.response.send_message(embed=help_embed, ephemeral=True)


client.run(BOT_TOKEN)
