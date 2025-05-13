# core/converters/doc_converter.py
import subprocess
import os
from tempfile import mkstemp
from core.converters.base_converter import BaseConverter
from core.exceptions import FileConversionError, UnsupportedFormatError
from core.registry import register_converter  # 导入新的注册函数

class DocConverter(BaseConverter):
    """处理DOC文件的转换(使用LibreOffice)"""

    @classmethod
    def supported_formats(cls) -> dict:
        return {
            'doc': ['docx', 'pdf', 'html', 'txt'],
            # 可以添加更多支持的输出格式
        }

    @classmethod
    def convert(cls, input_path: str, output_path: str, input_ext: str, output_ext: str):
        try:
            cls._ensure_output_dir_exists(output_path)

            if output_ext not in ['docx', 'pdf', 'html', 'txt']:
                raise UnsupportedFormatError(f"不支持将 doc 转换为 {output_ext}")

            # 使用LibreOffice进行转换
            temp_output = None
            try:
                # 对于某些格式，可能需要先转换为docx
                if output_ext == 'docx':
                    cls._convert_with_libreoffice(input_path, output_path, 'docx')
                elif output_ext == 'pdf':
                    cls._convert_with_libreoffice(input_path, output_path, 'pdf')
                elif output_ext in ['html', 'txt']:
                    # 先转换为docx，然后再转换为目标格式
                    fd, temp_output = mkstemp(suffix='.docx')
                    os.close(fd)
                    cls._convert_with_libreoffice(input_path, temp_output, 'docx')

                    # 使用DocxConverter进行进一步转换
                    from core.converters.docx_converter import DocxConverter
                    DocxConverter.convert(temp_output, output_path, 'docx', output_ext)
            finally:
                if temp_output and os.path.exists(temp_output):
                    os.unlink(temp_output)
        except Exception as e:
            raise FileConversionError(f"DOC转换失败: {str(e)}")

    @classmethod
    def _convert_with_libreoffice(cls, input_path: str, output_path: str, output_format: str):
        """使用LibreOffice进行转换"""
        try:
            cmd = [
                'soffice',
                '--headless',
                '--convert-to',
                output_format,
                input_path,
                '--outdir',
                os.path.dirname(output_path) or '.'
            ]

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            # 检查输出文件是否生成
            if not os.path.exists(output_path):
                generated_file = os.path.join(
                    os.path.dirname(output_path),
                    os.path.splitext(os.path.basename(input_path))[0] + '.' + output_format
                )
                if os.path.exists(generated_file):
                    os.rename(generated_file, output_path)
                else:
                    raise FileConversionError("LibreOffice转换失败，未生成输出文件")
        except subprocess.CalledProcessError as e:
            raise FileConversionError(f"LibreOffice转换失败: {e.stderr.decode('utf-8')}")
        except FileNotFoundError:
            raise FileConversionError("LibreOffice未安装或不在PATH中")

# 使用新的注册机制
for input_ext, output_exts in DocConverter.supported_formats().items():
    for output_ext in output_exts:
        register_converter(input_ext, output_ext, DocConverter)