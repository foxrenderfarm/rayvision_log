"""Basic logging setup."""
from copy import deepcopy
from getpass import getuser
import logging.config
import os
from socket import getfqdn
import traceback

from appdirs import user_log_dir
import yaml


def init_logger(app_name):
    """Initialize logging with our default configuration.

    An easier interface for artists to use to create loggers in their
    packages and applications. Any application that uses this will use the
    default logging configuration.

    Examples:
        >>> import logging
        >>> from rayvision_log import init_logger
        >>> app_name = "rayvision_api"
        >>> init_logger(app_name)
        >>> LOG = logging.getLogger(app_name)

    Args:
        app_name (str): The application or package name for which to create a logger.
    """
    try:
        log_config = get_default_log_config()
        set_up_logger(app_name, log_config)
    except Exception:  # pylint: disable=broad-except
        # Catch a broad exception here, since there's no reason logging setup
        # failing should crash a program.
        err_msg = traceback.format_exc()
        logging.basicConfig()
        logger = logging.getLogger("rayvision_log")
        logger.exception("rayvision log initilization failed.\n%s", err_msg)


def get_default_log_config():
    """Get the default logging configuration.

    Returns:
        dict: The default logging configuration.

    """
    root = os.path.dirname(__file__)
    config_file = os.path.join(root, "logging.yaml")
    with open(config_file, "r") as file_object:
        data = yaml.load(file_object, yaml.FullLoader)
    return data["logging"]


def set_up_logger(app_name, log_config):
    """Set up loggers based on given name and configuration.

    Example:
        >>> app_name = "rayvision_api"
        >>> log_config = {
                            formatters: {
                                file: {
                                    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                                }
                            },
                            handlers: {
                                file: {
                                    class: concurrent_log_handler.ConcurrentRotatingFileHandler
                                }
                            }
                        }

    Args:
        app_name (str): Name of the application.
        log_config (dict): The configuration of the logger.

    References:
        https://pypi.org/project/ConcurrentLogHandler/

    """
    log_config = deepcopy(log_config)
    if log_config["handlers"].get("file"):
        root = os.getenv(
            "RAYVISION_LOG_ROOT", user_log_dir(app_name, appauthor="RayVision")
        )
        filename = os.path.join(root, getuser(), "{}.log".format(getfqdn()))
        log_config["handlers"]["file"]["filename"] = filename
        folder = os.path.dirname(filename)
        if not os.path.isdir(folder):
            os.makedirs(folder)
    logging.config.dictConfig(log_config)
