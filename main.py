from ast import parse
from jinja2.ext import Extension
import jinja2
from jinja2 import Template, StrictUndefined, DebugUndefined
from jinja2.lexer import Token

t1 = Template(open('sample_1.j2').read(), undefined=DebugUndefined)
s1 = t1.render(a='a', b='b', c=[1, 2])
print('------------------------')
print(s1)
print('------------------------')

s1 = t1.render()
print(s1)

from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2 import nodes

class PreserveExtension(Extension):

  """
  Example Input:

    this is plain text
    {%- preserve %}
    this is plain text
    {{ a }}
    {%- if b %}{{ b }}{% endif -%}
    {% for i in c -%}
      {{ i }}
    {%- endfor %}
    {%- endpreserve %}

  Example Output:

    this is plain text
    this is plain text
    {{ a }}{%- if b %} {{ b }} {% endif -%}
    {% for i in c -%}
      {{ i }}{%- endfor %}
  """

  # a set of names that trigger the extension.
  tags = {"preserve"}

  def parse(self, parser: Parser):
    lineno = parser.stream.current.lineno
    parser.parse_expression()
    parser.stream.skip()
    body = []
    raw = []
    def flush():
      nonlocal raw
      nonlocal body
      node = nodes.TemplateData(''.join(raw))
      body.append(node)
      raw = []

    while True:
      t: Token = next(parser.stream)
      if t.lineno != lineno:
        flush()
        lineno = t.lineno
      test = t.test('name:endpreserve')
      if test:
        raw.pop(-1)
        break
      # if raw and not raw[-1].endswith('\n'):
      if t.type in ('name', 'block_end', 'variable_end'):
        raw.append(' ')
      raw.append(t.value)
    if raw:
      flush()
    return body

t1 = Template(open('sample_2.j2').read(), extensions=[PreserveExtension])
s1 = t1.render(a='a', b='b', c=[1, 2])
print('------------------------')
print(s1)
print('------------------------')

t1 = Template(s1)
s1 = t1.render(a='a', b='b', c=[1, 2])
print('------------------------')
print(s1)
print('------------------------')
