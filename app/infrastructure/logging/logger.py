import logging
import sys
from pathlib import Path
from typing import Optional


def configure_logging(
        level: str = "INFO",
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
) -> None:
    """
    Настройка логирования для приложения

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу лога (опционально)
        format_string: Формат сообщения лога
    """
    # Формат по умолчанию
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"

    # Конфигурация
    config = {
        "level": getattr(logging, level.upper(), logging.INFO),
        "format": format_string,
        "handlers": [logging.StreamHandler(sys.stdout)]
    }

    # Файловый хендлер (если указан)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        config["handlers"].append(
            logging.FileHandler(log_file, encoding="utf-8", mode="a")
        )

    # Применяем конфигурацию
    logging.basicConfig(**config)

    # Устанавливаем уровень для SQLAlchemy (чтобы не спамило в DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Получить инстанс логгера по имени

    Args:
        name: Обычно __name__ модуля

    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)
