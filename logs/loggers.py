"""
일단 json 을 사용

"""

import os

logger_setting = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detail_formatter": {
            "format": "[%(asctime)s] %(levelname)s [%(module)s %(name)s :%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "summary_formatter": {
            "format": "%(asctime)s:%(module)s:%(levelname)s:%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "file_debug_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "file_debug_formatter",
            'when': 'midnight',     # 로그 백업 시간
            "interval": 1,          # 간격
            'backupCount': 10,      # 백업 로그 갯수
            "encoding": "utf-8"
        },
        "file_debug": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "filename": "debug.log"
        },
        "file_error": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "basic",
            "filename": "error.log"
        }
    },
    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["console", "file_debug", "file_error"],
            "propagate": True
        }
    }
}