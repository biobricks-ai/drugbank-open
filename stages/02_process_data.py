# Imports
# -------
import re
import os
import gzip
import pathlib
import pandas as pd

extensions = ['zip']
extensions_re = re.compile(r'\.(' + '|'.join(re.escape(ext) for ext in extensions) + r')$')

files = filter( lambda item: item.is_file(), pathlib.Path('download').rglob('*') )

brick_dir = pathlib.Path('brick')
brick_dir.mkdir(exist_ok=True)

for file in files:
  out_basename = re.sub(extensions_re, '.parquet', file.name )
  out_file = brick_dir / file.relative_to('download').with_name( out_basename )

  file = str(file)

  if file.endswith('.gz'):
    with gzip.open(file, 'rb') as file_in:
      lines = file_in.read().decode("utf-8").split('\n')
      data = [ line.split('\t') for line in lines ]
      headers = data.pop(0)
      df = pd.DataFrame(data, columns=headers)
      df.to_parquet(out_file)

  else:
    raise Exception('Unknown File Found: %s' % file)


