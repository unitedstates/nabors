import os
import sys

import boto3
import jinja2

import render

region_name = 'us-east-1'
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

if not aws_access_key_id or not aws_secret_access_key:
  print('ERROR: Specify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the '
        'shell env', file=sys.stderr)
  sys.exit(1)

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

# The contents of the HTML template are replaced with values from the
# hit_input.jsonlines file. Then, this entire HTML document is inserted into the
# XML template, as the contents of an Amazon Mturk "HTMLQuestion" element
question_xml_tmpl = jinja2.Template(open('templates/question.xml').read())

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Five random pages for testing
for page_num in range(250, 256):
  question_html = render.render(page_num)
  question_xml = question_xml_tmpl.render(html_data=question_html)
  resp = client.create_hit(
    MaxAssignments=2,
    LifetimeInSeconds=60 * 60 * 24 * 14,
    AssignmentDurationInSeconds=60 * 60,
    Reward='0.10',
    Title='Verify OCR pages of tables of United States legislative data',
    Keywords='ocr,verification,table,legislation',
    Description=('A PNG image of a page out of a book of legislative data '
                 'tables is presented, alongside data that has been retrieved '
                 'from these images using OCR (Optical Character Recognition). '
                 'The task is to verify that the OCR data is either Accurate '
                 'or Inaccurate.'),
    Question=question_xml,
    UniqueRequestToken='NABORS-%s' % str(page_num).rjust(4, '0')
)
