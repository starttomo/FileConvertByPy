# core/factory.py
from core.registry import get_converter
from core.exceptions import UnsupportedFormatError

class ConverterFactory:
    """转换器工厂，负责创建和管理转换器"""

    @classmethod
    def create_converter(cls, input_ext: str, output_ext: str):
        """创建适合的转换器实例"""
        converter_class = get_converter(input_ext, output_ext)
        return converter_class()

    @classmethod
    def load_converters(cls):
        """动态加载所有转换器"""
        # 导入所有转换器模块，触发注册
        from core.converters import (
            docx_converter, pdf_converter, html_converter, doc_converter
        )

    @classmethod
    def get_converter(cls, input_ext, output_ext):
        """获取适合的转换器类"""
        return get_converter(input_ext, output_ext)