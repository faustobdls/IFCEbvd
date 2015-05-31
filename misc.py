import random

# TODO: Não gera todos os tipos de matrículas possíveis, mas só os equivalentes a alguns cursos, e nem sempre existente
def gerarMatricula():
  ano = str(random.randrange(2012, 2016))
  semestre = str(random.randrange(1, 3))
  curso = random.choice(['01106', '01101', '1222']).zfill(5)
  ultimosDigitos = str(random.randrange(100, 270)).zfill(4)

  return ano + semestre + curso + ultimosDigitos