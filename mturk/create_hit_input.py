from collections import defaultdict
import csv
import json
import sys

def unformat_date(date):
  try:
    return '%s-%s-%s' % (date[6], date[8:10], date[2:4])
  except IndexError:
    print(date, len(date))
    raise

in_path = 'table.csv'
if len(sys.argv) >= 2:
  in_path = sys.argv[1]

out_path = 'hit_input.jsonlines'
if len(sys.argv) == 3:
  out_path = sys.argv[2]

print('input: %s, output: %s' % (in_path, out_path), file=sys.stderr)

output = []
header_row = ['image_url']
header_row.extend('line_%s' % i for i in range(43))

lines = defaultdict(lambda: [])
for row in csv.reader(open(in_path)):
  try:
    int(row[0])
    lines[row[0]].append(row)
  except ValueError:
    pass

for page, pagelines in lines.items():
  pagekey = str(int(page) + 20).rjust(3, '0')
  nextlines = []
  nextrow = {
    'image_url': ('https://s3.amazonaws.com/images.nabors.0-z-0.com/png/'
                  'page-%s.png' % pagekey),
    'lines': nextlines
  }
  for line in pagelines:
    if len(line) != 11 or line[-1] == 'ERROR':
      nextline = 'ERROR'.ljust(58)
    else:
      stat_page = line[5]
      if line[6]:
        stat_page += '-' + line[6]
      try:
        nextline = (
          line[2].rjust(4) + line[3].rjust(10) + line[4].rjust(10) +
          stat_page.rjust(10) + unformat_date(line[7]).rjust(12) + '  ' +
          line[8] + line[9].rjust(10 - len(line[8]))
        )
      except (IndexError, Exception):
        print(line)
        raise
    nextlines.append(nextline)
  output.append(json.dumps(nextrow))

outfile = open(out_path, 'w')
for row in output:
  outfile.write('%s\n' % row)
