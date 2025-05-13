# core/converters/html_converter.py
import html2text
from core.converters.base_converter import BaseConverter
from core.exceptions import FileReadError, FileWriteError, UnsupportedFormatError, FileConversionError
from core.registry import register_converter  # 导入新的注册函数

class HtmlConverter(BaseConverter):
    """处理HTML文件的转换"""

    @classmethod
    def supported_formats(cls) -> dict:
        return {
            'html': ['txt', 'pdf'],
            # 可以添加更多支持的输出格式
        }

    @classmethod
    def convert(cls, input_path: str, output_path: str, input_ext: str, output_ext: str):
        try:
            cls._ensure_output_dir_exists(output_path)

            if output_ext == 'txt':
                cls._convert_to_txt(input_path, output_path)
            elif output_ext == 'pdf':
                cls._convert_to_pdf(input_path, output_path)
            else:
                raise UnsupportedFormatError(f"不支持将 html 转换为 {output_ext}")
        except Exception as e:
            raise FileConversionError(f"HTML转换失败: {str(e)}")

    @classmethod
    def _convert_to_txt(cls, input_path: str, output_path: str):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            text = html2text.html2text(html_content)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            raise FileReadError(f"读取HTML文件失败: {str(e)}")

    @classmethod
    def _convert_to_pdf(cls, input_path: str, output_path: str):
        try:
            import pypandoc
            pypandoc.convert_file(
                input_path,
                'pdf',
                outputfile=output_path,
                format='html'
            )
        except ImportError:
            raise FileConversionError("PDF转换需要安装pypandoc和系统上的pandoc")
        except Exception as e:
            raise FileWriteError(f"生成PDF失败: {str(e)}")

# 使用新的注册机制
for input_ext, output_exts in HtmlConverter.supported_formats().items():
    for output_ext in output_exts:
        register_converter(input_ext, output_ext, HtmlConverter)