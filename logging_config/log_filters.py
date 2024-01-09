import logging

class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'ERROR'

class CriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'CRITICAL'
    
class DebugWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('DEBUG', 'WARNING')