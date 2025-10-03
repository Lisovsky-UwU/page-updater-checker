from src import msg_templates
from src.bot import build_bot, create_bot_thread
from src.config import app_config
from src.log import logger, setup_log
from src.page_checker import PageUpdaterChecker
from src.worker_cheker import WorkerChecker


def main() -> None:
    setup_log(app_config.log.level, app_config.log.log_to_console)
    logger.info("Запуск модуля page-updater-checker")
    if not app_config.tg_bot.token:
        logger.critical("Не установлен токен бота, запуск невозможен")
        return

    try:
        logger.debug("Запуск бота")
        bot = build_bot(app_config.tg_bot.token)
        bot_thread = create_bot_thread(bot)
        bot_thread.start()
        logger.info("Бот был запущен")
    except Exception:
        logger.exception("Ошибка запуска ТГ бота")
        return

    if app_config.tg_bot.chat_id != 0:
        logger.debug("Оповещение в чат id=%s о запуске", app_config.tg_bot.chat_id)
        try:
            bot.send_message(
                app_config.tg_bot.chat_id,
                msg_templates.START_MSG.format(url=app_config.page_parser.address),
            )
        except Exception:
            logger.exception("Ошибка уведомления о запуске в чат id=%s", app_config.tg_bot.chat_id)
    else:
        logger.warning("Не установен идентификатор чата")

    worker = WorkerChecker(
        bot,
        app_config.tg_bot.chat_id,
        PageUpdaterChecker(
            app_config.page_parser.page_save_path,
            app_config.page_parser.address,
            app_config.page_parser.timeout,
        ),
        app_config.page_parser.check_period,
    )

    try:
        worker.run()
    except KeyboardInterrupt:
        logger.info("Штатное завершение работы приложения")
    except Exception:
        logger.exception("Возникла необработанная ошибка")
    finally:
        logger.debug("Выключение бота")
        bot_thread.join(5)
        if app_config.tg_bot.chat_id != 0:
            logger.debug("Оповещение в чат id=%s о выключении", app_config.tg_bot.chat_id)
            try:
               bot.send_message(
                   app_config.tg_bot.chat_id,
                   msg_templates.SHUTDOWN_MSG.format(url=app_config.page_parser.address),
               )
            except Exception:
                logger.exception(
                    "Ошибка уведомления о завершении в чат id=%s",
                    app_config.tg_bot.chat_id,
                )
        logger.info("Модуль завершит свою работу")


if __name__ == "__main__":
    main()

