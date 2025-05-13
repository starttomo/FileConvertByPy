import os
from pathlib import Path
from typing import Tuple


def validate_file_path(input_path: str, output_path: str) -> Tuple[str, str, str, str]:
    """
    验证文件路径并提取扩展名
    :return: (input_path, output_path, input_ext, output_ext)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    input_ext = Path(input_path).suffix[1:].lower()  # 去掉点并转为小写
    output_ext = Path(output_path).suffix[1:].lower()

    if not input_ext or not output_ext:
        raise ValueError("文件必须包含扩展名")

    return input_path, output_path, input_ext, output_ext