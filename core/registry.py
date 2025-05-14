# core/registry.py
from core.exceptions import UnsupportedFormatError

_converter_registry = {}

def register_converter(input_ext, output_ext, converter_class):
    if input_ext not in _converter_registry:
        _converter_registry[input_ext] = {}
    _converter_registry[input_ext][output_ext] = converter_class

def get_converter(input_ext, output_ext):
    try:
        return _converter_registry[input_ext][output_ext]
    except KeyError:
        raise UnsupportedFormatError(f"不支持从 {input_ext} 到 {output_ext} 的转换")