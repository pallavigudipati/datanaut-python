#!/usr/bin/env python
from edge import Edge
from edge import Message
from edge import User
from exporter import Exporter
from sql_handler import SQLHandler
import json
import sys
#import xmltodict

def get_inters_and_cons(messages, edges):
  participants = set()
  mssgs = {} # user -> all messages
  for message in messages:
    uid = int(message['sender_id'])
    participants.add(uid)
    if uid in mssgs:
      mssgs[uid].append(Message(message['body']['plain']))
    else:
      mssgs[uid] = [Message(message['body']['plain'])]
    
  parts = list(participants)
  parts.sort()

  for i in range(0, len(parts)):
    for j in range(i + 1, len(parts)):
      edge_id = str(parts[i]) + ':' + str(parts[j])
      if not edge_id in edges:
        edges[edge_id] = Edge()
      edges[edge_id].update_edge(mssgs[parts[i]])
      edges[edge_id].update_edge(mssgs[parts[j]])

  return parts

sql_handler = SQLHandler()

groups = {}
group_hash = {}
user_hash = {}

interactions = {}
contributions = {}

# Group -> Threads 
json_string = sql_handler.get_feeds(sys.argv[1])
if json_string == None:
  print False
  exit()

doc = json.loads(json_string)

for reference in doc['references']:
  # User
  if reference['type'] == 'user':
    user_hash[int(reference['id'])] = User(reference['full_name'], reference['job_title'], reference['mugshot_url'])
    # Group
  elif reference['type'] == 'group':
    group_hash[int(reference['id'])] = reference['full_name']

for message in doc['messages']:
  # If its not a group message
  if not 'group_id' in message:
    continue
  
  # Group
  group_id = int(message['group_id'])
  if not group_id in groups:
    groups[group_id] = {}
  group = groups[group_id] 
  
  # Thread
  thread_id = int(message['thread_id'])
  if thread_id in group:
    group[thread_id].append(message)
  else:
    group[thread_id] = [message]
#print groups

# Get interactions and contributions
for group_id in groups.keys():
  threads = groups[group_id]
  edges = {} # Pair-wise
  radius = {}
  for thread_id in threads.keys():
    cons = get_inters_and_cons(threads[thread_id], edges)
    # Update cons
    for uid in cons:
      if uid in radius:
        radius[uid] = radius[uid] + 1
      else:
        radius[uid] = 1
  interactions[group_id] = edges
  contributions[group_id] = radius

# OVERALL
all_id = 0
all_name = 'All'
all_edges = Edge.combine(interactions.values())
all_conts = User.combine(contributions.values())
interactions[all_id] = all_edges
contributions[all_id] = all_conts
group_hash[all_id] = all_name

outs = Exporter.export(contributions, user_hash, interactions)
#print outs

success = sql_handler.insert_plots(sys.argv[1], outs, group_hash)
if success == False:
  print False
  exit()
sql_handler.cleanup()
print True
#doc = xmltodict.parse(fd.read())
