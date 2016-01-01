# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib
import hashlib
import sys
import re
import os


def page_download(_url, _nome):
    try:
        urllib.request.urlretrieve(_url, _nome)
    except:
        print('problemas ao baixar %s' % _nome)
    else:
        print('%s baixado' % _nome)

_hash = lambda _mat: 'login=%s&token=%s' % (_mat, hashlib.md5(('%sQJEkJM2iLJiAj6LScxsZivml54SmzSy0' % _mat).encode()).hexdigest())


def dump(matricula, id_book):
    phantom = webdriver.PhantomJS()
    phantom.set_page_load_timeout(10)

    # Login
    print('gerando cookie de login para matricura %s...' % matricula)
    try:
        phantom.get('http://ifce.bv3.digitalpages.com.br/user_session/authentication_gateway?%s' % _hash(matricula))
    except TimeoutException:
        print('Timeout durante o login... Refazendo-o...')
        return dump(matricula, id_book)

    # Obter informações do livro
    print('obtendo informacoes para o livro %s...' % id_book)
    try:
        phantom.get('http://ifce.bv3.digitalpages.com.br/users/publications/%s' % id_book)
    except TimeoutException as e:
        print('Timeout durante a coleta das informações do livro... Recomeçando tudo...')
        return dump(matricula, id_book)
    p_1 = 0
    while p_1 == 0:
        try:
            p_1 = phantom.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
        except:
            p_1 = 0
    num_pag = int(phantom.execute_script('return RDP.options.pageSetLength')) - 2

    # Download
    print('preparando para baixar livro id=%s com %d paginas...' % (id_book, num_pag))
    page_download(phantom.execute_script("return $('.backgroundImg')[0].src"), '%s-00000.jpg' % id_book)
    print('baixando livro...')
    phantom.execute_script('navigate.next_page()')
    _v_p1, _v_p2 = '', ''
    for i in range(1, num_pag, 2):
        # loop para esperar a pagina carregar
        p_1, p_2 = 0, 0
        while (p_1 == 0) or (p_2 == 0):
            try:
                p_1 = phantom.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
                p_2 = phantom.execute_script("if ($('.backgroundImg')[1]) { return 1 } else { return 0 }")
            except:
                p_1 , p_2 = 0, 0
        # carregou, pegar endereco
        _p1 = phantom.execute_script("return $('.backgroundImg')[0].src")
        _p2 = phantom.execute_script("return $('.backgroundImg')[1].src")
        # checa se ainda não carregou a nova pagina
        while (_p1 == _v_p1) or (_p2 == _v_p2):
            try:
                _p1 = phantom.execute_script("return $('.backgroundImg')[0].src")
                _p2 = phantom.execute_script("return $('.backgroundImg')[1].src")
            except:
                pass
        # carregou nova, baixar...
        page_download(_p1, '%s-%05d.jpg' % (id_book, i))
        page_download(_p2, '%s-%05d.jpg' % (id_book, i+1))
        # ajusta os novos valores
        _v_p1, _v_p2 = _p1, _p2
        phantom.execute_script('navigate.next_page()')
        print('baixadas %d/%d paginas...' % (i,num_pag))

    # Finalização
    print('fim do dump')
    phantom.quit()


def make_pdf(_livro):
    print('convertendo para PDF...')
    from fpdf import FPDF
    from PIL import Image
    import glob
    list_pages = sorted(glob.glob('*.jpg'))
    cover = Image.open(str(list_pages[0]))
    width, height = cover.size
    pdf = FPDF(unit='pt', format=[width, height])
    for page in list_pages:
        pdf.add_page()
        pdf.image(str(page), 0, 0)
    pdf.output('%s.pdf' % _livro, 'F')
    for page in list_pages:
        os.remove(page)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Falta fornecer parâmetros!\n"
              "Sintaxe: ifcevd.py <número da matrícula> <endereco url do livro no bvu> [endereco url de outro livro] ..")
        exit()

    _, matricula, *book_list = sys.argv

    book_list = map(lambda i: i if (i.isdigit()) else re.match(r'(?:.*publications\/(\d+)|(\d+))', i).group(1), book_list)

    for livro_atual in book_list:
        #dump(matricula, livro_atual)
        make_pdf(livro_atual)
    print('operacao finalizada.')
