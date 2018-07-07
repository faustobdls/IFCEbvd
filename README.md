# UFERSA DigitalPages
## DigitalPages Biblioteca Virtual Downloader

Ferramenta de download de livros da biblioteca virtual da DigitalPages. Baixa página a página como imagem e depois converte para pdf.
<a href="http://macalogs.com.br/estudo-de-caso-baixando-livros-de-uma-biblioteca-virtual/">Veja esse estudo de caso para saber como ela foi desenvolvida.</a> escrito pelo desenvolvedor que iniciou o projeto.

## Dependências
- Biblioteca do Python Selenium: `sudo pip3 install selenium`
- Biblioteca do Python fpdf: `sudo pip3 install fpdf`
- Biblioteca do Python pillow: `sudo pip3 install pillow`
- PhantonJS: <a href="http://phantomjs.org/download.html"> Download Page in phantonjs.org</a>

## Receita pre-execução
1. Adicione o python ao path do S.O. para que seja fácil executar os comandos
2. Adicione o phantonjs ao path do S.O. porque foi desenvolvido pensando nisso

## Explicando as pastas e arquivos
1. download.py é o responsável por fazer o serviço completo, ele faz o login, acessa todas as paginas, baixa, coloca na pasta, cria o PDF, e apaga as paginas baixadas...
2. pdf.py foi criado para criar o pdf caso por algum motivo o processo tenha falhado e as paginas já tenham sido baixadas, basta usar o comando `pdf.py <id do livro> [outros ids]` para usá-lo...
3. book é a pasta onde ele fará o download das páginas
4. books é onde ele salvará os arquivos pdf com o id do livro (no futuro vou tentar por com o título)


## Uso
**Windows**
1. Abra o CMD na pasta em que se localiza o script
2. Use o comando: `download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`.

**Linux**
1. Abra o terminal na pasta em que se localiza o script
2. Use o comando: `py3 download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`. 

**Mac-OSX**
1. Abra o terminal na pasta em que se localiza o script
2. Use o comando: `python3 download.py <números, e somente os numeros, de sua matrícula> <senha> <endereco url do livro no bvu> [endereco url de outro livro] ..`.
***OBS:** O endereço a ser fornecido é o mesmo do navegador. Pode-se fornecer quantos livros quiser.*
