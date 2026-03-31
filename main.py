from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
import aiohttp
import time
import json
import os

# ====================== 配置 ======================
API_URL = "https://em.xiaoxin.skin"
API_TOKEN = "购买"
ADMIN_QQ = "2275524927"      # 管理员QQ
LOW_STOCK = 10              # 库存低于这个值提醒
AD_TEXT = "购买api上xiaoxin1337.top"  # 广告
DATA_FILE = "4399_limit.json"
# ==================================================

# 每日限制
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"date": time.strftime("%Y-%m-%d"), "users": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f)

def check_limit(uid):
    today = time.strftime("%Y-%m-%d")
    data = load_data()
    if data["date"] != today:
        data = {"date": today, "users": {}}
    if uid not in data["users"]:
        data["users"][uid] = 0
    if data["users"][uid] >= 20:
        return False, data["users"][uid]
    data["users"][uid] += 1
    save_data(data)
    return True, data["users"][uid]

# 插件注册（已修复 desc 缺失报错）
@register(
    name="4399账号获取",
    author="xiaoxin1336",
    desc="获取4399账号密码Sauth+每日限制+库存提醒",
    version="1.0.0"
)
class Main(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        pass

    @filter.command("4399")
    async def on_message(self, event: AstrMessageEvent):
        uid = str(event.get_sender_id())
        ok, cnt = check_limit(uid)
        if not ok:
            yield event.plain_result(f"❌ 今日已达上限({cnt}/20)")
            return

        try:
            url = f"{API_URL}?token={API_TOKEN}"
            async with aiohttp.ClientSession() as s:
                async with s.get(url, ssl=False) as r:
                    t = await r.text()

            if "----" not in t:
                yield event.plain_result("❌ 服务异常")
                return

            a, b, c, stock_str = t.split("----")
            stock = int(stock_str)

            # 库存不足提醒管理员
            if stock < LOW_STOCK:
                warn_msg = f"⚠️库存预警！4399仅剩 {stock}，请管理员 {ADMIN_QQ} 及时补货！"
                yield event.plain_result(warn_msg)

            # 最终返回消息
            yield event.plain_result(f"""🎮 4399账号
━━━━━━━━
账号：{a}
密码：{b}
Sauth：{c}
库存：{stock}
━━━━━━━━
{AD_TEXT}
今日已领：{cnt}/20""")

        except Exception as e:
            yield event.plain_result("❌ 连接失败")

    async def terminate(self):
        pass