import csv
from collections import defaultdict

def unformat_date(date):
  try:
    return '%s-%s-%s' % (date[6], date[8:10], date[2:4])
  except IndexError:
    print(date, len(date))
    raise

output = csv.writer(open('hit_input.csv', 'w', newline=''))
header_row = ['image_url']
header_row.extend('line_%s' % i for i in range(43))
output.writerow(header_row)

lines = defaultdict(lambda: [])
for row in csv.reader(open('table.csv')):
  try:
    int(row[0])
    lines[row[0]].append(row)
  except ValueError:
    pass

for page, pagelines in lines.items():
  pagekey = str(int(page) + 20).rjust(3, '0')
  nextrow = [
    'https://s3.amazonaws.com/images.nabors.0-z-0.com/png/page-%s.png' % 
    pagekey
  ]
  for line in pagelines:
    if len(line) != 11 or line[-1] == 'ERROR':
      nextrow.append('')
      continue

    stat_page = line[5]
    if line[6]:
      stat_page += '-' + line[6]
    try:
      nextline = (
        line[2].rjust(4) + line[3].rjust(10) + line[4].rjust(10) +
        stat_page.rjust(10) + unformat_date(line[7]).rjust(10) + '  ' +
        line[8] + line[9].rjust(10 - len(line[8]))
      )
    except (IndexError, Exception):
      print(line)
      raise
    nextrow.append(nextline)
  output.writerow(nextrow)
