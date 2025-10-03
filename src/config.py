from src.ext.parametrica import Field, Fieldset, Parametrica
from src.ext.parametrica.io import YAMLFileConfigIO


class TGBotSettings(Fieldset):
    token = Field[str]("").label("Токен бота ТГ")
    chat_id = Field[int](0).label("Идентификатор чата, в который отправлять уведомления")


class PageParserSettings(Fieldset):
    address = Field[str]("https://ya.ru") \
        .label("Полный адрес страницы, которую необходимо проверять")
    check_period = Field[int](60).label("Период для проверки страницы в секундах")
    page_save_path = Field[str]("page_cache.txt").label("Путь к сохранению файла страницы")
    timeout = Field[int](30).label("Таймаут для чтения страницы")


class LogSettings(Fieldset):
    level = Field[str]("info").label("Уровень логирования")
    log_to_console = Field[bool](True).label("Логи в консоль")


class AppConfig(Parametrica):
    tg_bot = Field[TGBotSettings]().label("Настройки ТГ бота")
    page_parser = Field[PageParserSettings]().label("Настройки парсинга страницы")
    log = Field[LogSettings]().label("Настройки логирования")


app_config = AppConfig(YAMLFileConfigIO("page_updater_checker.yaml"))

