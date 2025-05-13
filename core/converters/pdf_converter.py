# core/converters/pdf_converter.py
from pdfminer.high_level import extract_text
from core.converters.base_converter import BaseConverter
from core.exceptions import FileReadError, FileWriteError, UnsupportedFormatError, FileConversionError
from core.registry import register_converter  # 导入新的注册函数

class PdfConverter(BaseConverter):
    """处理PDF文件的转换"""

    @classmethod
    def supported_formats(cls) -> dict:
        return {
            'pdf': ['txt', 'html'],
            # 可以添加更多支持的输出格式
        }

    @classmethod
    def convert(cls, input_path: str, output_path: str, input_ext: str, output_ext: str):
        try:
            cls._ensure_output_dir_exists(output_path)

            if output_ext == 'txt':
                cls._convert_to_txt(input_path, output_path)
            elif output_ext == 'html':
                cls._convert_to_html(input_path, output_path)
            else:
                raise UnsupportedFormatError(f"不支持将 pdf 转换为 {output_ext}")
        except Exception as e:
            raise FileConversionError(f"PDF转换失败: {str(e)}")

    @classmethod
    def _convert_to_txt(cls, input_path: str, output_path: str):
        try:
            text = extract_text(input_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            raise FileReadError(f"读取PDF文件失败: {str(e)}")

    @classmethod
    def _convert_to_html(cls, input_path: str, output_path: str):
        try:
            text = extract_text(input_path)
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Converted PDF</title>
            </head>
            <body>
                <pre>{text}</pre>
            </body>
            </html>
            """
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            raise FileWriteError(f"写入HTML文件失败: {str(e)}")

# 使用新的注册机制
for input_ext, output_exts in PdfConverter.supported_formats().items():
    for output_ext in output_exts:
        register_converter(input_ext, output_ext, PdfConverter)