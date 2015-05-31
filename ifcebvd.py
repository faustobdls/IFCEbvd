# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia do Ceará
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

from selenium import webdriver
import urllib, hashlib, sys, platform, argparse
import misc

def _baixa(_url,_nome):
  try:
    urllib.request.urlretrieve(_url, _nome)
  except:
    print('problemas ao baixar %s' % _nome)
  else:
    print('%s baixado' % _nome)

_hash = lambda _mat: 'login=%s&token=%s' % (_mat, hashlib.md5(('%sQJEkJM2iLJiAj6LScxsZivml54SmzSy0' % _mat).encode()).hexdigest())

def _dump(matricula, id_livro):
  b=webdriver.PhantomJS()
  print('gerando cookie de login para matricura %s...' % matricula)
  b.get('http://ifce.bv3.digitalpages.com.br/user_session/authentication_gateway?%s' % _hash(matricula))
  print('inicializando...')
  b.get('http://ifce.bv3.digitalpages.com.br/users/publications/%s' % id_livro)
  print('obtendo informacoes para o livro %s...' % id_livro)
  p_1 = 0
  while(p_1 == 0):
    try:
      p_1 = b.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
    except:
      p_1 = 0
  num_pag = 7 #int(b.execute_script("return RDP.options.pageSetLength")) - 2
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
  soCorrente = platform.system()
  if (soCorrente == 'Linux'):
    import os
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
  else:
    print('nao e possivel gerar pdf nesse sistema')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--matricula', '-m',
            help='Matricula para acessar o BVU (apenas numeros).'
                 'Caso nao seja fornecida, sera gerada uma matricula aleatoria')
  parser.add_argument('--livro', '-l', required=True,
            help='ID do livro que será baixado.'
                 'Para descobrir qual o ID do livro que deseja baixar, acesse-o no navegador'
                 'e veja na barra de endereco os numeros apos o \'publications\'')
  args = parser.parse_args()

  if (args.matricula):
    matricula = args.matricula
  else:
    matricula = misc.gerarMatricula()
    print('nao foi fornecida uma matricula, entao sera usada a %s, gerada aleatorialmente' % matricula)

  _dump(matricula, args.livro)
  _gerapdf(args.livro)
  print('operacao finalizada.')
