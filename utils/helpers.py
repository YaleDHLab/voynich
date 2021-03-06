from collections import defaultdict, Counter
import codecs, warnings, os
warnings.filterwarnings('ignore')

def parse_pages():
  '''
  Return a mapping from single character representation of transcriptor to
  array of line strings.
  @kwarg str path: the path to the voynich full text
  @returns
    [str] page_order: a list of the page keys in order
    dict d: # d[annotator][page] = ['line_one', 'line_two']
  '''
  page_order = []
  d = defaultdict(lambda: defaultdict(list))
  path = os.path.join(__file__.replace('helpers.py', 'text16e6.evt'))
  if path[-1] == 'c':
    path = ''.join(path[:-1])
  with codecs.open(path, 'r', 'latin1') as f:
    f = f.read()
    for line_idx, line in enumerate(f.split('\n')):
      if not line.strip(): continue
      if line[0] != '<': continue # skip paratextual lines
      meta = line.split('<')[1].split('>')[0]
      if '.' not in meta: # indicates the start of a new page (e.g. <f1r>)
        page_order.append(meta)
        continue
      page, sheet, line_num_and_annotator = meta.split('.')
      line_num, annotator = line_num_and_annotator.split(';')
      if '>' not in line: continue
      if not page: continue # skip the page id 0
      line_text = line.split('>')[1].strip()
      d[annotator][page].append(line_text)
  return page_order, d

page_order, line_map = parse_pages()

# select the annotator to use (Takahashi)
annotator = 'H'

# set page array
pages = line_map[annotator]