# core/converters/pdf_converter.py
from pdf2docx import Converter
from core.converters.base_converter import BaseConverter
from core.exceptions import FileReadError, FileWriteError, UnsupportedFormatError, FileConversionError
from core.registry import register_converter

class PdfConverter(BaseConverter):
    """处理PDF文件的转换"""

    @classmethod
    def supported_formats(cls) -> dict:
        return {
            'pdf': ['docx', 'txt'],  # 添加对 docx 的支持
            # 可以添加更多支持的输出格式
        }

    @classmethod
    def convert(cls, input_path: str, output_path: str, input_ext: str, output_ext: str):
        try:
            cls._ensure_output_dir_exists(output_path)

            if output_ext == 'docx':
                cls._convert_to_docx(input_path, output_path)
            elif output_ext == 'txt':
                cls._convert_to_txt(input_path, output_path)
            else:
                raise UnsupportedFormatError(f"不支持将 pdf 转换为 {output_ext}")
        except Exception as e:
            raise FileConversionError(f"PDF转换失败: {str(e)}")

    @classmethod
    def _convert_to_docx(cls, input_path: str, output_path: str):
        try:
            # 检查PDF是否是扫描版（需要使用pdfplumber或其他库检测）
            # 这里简化处理，假设用户知道需要OCR处理
            use_ocr = True  # 可以通过参数或检测决定是否使用OCR

            if use_ocr:
                # 使用OCR处理
                import pdf2image
                from PIL import Image
                import pytesseract

                # 将PDF转换为图像
                images = pdf2image.convert_from_path(input_path)

                # 使用OCR提取文本
                text = ""
                for image in images:
                    text += pytesseract.image_to_string(image, lang='chi_sim')  # 指定中文识别

                # 创建DOCX文件
                from docx import Document
                doc = Document()
                doc.add_paragraph(text)
                doc.save(output_path)
            else:
                # 直接转换（适用于文本型PDF）
                cv = Converter(input_path)
                cv.convert(output_path)
                cv.close()
        except Exception as e:
            raise FileConversionError(f"PDF转DOCX失败: {str(e)}")
    @classmethod
    def _convert_to_txt(cls, input_path: str, output_path: str):
        try:
            # 使用 pdfplumber 或其他库提取文本
            import pdfplumber
            with pdfplumber.open(input_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            raise FileReadError(f"读取PDF文件失败: {str(e)}")

# 注册转换器
for input_ext, output_exts in PdfConverter.supported_formats().items():
    for output_ext in output_exts:
        register_converter(input_ext, output_ext, PdfConverter)