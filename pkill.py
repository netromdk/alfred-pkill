#!/usr/bin/python
# encoding: utf-8

from __future__ import unicode_literals

import os
import sys
import subprocess
import re

from workflow import Workflow3, ICON_NOTE

# "PID STAT COMMAND"
PROC_REGEX = re.compile(r'(\d+?)\s+(.+?)\s+(.+)')

# Returns a list of tuples (PID, COMMAND).
def user_processes():
  output = subprocess.check_output('ps x -o pid,stat,command; exit 0',
                                   stderr = subprocess.STDOUT, shell = True)
  output = wf.decode(output)
  results = []
  for line in output.split('\n'):
    match = PROC_REGEX.match(line.strip())
    if match:
      # TODO: exclude zombies
      results.append(match.group(1, 3))
  return results

def search(text, wf):
  procs = user_processes()

  # Filter on process names.
  procs = wf.filter(text, procs, key = lambda p: p[1], min_score = 80, max_results = 50)

  # Remove our own process.
  pid = unicode(os.getpid())
  for i in range(len(procs)):
    val = procs[i]
    if pid == val[0]:
      del(procs[i])
      break

  return procs

def main(wf):
  args = wf.args
  text = args[0].strip().lower()

  results = search(text, wf)

  if len(results) == 0:
    wf.add_item(title = 'No results found.. Try with another query.', icon = ICON_NOTE)

  for result in results:
    wf.add_item(title = result[1], subtitle = 'Action: kill -TERM {}'.format(result[0]),
                arg = result[0], valid = True)

  wf.send_feedback()

if __name__ == '__main__':
  wf = Workflow3()
  sys.exit(wf.run(main))
