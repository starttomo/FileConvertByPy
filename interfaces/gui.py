import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from core.factory import ConverterFactory
from core.utils import validate_file_path
from core.exceptions import FileConversionError


class FileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文件格式转换器")
        self.root.geometry("600x400")
        self.setup_ui()

        # 初始化转换器工厂
        ConverterFactory.load_converters()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 输入文件部分
        input_frame = ttk.LabelFrame(main_frame, text="输入文件", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        self.input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(input_frame, text="浏览...", command=self.select_input_file).pack(side=tk.RIGHT)

        # 输出文件部分
        output_frame = ttk.LabelFrame(main_frame, text="输出文件", padding="10")
        output_frame.pack(fill=tk.X, pady=5)

        self.output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="浏览...", command=self.select_output_file).pack(side=tk.RIGHT)

        # 格式选择部分
        format_frame = ttk.LabelFrame(main_frame, text="转换格式", padding="10")
        format_frame.pack(fill=tk.X, pady=5)

        ttk.Label(format_frame, text="从").pack(side=tk.LEFT)
        self.input_format = tk.StringVar()
        self.input_format_combo = ttk.Combobox(
            format_frame, textvariable=self.input_format, state="readonly", width=10)
        self.input_format_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(format_frame, text="到").pack(side=tk.LEFT)
        self.output_format = tk.StringVar()
        self.output_format_combo = ttk.Combobox(
            format_frame, textvariable=self.output_format, state="readonly", width=10)
        self.output_format_combo.pack(side=tk.LEFT, padx=5)

        # 绑定事件
        self.input_path.trace_add('write', self.update_input_format)
        self.input_format.trace_add('write', self.update_output_formats)

        # 转换按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="转换",
            command=self.perform_conversion,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT, padx=5)

        # 日志输出
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 样式配置
        self.root.style = ttk.Style()
        self.root.style.configure('Accent.TButton', foreground='white', background='#0078d7')

    def select_input_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_path.set(file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            self.output_path.set(file_path)

    def update_input_format(self, *args):
        input_path = self.input_path.get()
        if not input_path:
            return

        try:
            input_ext = Path(input_path).suffix[1:].lower()
            if not input_ext:
                return

            # 更新输入格式组合框
            self.input_format_combo['values'] = [input_ext]
            self.input_format.set(input_ext)

            # 更新可能的输出格式
            self.update_output_formats()
        except Exception:
            pass

    def update_output_formats(self, *args):
        input_ext = self.input_format.get()
        if not input_ext:
            return

        # 获取所有支持的输出格式
        output_formats = []
        if hasattr(ConverterFactory, '_converters'):
            if input_ext in ConverterFactory._converters:
                output_formats = list(ConverterFactory._converters[input_ext].keys())

        # 更新输出格式组合框
        self.output_format_combo['values'] = output_formats
        if output_formats:
            self.output_format.set(output_formats[0])

    def perform_conversion(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        input_ext = self.input_format.get()
        output_ext = self.output_format.get()

        if not all([input_path, output_path, input_ext, output_ext]):
            messagebox.showerror("错误", "请填写所有必要字段")
            return

        try:
            # 验证文件路径
            input_path, output_path, input_ext, output_ext = validate_file_path(
                input_path, output_path)

            # 获取转换器并执行转换
            converter = ConverterFactory.get_converter(input_ext, output_ext)
            converter.convert(input_path, output_path, input_ext, output_ext)

            self.log(f"转换成功: {input_path} -> {output_path}")
            messagebox.showinfo("成功", "文件转换成功!")
        except Exception as e:
            self.log(f"转换失败: {str(e)}", error=True)
            messagebox.showerror("错误", f"转换失败: {str(e)}")

    def log(self, message, error=False):
        self.log_text.config(state=tk.NORMAL)
        tag = "ERROR" if error else "INFO"
        self.log_text.insert(tk.END, f"[{tag}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 配置标签样式
        self.log_text.tag_config("ERROR", foreground="red")
        self.log_text.tag_config("INFO", foreground="green")


def run_gui():
    root = tk.Tk()
    app = FileConverterGUI(root)
    root.mainloop()