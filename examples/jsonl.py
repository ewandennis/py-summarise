import sys, types, json

from summary import *

# Read JSONL record set 
with open(sys.argv[1], 'r') as f:
  recs = [json.loads(line) for line in f]

# Prepare some field type hints
hints = {
    'timestamp:' + str(IntType): TimestampSummary
}

# Produce a summary of the data set 
fielddeets = summariseRecs(recs, hints=hints)

# Write the summary
print('\n'.join([str(deets['spec']) for fldkey, deets, in fielddeets.items()]))
