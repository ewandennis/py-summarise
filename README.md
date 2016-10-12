# Summarise: a simple recordset reporting tool

You have a list of structured records, maybe from JSON, JSONL, a DB extract, an event log.  Its big an you have no idea whats inside.  Summarise is an objective alternative to opening your blob in an editor and just staring.

Summarise will produce a report of each field found in a given record set, including values found, their frequency and with the ability to interpret fields given type hints.

## Example: Array of Dicts

```python
import sys, json

from summary import *

# Read JSONL record set 
with open(sys.argv[1], 'r') as f:
  recs = [json.loads(line) for line in f]

# Prepare some field type hints
hints = {
    'timestamp:' + str(UnicodeType): TimestampSummary
}

# Produce a summary of the data set 
fielddeets = summariseRecs(recs, hints=hints)

# Write the summary
print([deets['spec'] for fldkey, deets, in fielddeets.items()])

```

