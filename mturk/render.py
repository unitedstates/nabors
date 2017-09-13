import json

import jinja2

page_data = []
with open('hit_input.jsonlines') as page_file:
  for line in page_file:
    page_data.append(json.loads(line))

def render(page_num):
  page = page_data[page_num - 1]
  javascript = open('templates/question.js').read()
  css = open('templates/question.css').read()
  question_html_tmpl = jinja2.Template(open('templates/question.html').read())
  return question_html_tmpl.render(page=page, page_num=page_num,
                                   javascript=javascript, css=css)

def render_all():
  for page_num, page in enumerate(page_data):
    yield render(page_num)
