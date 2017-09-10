import json

import jinja2

def render(page_num):
  page_data = []
  with open('hit_input.jsonlines') as page_file:
    for line in page_file:
      page_data.append(json.loads(line))

  javascript = open('templates/question.js').read()
  css = open('templates/question.css').read()

  page = page_data[page_num - 1]
  question_html_tmpl = jinja2.Template(open('templates/question.html').read())
  return question_html_tmpl.render(page=page, javascript=javascript, css=css)
  
