# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

from selenium import webdriver
import urllib
import hashlib
import sys
import platform
import re


def _baixa(_url, _nome):
    try:
        urllib.request.urlretrieve(_url, _nome)
    except:
        print('problemas ao baixar %s' % _nome)
    else:
        print('%s baixado' % _nome)

_hash = lambda _mat: 'login=%s&token=%s' % (_mat, hashlib.md5(('%sQJEkJM2iLJiAj6LScxsZivml54SmzSy0' % _mat).encode()).hexdigest())


def _dump(matricula, id_livro):
    phantom = webdriver.PhantomJS()
    print('gerando cookie de login para matricura %s...' % matricula)
    phantom.get('http://ifce.bv3.digitalpages.com.br/user_session/authentication_gateway?%s' % _hash(matricula))
    print('obtendo informacoes para o livro %s...' % id_livro)
    phantom.get('http://ifce.bv3.digitalpages.com.br/users/publications/%s' % id_livro)
    p_1 = 0
    while p_1 == 0:
        try:
            p_1 = phantom.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
        except:
            p_1 = 0
    num_pag = int(phantom.execute_script('return RDP.options.pageSetLength')) - 2
    print('preparando para baixar livro id=%s com %d paginas...' % (id_livro, num_pag))
    _baixa(phantom.execute_script("return $('.backgroundImg')[0].src"), '%s-00000.jpg' % id_livro)
    print('baixando livro...')
    phantom.execute_script('navigate.next_page()')
    _v_p1, _v_p2 = '', ''
    for i in range(1, num_pag, 2):
        # loop para esperar a pagina carregar
        p_1 , p_2 = 0, 0
        while ((p_1==0) or (p_2==0)):
            try:
                p_1 = phantom.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
                p_2 = phantom.execute_script("if ($('.backgroundImg')[1]) { return 1 } else { return 0 }")
            except:
                p_1 , p_2 = 0, 0
        # carregou, pegar endereco
        _p1 = phantom.execute_script("return $('.backgroundImg')[0].src")
        _p2 = phantom.execute_script("return $('.backgroundImg')[1].src")
        # checa se ainda não carregou a nova pagina
        while((_p1 == _v_p1) or (_p2 == _v_p2)):
            try:
                _p1 = phantom.execute_script("return $('.backgroundImg')[0].src")
                _p2 = phantom.execute_script("return $('.backgroundImg')[1].src")
            except:
                pass
        # carregou nova, baixar...
        _baixa(_p1, '%s-%05d.jpg' % (id_livro, i))
        _baixa(_p2, '%s-%05d.jpg' % (id_livro, i+1))
        # ajusta os novos valores
        _v_p1, _v_p2 = _p1, _p2
        phantom.execute_script('navigate.next_page()')
        print('baixadas %d/%d paginas...' % (i,num_pag))
    print('fim do dump')
    phantom.quit()


def _gerapdf(_livro):
    # usando a ferramenta convert do ImageMagick
    print('convertendo para PDF...')
    import os
    so_corrente = platform.system()
    if so_corrente == 'Linux':
        os.system('convert *.jpg %s.pdf' % _livro)
        print('limpando os jpgs residuais...')
        os.system('rm *.jpg')
    elif so_corrente == 'Windows':
        from fpdf import FPDF
        from PIL import Image
        import glob
        listPages = glob.glob('*.jpg')
        cover = Image.open(str(listPages[0]))
        width, height = cover.size
        pdf = FPDF(unit = 'pt', format = [width, height])
        for page in listPages:
            pdf.add_page()
            pdf.image(str(page), 0, 0)
        pdf.output('%s.pdf' % _livro, 'F')
        del cover
        for page in listPages:
            os.remove(page)
    else:
        print('nao e possivel gerar pdf nesse sistema')


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta fornecer parâmetros!\n"
              "Sintaxe: ifcevd.py <número da matrícula> <endereco url do livro no bvu> [endereco url de outro livro] ..")
        exit()

    _, matricula, *lista_livros = sys.argv

    lista_livros = map(lambda i: i if (i.isdigit()) else re.match(r'(?:.*publications\/(\d+)|(\d+))', i).group(1), lista_livros)

    for livro_atual in lista_livros:
        _dump(matricula, livro_atual)
        _gerapdf(livro_atual)
    print('operacao finalizada.')
