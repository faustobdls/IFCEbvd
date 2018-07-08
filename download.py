# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

# Modify by: Fausto Blanco | UFERSA

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import urllib3
import sys
import re
import os

def whileZoom(phantom):
    zoom = 0
    while zoom <= 2:
        phantom.execute_script("document.getElementById('sunflower_zoom_bar').setAttribute('style', 'visibility: visible;')")
        phantom.find_element_by_css_selector('.zoom_btn.zoom_in').click()

        # phantom.execute_script("$('.zoom_btn.zoom_in').click()")
        zoom = phantom.execute_script('return parseInt(RDP.zoom.current)')
        print('atual zoom in = %s' % zoom)
        if zoom >= 3:
            phantom.get_screenshot_as_file('ss/error-1.png')
            break

def page_download(_url, _nome):
    try:
        print("tentando baixar %s" % _nome)
        # print("wget " + _url + " -o " + _nome)
        # os.system("wget " + _url + " -o " + _nome)
        print('curl %s > %s' % (_url, _nome)) # | "curl " + _url + " > " + _nome)
        os.system('curl %s > %s' % (_url, _nome)) # | "curl " + _url + " > " + _nome)
        # urllib.request.urlretrieve(_url, _nome)
    except:
        print('problemas ao baixar %s' % _nome)
    else:
        print('%s baixado' % _nome)


def dump(matricula, senha, quality, id_book):
    phantom = webdriver.Chrome()
    phantom.set_window_size(1366, 900) # set browser size.
    phantom.set_page_load_timeout(10)
    singin = 'https://ufersa.bv3.digitalpages.com.br/users/sign_in'

    # Login
    print('Logando no BVU com a matrícula %s...' % matricula)
    try:
        phantom.get(singin)
        phantom.find_element_by_id('user_login').send_keys(matricula)
        phantom.find_element_by_id('user_password').send_keys(senha)
        phantom.execute_script("$('input[name=commit]').click()")
        # phantom.find_element_by_css_selector('input[name=commit]').click()
        phantom.save_screenshot('ss/user_%s_ufersa_afterlogin.png' % matricula)
    except TimeoutException:
        print('Timeout durante o login... Refazendo-o...')
        return dump(matricula, senha, quality, id_book)

    # Obter informações do livro
    print('obtendo informacoes para o livro %s...' % id_book)
    try:
        print('try %s' % id_book)
        phantom.get('https://ufersa.bv3.digitalpages.com.br/users/publications/%s' % id_book)
    except TimeoutException as e:
        print('Timeout durante a coleta das informações do livro... Recomeçando tudo...')
        return dump(matricula, senha, quality, id_book)
    p_1 = 0
    count = 0
    location = phantom.execute_script('return document.location.href')
    if location == singin:
        print(location)
        print(singin)
        exit()
        
        
    # phantom.find_element_by_css_selector('.zoom_btn.zoom_in').click()
    # phantom.execute_script("$('.zoom_btn.zoom_in').click()")
    # phantom.execute_script("$('.zoom_btn.zoom_in').click()")
    # phantom.execute_script("$('.zoom_btn.zoom_in').click()")

    phantom.get_screenshot_as_file('ss/user_%s_ufersa_livro.png' % matricula)
    
    while p_1 == 0:
        try:
            p_1 = phantom.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
            # count = count + 1
            # print(count)
            if p_1 == 1:
                whileZoom(phantom)

                phantom.get_screenshot_as_file('ss/error-2.png')
                page_download(phantom.execute_script('return (RDP.reader.currentPages[0].portrait.zoom[%s])' % quality), 'book/[%s]%s-00000.jpg' % (quality, id_book))
        except:
            p_1 = 0
    num_pag = int(phantom.execute_script('return RDP.options.pageSetLength')) - 2
    print('numero de paginas: %s' % num_pag)
    
    # Download
    print('preparando para baixar livro id=%s com %d paginas...' % (id_book, num_pag))
    p0 = phantom.execute_script('return (RDP.reader.currentPages[0].portrait.zoom[%s])' % quality)
    page_download(p0, 'book/[%s]%s-00000.jpg' % (quality, id_book))
    
    phantom.get_screenshot_as_file('ss/user_%s_ufersa_capa_do_livro.png' % matricula)

    print('baixando livro...')
    phantom.execute_script('navigate.next_page()')
    _v_p1, _v_p2 = '', ''
    for i in range(1, num_pag, 2):
        # loop para esperar a pagina carregar
        p_1, p_2 = 0, 0

        while (p_1 == 0) or (p_2 == 0):
            try:
                whileZoom(phantom)

                p_1 = phantom.execute_script("if (RDP.reader.currentPages[0].portrait.zoom[%s]) { return 1 } else { return 0 }" % quality)
                p_2 = phantom.execute_script("if (RDP.reader.currentPages[1].portrait.zoom[%s]) { return 1 } else { return 0 }" % quality)
            except:
                p_1 , p_2 = 0, 0
        # carregou, pegar endereco
        _p1 = phantom.execute_script('return (RDP.reader.currentPages[0].portrait.zoom[%s])' % quality)
        _p2 = phantom.execute_script('return (RDP.reader.currentPages[1].portrait.zoom[%s])' % quality)
        # checa se ainda não carregou a nova pagina
        while (_p1 == _v_p1) or (_p2 == _v_p2):
            try:
                whileZoom(phantom)
                        
                _p1 = phantom.execute_script('return (RDP.reader.currentPages[0].portrait.zoom[%s])' % quality)
                _p2 = phantom.execute_script('return (RDP.reader.currentPages[1].portrait.zoom[%s])' % quality)
            except:
                pass
        # carregou nova, baixar...
        page_download(_p1, 'book/[%s]%s-%05d.jpg' % (quality, id_book, i))
        page_download(_p2, 'book/[%s]%s-%05d.jpg' % (quality, id_book, i+1))
        # ajusta os novos valores
        _v_p1, _v_p2 = _p1, _p2
        phantom.execute_script('navigate.next_page()')
        print('baixadas %d/%d paginas...' % (i,num_pag))

    # Finalização
    print('fim do dump')
    phantom.quit()


def make_pdf(_quality, _livro):
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
    pdf.output('books/[%s]_%s.pdf' % (_quality, _livro), 'F')
    for page in list_pages:
        os.remove(page)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Falta fornecer parâmetros!\n"
              "Sintaxe: download.py <funcao> <número da matrícula> <senha> <quality 0, 1 or 3> <endereco url do livro no bvu> [endereco url de outro livro] ..")
        exit()

    _, matricula, senha, quality, *book_list = sys.argv

    book_list = map(lambda i: i if (i.isdigit()) else re.match(r'(?:.*publications\/(\d+)|(\d+))', i).group(1), book_list)

    if quality == 2: # or quality >= 4:
        print("qualidade incorreta, use 0, 1 ou 3")
        exit()

    for livro_atual in book_list:
        dump(matricula, senha, quality, livro_atual)
        make_pdf(quality, livro_atual)
    print('operacao finalizada.')
