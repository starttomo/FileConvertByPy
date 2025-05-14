import sys
from core.factory import ConverterFactory
from interfaces import run_cli, run_gui


def main():

    # 加载所有转换器
    ConverterFactory.load_converters()

    # 根据参数决定运行CLI还是GUI
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()


if __name__ == '__main__':
    main()