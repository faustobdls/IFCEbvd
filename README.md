# IFCEbvd
## IFCE Biblioteca Virtual Downloader

Ferramenta de download de livros da biblioteca virtual do IFCE. Baixa página a página como imagem e depois converte para pdf.

## Dependências
### Linux
- Python3: sudo apt-get install python3
- Biblioteca do Python Selenium: sudo pip3 install selenium
- PhantonJS: sudo apt-get install phantomjs
- Imagemagick: sudo apt-get install imagemagick

### Windows
- Python3: https://www.python.org/downloads/
- Biblioteca do Python Selenium: pip install selenium
- Biblioteca do Python fpdf: pip install fpdf
- Biblioteca do Python pil: pip install pillow
- PhantomJS: http://phantomjs.org/ (deixe o binário na mesma pasta do script)

## Uso
1. Abra o termina/cmd na pasta em que se localiza o script
2. No Windows, use o comando `ifcevd.py <endereco url do livro no bvu> [endereco url de outro livro] ..`, no Linux, use `py3 ifcevd.py <endereco url do livro no bvu> [endereco url de outro livro] ..`. O endereço a ser fornecido é o mesmo do navegador. Pode-se fornecer quantos livros quiser.
