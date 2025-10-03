import time
from datetime import datetime

from telebot import TeleBot

from src import msg_templates
from src.log import logger
from src.page_checker import PageUpdaterChecker


class WorkerChecker:

    def __init__(
        self,
        bot: TeleBot,
        tg_chat_id_to_send: int,
        page_checker: PageUpdaterChecker,
        check_period: int = 60,
    ) -> None:
        self._bot = bot
        self._tg_chat_id = tg_chat_id_to_send
        self._page_checker = page_checker
        self._check_period = check_period

    def notify_chat(self, diff_text: str) -> None:
        if not self._tg_chat_id:
            logger.warning("Не установлен chat_id, невозможно отправить уведомление")
            return
        try:
            logger.debug("Отправляем уведомление в чат id=%s", self._tg_chat_id)
            self._bot.send_message(
                self._tg_chat_id,
                msg_templates.PAGE_CHANGE_TEXT.format(
                    url=self._page_checker.page_url,
                    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    diff=diff_text,
                ),
            )
            logger.info("Уведомление было успешно отправлено")
        except Exception:
            logger.exception("Ошибка при отправки уведомления в чат id=%s", self._tg_chat_id)


    def do_check(self) -> None:
        logger.debug("Проверка url=%s на наличие изменений", self._page_checker.page_url)
        diff_result = self._page_checker.check_update()
        if diff_result != None:
            logger.info(
                "Обнаружены изменения на странице url=%(url)s\n\nТекст изменений:\n%(diff)s",
                {
                    "url": self._page_checker.page_url,
                    "diff": diff_result,
                },
            )
            self.notify_chat(diff_result)
        else:
            logger.debug("Изменений не обнаружено")

    def run(self) -> None:
        while True:
            try:
                self.do_check()
            except Exception:
                logger.exception("Ошибка при проверке изменений на странице")
            time.sleep(self._check_period)

