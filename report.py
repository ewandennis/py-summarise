"""Summarise SparkPost eventlog entries"""

import sys

from summary import *

def main():
  inpath = sys.argv[1]
  hints = {
      'timestamp:' + str(UnicodeType): TimestampSummary
  }
  with open(inpath, 'r') as f:
    recs = [eval(line) for line in f]
  fielddeets = summariseRecs(recs, hints=hints)
  print('# records: %s' % len(recs))
  print([deets['spec'] for fldkey, deets, in fielddeets.items()])

if __name__ == '__main__':
  main()

# vim: ts=2 expandtab shiftwidth=2 softtabstop=2

