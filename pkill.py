#!/usr/bin/python
# encoding: utf-8

from __future__ import unicode_literals

import os
import sys
import subprocess
import re

from workflow import Workflow3, ICON_NOTE, ICON_BURN, ICON_SYNC

# "PID STAT COMMAND"
# Only match sane values for the commands.
PROC_REGEX = re.compile(r'(\d+?)\s+(.+?)\s+([\w\d\s\-\\\/\.:;,]+)')

log = None

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
  log.debug('#procs: "{}"'.format(len(procs)))

  # Filter on process names.
  log.debug('filtering..')
  procs = wf.filter(text, procs, key = lambda p: p[1], min_score = 80, max_results = 50)
  log.debug('#filtered: "{}"'.format(len(procs)))

  # Remove our own process.
  pid = unicode(os.getpid())
  for i in range(len(procs)):
    val = procs[i]
    if pid == val[0]:
      log.debug('found and removed ourself: "{}"'.format(val))
      del(procs[i])
      break

  return procs

def kill_args(sig_arg, pid):
  return '{} {}'.format(sig_arg, pid)

def main(wf):
  if wf.update_available:
    wf.add_item('New version available',
                'Action this item to install the update',
                autocomplete = 'workflow:update', icon = ICON_SYNC)

  args = wf.args

  all_mode = (args[0].strip().lower() == 'all')
  log.debug('all_mode: "{}"'.format(all_mode))

  text = args[1].strip().lower()
  log.debug('input: "{}"'.format(text))

  results = search(text, wf)
  log.debug('#results: "{}"'.format(len(results)))

  if len(results) == 0:
    wf.add_item(title = 'No results found.. Try with another query.', icon = ICON_NOTE)

  pids = ' '.join(p[0] for p in results) if all_mode else ''

  for result in results:
    if not all_mode:
      pids = result[0]
    item = wf.add_item(title = result[1], subtitle = 'Action: kill -TERM {}'.format(pids),
                       arg = kill_args('-TERM', pids), valid = True, icon = ICON_BURN)
    item.add_modifier(key = 'alt', subtitle = 'Action: kill -KILL {}'.format(pids),
                      arg = kill_args('-KILL', pids))
    item.add_modifier(key = 'ctrl', subtitle = 'Action: kill -STOP {}'.format(pids),
                      arg = kill_args('-STOP', pids))

  wf.send_feedback()

if __name__ == '__main__':
  wf = Workflow3(update_settings = {'github_slug': 'netromdk/alfred-pkill', 'frequency': 7})
  log = wf.logger
  sys.exit(wf.run(main))
