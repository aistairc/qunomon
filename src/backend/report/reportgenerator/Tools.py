
import codecs

def read_file(filepath):
    # Excelでcsvを作るとshiht-jisになり、UnicodeDecodeErrorが発生するかもしれないので、その対応が必要
    fin = codecs.open(r'' + filepath, "r", "utf-8")
    contents = fin.read()
    fin.close()
    return contents


def write_file(filepath, htmlcode, write_mode="w"):
    fout = codecs.open(r'' + filepath, write_mode, "utf-8")
    fout.write(htmlcode)
    fout.close()


def replace_html(htmlfile: str, htmlcode: str, output_filepath: str, replacemark="%%replace%%"):
    # 参照テンプレート、置換文字、保存先ファイル、置換対象文字
    contents = read_file(htmlfile)
    contents_replaced = contents.replace(replacemark, htmlcode)
    write_file(output_filepath, contents_replaced)
