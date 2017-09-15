from collections import defaultdict
import csv
import json
import sys
import jinja2
from num2words import num2words

def unformat_date(date):
  if len(date) == 4: return date # just year is known
  return '%2d-%s-%s' % (int(date[5:7]), date[8:10], date[2:4])

def load_pages():
  # Load table.csv and group the rows by page number, which is in
  # the first column.
  pages = defaultdict(lambda: [])
  for row in csv.reader(open("../table.csv")):
    if row[0] == "nabors-page": continue # skip header row
    pages[int(row[0])].append(row)
  return pages

def get_page(pages, page):
  # How many acts/resolutions on this page?
  how_many = defaultdict(lambda : 0)
  for line in pages[page]:
    if "ERROR" in line: continue
    how_many[line[8] in ("HR", "S")] += 1

  # form template context
  ret = {
    # temporary URL holding the image of the page
    'image_url': ('https://s3.amazonaws.com/images.nabors.0-z-0.com/png/'
                  'page-%s.png' % str(page + 20).rjust(3, '0')),
    'lines': []
  }
  last_header = None
  for line in pages[page]:
    if len(line) != 11 or line[-1] == 'ERROR':
      nextline = " ".join(line[0:11]).ljust(58)
    else:
      header = (line[0], line[8] in ("HR", "S"))
      if header != last_header:
        ret["lines"].append(
          (
            ("PUBLIC ACT" if header[1] else "RESOLUTION")
          + ("S" if how_many[header[1]] > 1 else "")
          + " OF THE "
          + num2words(int(line[1]), ordinal=True).upper()
          + " CONGRESS"
          ).center(58)
        )
        last_header = header

      stat_page = line[5]
      if line[6]:
        stat_page += '-' + line[6]
      nextline = (
        line[2].rjust(4) + line[3].rjust(10) + line[4].rjust(10) +
        stat_page.rjust(10) + unformat_date(line[7]).rjust(12) + '  ' +
        line[8] + line[9].rjust(10 - len(line[8]))
      )
    ret["lines"].append(nextline)
  return ret

def render(page_num):
  page = get_page(load_pages(), page_num)
  javascript = open('templates/question.js').read()
  css = open('templates/question.css').read()
  question_html_tmpl = jinja2.Template(open('templates/question.html').read())
  return question_html_tmpl.render(page=page, page_num=page_num,
                                   javascript=javascript, css=css)

def render_all():
  for page_num, page in enumerate(page_data):
    yield render(page_num)
