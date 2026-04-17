class MaskingConfigError(Exception):
    """Raised when config file is invalid or missing required fields"""
    pass

class UnsupportedStrategyError(Exception):
    """Raised when config references a strategy that doesn't exist"""
    pass

class FileHandlerError(Exception):
    """Raised when input/output file operations fail"""
    pass