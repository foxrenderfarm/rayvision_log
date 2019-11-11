"""Test rayvision_log core functions."""
import logging

from rayvision_log.core import init_logger, set_up_logger


def test_overwrite(monkeypatch, tmpdir):
    """Test we can overwrite the log output root."""
    root = tmpdir.join("test_log")
    monkeypatch.setenv("RAYVISION_LOG_ROOT", str(root))
    init_logger("rayvision_log_test")
    logger = logging.getLogger("rayvision_log_test")
    logger.info("test")
    assert len(root.listdir()) == 1


def test_init_logger():
    """Test init the custom logger."""
    config = {
        "version": 1,
        "formatters": {
            "file": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }  # noqa: E501 # pylint: disable=line-too-long
        },
        "handlers": {
            "file": {
                "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",  # noqa: E501 # pylint: disable=line-too-long
                "formatter": "file",
                "level": "DEBUG",
                "filename": "",
                "backupCount": 7,
                "maxBytes": "1024*1024*5",
                "delay": True,
            }
        },
        "loggers": {"": {"level": "DEBUG", "handlers": ["file"]}},
    }
    set_up_logger("rayvision_log_test", config)
    logging.basicConfig()
    logger = logging.getLogger("rayvision_log_test")
    logger.info("test")
    assert "rayvision_log_test" in logging.root.manager.loggerDict


def test_catch_setup_logger_failed(mocker):
    """Test that we can ignore the initialization log error.

    The idea behind this is that if we fail to initialize the log we will not
    affect the use of the log API and will be able to catch the wrong log.

    """
    mock_config = mocker.patch("rayvision_log.core.get_default_log_config")
    mock_config.return_value = {}
    init_logger("test_logger")
    assert "rayvision_log" in logging.root.manager.loggerDict
