import re
import textwrap

# Definimos los patrones de tokens usando expresiones regulares
TOKEN_PATTERNS = [
    ('NUMBER', r'\d+(\.\d+)?'),   # Números enteros o decimales
    ('PLUS', r'\+'),              # Suma
    ('MINUS', r'-'),              # Resta
    ('TIMES', r'\*'),             # Multiplicación
    ('DIVIDE', r'/'),             # División
    ('LPAREN', r'\('),            # Paréntesis izquierdo
    ('RPAREN', r'\)'),            # Paréntesis derecho
    ('WHITESPACE', r'\s+'),       # Espacios en blanco (serán ignorados)
    ('OPERATOR', r'(?i)\b(si|entonces|sino|cada|mientras|entero|decimal|en)\b|>|<'),  # Operadores (case insensitive)
    ('FUNCTION', r'\b(ver|meter|sacar)\b'),  # Funciones
    ('VARIABLE', r'[a-zA-Z_0-9]*'),  # Variables
]

# Función principal del analizador léxico


def lexer(code):
  tokens = []
  pos = 0
  while pos < len(code):
    match = None

    for token_type, pattern in TOKEN_PATTERNS:
      regex = re.compile(pattern)
      match = regex.match(code, pos)

      if match:
        text = match.group(0)

        if token_type == 'OPERATOR' and any((char.isupper() for char in text)):  # Ignoramos las variables
          raise SyntaxError(f'Operador escrito incorrectamente: {text}')

        if token_type != 'WHITESPACE':  # Ignoramos los espacios en blanco
          tokens.append((token_type, text))
        pos = match.end(0)
        break

    if not match:
      raise SyntaxError(f'Caracter no reconocido: {code[pos]}')
  tokens.append(('EOF', None))
  return tokens


# Ejemplo de uso
code = textwrap.dedent("""
                       si obed > 10 entonces
                         ver(obed)
                        sino
                        ver(chochi)
                       """)
tokens = lexer(code)
for token in tokens:
  print(token)
