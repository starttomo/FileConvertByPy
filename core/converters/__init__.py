# 确保所有转换器被导入，这样它们会被自动注册到工厂
from .docx_converter import DocxConverter
from .pdf_converter import PdfConverter
from .html_converter import HtmlConverter
from .doc_converter import DocConverter

# 方便外部导入
__all__ = ['DocxConverter', 'PdfConverter', 'HtmlConverter', 'DocConverter']