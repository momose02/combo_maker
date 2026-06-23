import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os

# ==========================================
# 1. UptimeRobot対策：常時起動用のダミーWebサーバー
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Combo Bot is Alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. Discord Botの設定
# ==========================================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class ComboMakerView(discord.ui.View):
    def __init__(self, memo: str = None):
        super().__init__(timeout=180)
        self.combo_parts = [] 
        self.memo = memo      

    def get_combo_string(self):
        return " ＞ ".join(self.combo_parts)

    # 【爆速コア処理】Discordに「ボタン受け取ったよ」と0秒で返しつつ、履歴を追記する
    async def add_part(self, interaction: discord.Interaction, text: str):
        self.combo_parts.append(text)
        
        # 1. まずDiscord側に「ボタン押下を検知した」と一瞬で応答（これでボタンの砂時計が消える）
        await interaction.response.defer(ephemeral=True)
        
        # 2. 本人にだけ、入力した履歴を光速でチャット欄に追記（これが体感ラグ0秒の秘密）
        await interaction.followup.send(f"➡️ **{text}** を入力中...", ephemeral=True)

    # ------------------------------------------
    # 3. 5行×5個のボタン配置
    # ------------------------------------------
    
    # 1行目：移動コマンド (row=0)
    @discord.ui.button(label="←左", style=discord.ButtonStyle.secondary, row=0)
    async def left(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "←左")
    @discord.ui.button(label="↙️左下", style=discord.ButtonStyle.secondary, row=0)
    async def down_left(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "↙️左下")
    @discord.ui.button(label="↓下", style=discord.ButtonStyle.secondary, row=0)
    async def down(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "↓下")
    @discord.ui.button(label="↘️右下", style=discord.ButtonStyle.secondary, row=0)
    async def down_right(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "↘️右下")
    @discord.ui.button(label="➡️右", style=discord.ButtonStyle.secondary, row=0)
    async def right(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "➡️右")

    # 2行目：通常技（パンチ）＆ ジャンプ系 (row=1)
    @discord.ui.button(label="小P", style=discord.ButtonStyle.primary, row=1)
    async def lp(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "小P")
    @discord.ui.button(label="中P", style=discord.ButtonStyle.primary, row=1)
    async def mp(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "中P")
    @discord.ui.button(label="大P", style=discord.ButtonStyle.primary, row=1)
    async def hp(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "大P")
    @discord.ui.button(label="前ジャンプ", style=discord.ButtonStyle.secondary, row=1)
    async def f_jump(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "前ジャンプ")
    @discord.ui.button(label="垂直ジャンプ", style=discord.ButtonStyle.secondary, row=1)
    async def v_jump(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "垂直ジャンプ")

    # 3行目：通常技（キック）＆ ステップ系 (row=2)
    @discord.ui.button(label="小K", style=discord.ButtonStyle.primary, row=2)
    async def lk(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "小K")
    @discord.ui.button(label="中K", style=discord.ButtonStyle.primary, row=2)
    async def mk(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "中K")
    @discord.ui.button(label="大K", style=discord.ButtonStyle.primary, row=2)
    async def hk(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "大K")
    @discord.ui.button(label="前ステップ", style=discord.ButtonStyle.secondary, row=2)
    async def f_step(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "前ステップ")
    @discord.ui.button(label="後ろステップ", style=discord.ButtonStyle.secondary, row=2)
    async def b_step(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "後ろステップ")

    # 4行目：システム ＆ SA (row=3)
    @discord.ui.button(label="ドライブインパクト", style=discord.ButtonStyle.danger, row=3)
    async def di(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "ドライブインパクト")
    @discord.ui.button(label="ドライブパリィ", style=discord.ButtonStyle.success, row=3)
    async def dp(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "ドライブパリィ")
    @discord.ui.button(label="SA1", style=discord.ButtonStyle.primary, row=3)
    async def sa1(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "SA1")
    @discord.ui.button(label="SA2", style=discord.ButtonStyle.primary, row=3)
    async def sa2(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "SA2")
    @discord.ui.button(label="SA3", style=discord.ButtonStyle.primary, row=3)
    async def sa3(self, interaction: discord.Interaction, btn: discord.ui.Button): await self.add_part(interaction, "SA3")

    # 5行目：システム制御 (row=4)
    @discord.ui.button(label="一手戻る", style=discord.ButtonStyle.danger, row=4)
    async def undo(self, interaction: discord.Interaction, btn: discord.ui.Button):
        if self.combo_parts: 
            removed = self.combo_parts.pop()
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(f"❌ 「{removed}」を取り消しました", ephemeral=True)

    @discord.ui.button(label="クリア", style=discord.ButtonStyle.danger, row=4)
    async def clear(self, interaction: discord.Interaction, btn: discord.ui.Button):
        self.combo_parts.clear()
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("🧹 入力をすべてクリアしました", ephemeral=True)

    @discord.ui.button(label="送信", style=discord.ButtonStyle.success, row=4)
    async def submit(self, interaction: discord.Interaction, btn: discord.ui.Button):
        current_str = self.get_combo_string()
        if not current_str:
            await interaction.response.send_message("コンボが空っぽです！", ephemeral=True)
            return
        
        user_name = interaction.user.display_name
        # 元のボタン画面を片付ける
        await interaction.response.edit_message(content="コンボを送信しました！", view=None)
        
        # 全体チャットへ綺麗なコンボをドンと投稿
        output_msg = f"**📢 {user_name} のコンボ投稿:**\n"
        if self.memo:
            output_msg += f"[コンボ名: {self.memo}]\n"
        output_msg += f"`{current_str}`"
        
        await interaction.channel.send(output_msg)
        self.stop()

# ==========================================
# 4. コマンド登録と起動
# ==========================================
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()

@bot.tree.command(name="combo-maker", description="スト6用コンボメーカーを起動します")
@app_commands.describe(memo="コンボ名や状況のメモ（例：使いやすいやつ、画面端限定 など）")
async def combo_maker(interaction: discord.Interaction, memo: str = None):
    view = ComboMakerView(memo=memo)
    memo_line = f"**コンボ名:** {memo}\n" if memo else ""
    await interaction.response.send_message(
        content=f"**[起動ユーザー限定]**\n{memo_line}ボタンをリズムよく押してコンボを作ってね！最後に「送信」で全体に流れます。", 
        view=view, 
        ephemeral=True
    )

keep_alive()
TOKEN = os.environ.get("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot.run(TOKEN)
