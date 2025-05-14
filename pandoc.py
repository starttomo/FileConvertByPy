import pypandoc

try:
    pypandoc.get_pandoc_path()
except OSError:
    pypandoc.download_pandoc()