# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

from selenium import webdriver
import urllib, hashlib, sys, platform, random, re

def _baixa(_url,_nome):
  try:
    urllib.request.urlretrieve(_url, _nome)
  except:
    print('problemas ao baixar %s' % _nome)
  else:
    print('%s baixado' % _nome)

_hash = lambda _mat: 'login=%s&token=%s' % (_mat, hashlib.md5(('%sQJEkJM2iLJiAj6LScxsZivml54SmzSy0' % _mat).encode()).hexdigest())
# Matricula: Ano|Semestre|Curso|Numero crescente
_matricula = lambda: '%s%s%05d%04d'%\
                     (random.randrange(2012, 2016), random.randrange(1, 3), random.choice(['01106', '01101', '1222']), random.randrange(100, 270))

def _dump(id_livro):
  b=webdriver.PhantomJS()
  print('gerando cookie de login para nova matricura aleatoria...')
  b.get('http://ifce.bv3.digitalpages.com.br/user_session/authentication_gateway?%s' % _hash(_matricula))
  print('obtendo informacoes para o livro %s...' % id_livro)
  b.get('http://ifce.bv3.digitalpages.com.br/users/publications/%s' % id_livro)
  p_1 = 0
  while(p_1 == 0):
    try:
      p_1 = b.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
    except:
      p_1 = 0
  num_pag = int(b.execute_script("return RDP.options.pageSetLength")) - 2
  print('preparando para baixar livro id=%s com %d paginas...' % (id_livro, num_pag))
  _baixa(b.execute_script("return $('.backgroundImg')[0].src"), "%s-00000.jpg" % id_livro)
  print('baixando livro...')
  b.execute_script("navigate.next_page()")
  _v_p1, _v_p2 = '', ''
  for i in range(1, num_pag, 2):
    # loop para esperar a pagina carregar
    p_1 , p_2 = 0, 0
    while ((p_1==0) or (p_2==0)):
      try:
        p_1 = b.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
        p_2 = b.execute_script("if ($('.backgroundImg')[1]) { return 1 } else { return 0 }")
      except:
        p_1 , p_2 = 0, 0
    # carregou, pegar endereco
    _p1 = b.execute_script("return $('.backgroundImg')[0].src")
    _p2 = b.execute_script("return $('.backgroundImg')[1].src")
    # checa se ainda não carregou a nova pagina
    while((_p1 == _v_p1) or (_p2 == _v_p2)):
      try:
        _p1 = b.execute_script("return $('.backgroundImg')[0].src")
        _p2 = b.execute_script("return $('.backgroundImg')[1].src")
      except:
        pass
    # carregou nova, baixar...
    _baixa(_p1, "%s-%05d.jpg" % (id_livro, i))
    _baixa(_p2, "%s-%05d.jpg" % (id_livro, i+1))
    # ajusta os novos valores
    _v_p1 , _v_p2 = _p1 , _p2
    b.execute_script("navigate.next_page()")
    print('baixadas %d/%d paginas...' % (i,num_pag))
  print('fim do dump')
  b.quit()

def _gerapdf(_livro):
  # usando a ferramenta convert do ImageMagick
  print('convertendo para PDF...')
  import os
  soCorrente = platform.system()
  if (soCorrente == 'Linux'):
    os.system('convert *.jpg %s.pdf' % _livro)
    print('limpando os jpgs residuais...')
    os.system('rm *.jpg')
  elif (soCorrente == 'Windows'):
    from fpdf import FPDF
    from PIL import Image
    import glob
    listPages = glob.glob('*.jpg')
    cover = Image.open(str(listPages[0]))
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    for page in listPages:
      pdf.add_page()
      pdf.image(str(page), 0, 0)

    pdf.output("%s.pdf" % _livro, "F")

    del cover
    for page in listPages:
      os.remove(page)
  else:
    print('nao e possivel gerar pdf nesse sistema')

if __name__ == "__main__":
  listaLivros = sys.argv
  del listaLivros[0]

  if (len(listaLivros) == 0):
    print("Erro! Falta fornecer os livros a serem baixados!\n"
          "Sintaxe: ifcevd.py <endereco url do livro no bvu> [endereco url de outro livro] ..")
    exit()

  listaLivros = map(lambda i: i if (i.isdigit()) else re.match(r"(?:.*publications\/(\d+)|(\d+))", i).group(1), listaLivros)

  for livroAtual in listaLivros:
    _dump(livroAtual)
    _gerapdf(livroAtual)
  print('operacao finalizada.')
