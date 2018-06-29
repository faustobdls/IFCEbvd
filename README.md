# UFERSA DigitalPages
## DigitalPages Biblioteca Virtual Downloader

Ferramenta de download de livros da biblioteca virtual da DigitalPages. Baixa página a página como imagem e depois converte para pdf.
<a href="http://macalogs.com.br/estudo-de-caso-baixando-livros-de-uma-biblioteca-virtual/">Veja esse estudo de caso para saber como ela foi desenvolvida.</a> escrito pelo desenvolvedor que iniciou o projeto.

## Dependências
- Biblioteca do Python Selenium: `sudo pip3 install selenium`
- Biblioteca do Python fpdf: `sudo pip3 install fpdf`
- PhantonJS: `sudo apt-get install phantomjs`

## Uso
**Windows**
1. Abra o CMD na pasta em que se localiza o script
2. Use o comando: `download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`.

**Linux**
1. Abra o terminal na pasta em que se localiza o script
2. Use o comando: `py3 download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`. 

**Mac-OSX**
1. Abra o terminal na pasta em que se localiza o script
2. Use o comando: `/usr/local/bin/python3 download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`.
***OBS:** O endereço a ser fornecido é o mesmo do navegador. Pode-se fornecer quantos livros quiser.*
