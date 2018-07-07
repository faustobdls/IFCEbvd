# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

# Modify by: Fausto Blanco | UFERSA

import sys
import re
import os

def make_pdf(_livro):
    print('convertendo para PDF...')
    from fpdf import FPDF
    from PIL import Image
    import glob
    list_pages = sorted(glob.glob('book/*.jpg'))
    cover = Image.open(str(list_pages[0]))
    width, height = cover.size
    pdf = FPDF(unit='pt', format=[width, height])
    for page in list_pages:
        print(page)
        pdf.add_page()
        pdf.image(str(page), 0, 0)
    pdf.output('books/%s.pdf' % _livro, 'F')
    for page in list_pages:
        os.remove(page)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Falta fornecer parâmetros!\n"
              "Sintaxe: download.py <id do livro> [ids de outros livros] ..")
        exit()

    _, *book_list = sys.argv

    book_list = map(lambda i: i if (i.isdigit()) else re.match(r'(?:.*publications\/(\d+)|(\d+))', i).group(1), book_list)

    for livro_atual in book_list:
        # dump(matricula, senha, livro_atual)
        make_pdf(livro_atual)
    print('operacao finalizada.')
