import logging as _log

_log.basicConfig(level=_log.WARNING, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logging = _log
