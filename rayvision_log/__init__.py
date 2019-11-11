"""Rayvision logging."""

# Disabling the import error because PyLint chokes on importing pkg_resources,
# it is available though.
# pylint: disable=import-error
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from rayvision_log.core import init_logger
from rayvision_log.core import set_up_logger

__all__ = ["init_logger", "set_up_logger"]

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # Package is not installed.
    __version__ = "0.0.0-dev.1"
