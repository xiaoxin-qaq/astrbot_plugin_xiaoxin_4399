from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp


@register("4399account", "YourName", "获取4399账号", "1.1.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        logger.info("4399账号插件已加载")

    # 发送 /4399 触发
    @filter.command("4399")
    async def get_4399_account(self, event: AstrMessageEvent):
        """获取4399免费账号"""
        api_url = "https://em.xiaoxin.skin/"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=10) as response:
                    if response.status != 200:
                        yield event.plain_result("❌ API请求失败，服务器异常")
                        return

                    text = await response.text()
                    text = text.strip()

                    # ============= 自动拆分账号、密码、广告，分行显示 =============
                    if "-----" in text:
                        part = text.split("-----")
                        username = part[0].strip()

                        if "本api由xiaoxin1336制作" in part[1]:
                            password_part = part[1].replace(" 本api由xiaoxin1336制作", "").strip()
                            password = password_part
                        else:
                            password = part[1].strip()

                        # 输出格式：账号 + 换行 + 密码 + 换行 + 广告
                        result = f"🎮 4399账号信息\n━━━━━━━━━━━━\n{username}\n{password}\n本api由xiaoxin1336制作\n━━━━━━━━━━━━"
                    else:
                        result = f"🎮 4399账号信息\n━━━━━━━━━━━━\n{text}\n━━━━━━━━━━━━"
                    # ============================================================

                    yield event.plain_result(result)

        except Exception as e:
            logger.error(f"4399 API错误：{e}")
            yield event.plain_result(f"❌ 请求失败：{str(e)}")

    async def terminate(self):
        logger.info("4399账号插件已卸载")