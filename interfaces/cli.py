import argparse
from core.factory import ConverterFactory
from core.utils import validate_file_path
from core.exceptions import FileConversionError, UnsupportedFormatError
import sys

def run_cli():
    parser = argparse.ArgumentParser(description='文件格式转换工具')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('--list', action='store_true', help='列出支持的转换格式')

    args = parser.parse_args()

    if args.list:
        _list_supported_conversions()
        return

    try:
        input_path, output_path, input_ext, output_ext = validate_file_path(args.input, args.output)

        converter = ConverterFactory.get_converter(input_ext, output_ext)
        converter.convert(input_path, output_path, input_ext, output_ext)

        print(f"转换成功: {input_path} -> {output_path}")
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


def _list_supported_conversions():
    print("支持的转换格式:")
    print("输入格式 -> 输出格式")
    print("-------------------")

    # 获取所有已注册的转换器支持格式
    for input_ext in ConverterFactory._converters:
        for output_ext in ConverterFactory._converters[input_ext]:
            print(f"{input_ext:8} -> {output_ext}")