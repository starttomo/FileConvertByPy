from abc import ABC, abstractmethod
from pathlib import Path
from core.exceptions import FileConversionError


class BaseConverter(ABC):
    """所有转换器的抽象基类"""

    @classmethod
    @abstractmethod
    def supported_formats(cls) -> dict:
        """
        返回支持的转换格式
        :return: {'input_format': ['output_format1', 'output_format2']}
        """
        pass

    @classmethod
    def can_convert(cls, input_ext: str, output_ext: str) -> bool:
        """检查是否支持指定的转换"""
        formats = cls.supported_formats()
        return input_ext in formats and output_ext in formats[input_ext]

    @classmethod
    @abstractmethod
    def convert(cls, input_path: str, output_path: str, input_ext: str, output_ext: str):
        """
        执行文件转换
        :raises: FileConversionError 如果转换失败
        """
        pass

    @classmethod
    def _ensure_output_dir_exists(cls, output_path: str):
        """确保输出目录存在"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)