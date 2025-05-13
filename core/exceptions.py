class FileConversionError(Exception):
    """文件转换异常基类"""
    pass

class UnsupportedFormatError(FileConversionError):
    """不支持的格式异常"""
    pass

class FileReadError(FileConversionError):
    """文件读取异常"""
    pass

class FileWriteError(FileConversionError):
    """文件写入异常"""
    pass