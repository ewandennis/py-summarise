"""Summarise field content in a collection of structured records"""

from datetime import datetime
from types import *

class IntSummary:
  BIG=2**64
  SMALL=-2**64
  def __init__(self, fldspec):
    self.fldspec = fldspec
    fldspec['lo'] = IntSummary.BIG 
    fldspec['hi'] = IntSummary.SMALL
  def update(self, val):
    val = int(val)
    self.fldspec['lo'] = min(self.fldspec['lo'], val)
    self.fldspec['hi'] = max(self.fldspec['hi'], val)
  def __repr__(self):
    return '%s\n\t(%d, %d)' % (self.fldspec['fldname'], self.fldspec['lo'], self.fldspec['hi'])

class TimestampSummary(IntSummary):
  def __repr__(self):
    lo = datetime.fromtimestamp(self.fldspec['lo'])
    hi = datetime.fromtimestamp(self.fldspec['hi'])
    return '%s\n\t%s -> %s\n' % (self.fldspec['fldname'], lo, hi)

class StrSummary(object):
  def __init__(self, fldspec, top=10):
    self.fldspec = fldspec
    self.fldspec['options'] = {}
    self.top = top
  def update(self, val):
    options = self.fldspec['options']
    if not val in options:
      options[val] = 1
    else:
      options[val] += 1
  def __repr__(self): 
    histo = [(k, v) for k, v in self.fldspec['options'].items()]
    histo.sort(key=lambda rec: rec[1], reverse=True)
    if self.top:
      histo = histo[0:self.top]
    histostr = '\n'.join(['\t%s: %d' % (k, v) for k, v in histo] )
    return '%s\n%s\n' % (self.fldspec['fldname'], histostr)

class NullSummary(object):
  def __init__(self, fldspec):
    self.fldspec = fldspec
    pass
  def update(self, val):
    pass
  def __repr__(self):
    return self.fldspec['fldname']

def summariseRecs(recs, hints=None):
  summaries = {
    str(IntType): IntSummary,
    str(StringType): StrSummary,
    str(UnicodeType): StrSummary
  }

  fielddeets = {}
  if hints:
    for fldspec, spec in hints.items():
      fldname = fldspec.split(':')[0]
      deets = dict(fldname=fldname)
      deets['spec'] = spec(deets)
      fielddeets[fldspec] = deets

  for rec in recs:
    for fldname in rec.keys():
      val = rec[fldname]
      fldtype = type(val)
      fldtypestr = str(fldtype)
      key = fldname + ':' + fldtypestr
      if not key in fielddeets:
        deets = dict(fldname=fldname)
        if fldtypestr in summaries:
          deets['spec'] = summaries[fldtypestr](deets)
        else:
          print('No summary type for $s' % filetypestr)
          deets['spec'] = NullSummary(deets)
        fielddeets[key] = deets
      deets = fielddeets[key]
      if 'spec' in deets:
        deets['spec'].update(val)
  return fielddeets

