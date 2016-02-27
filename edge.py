#!/usr/bin/env python
from textblob import TextBlob

class Message:
  def __init__(self, text):
    self.text = text
    self.score = 0
    self.get_sent()

  # Returns the average polarity of the whole message
  def get_sent(self):
    blob = TextBlob(self.text)
    scores = []
    for sentence in blob.sentences:
      scores.append(sentence.sentiment.polarity)
    self.score =  sum(scores) / float(len(scores))

class User:
  def __init__(self, name, job, pic):
    self.name = name
    self.job = job
    self.pic = pic
  
  @staticmethod
  def combine(all_conts):
    combo = {}
    for conts in all_conts:
      for uid in conts.keys():
        if uid in combo:
          combo[uid] = combo[uid] + conts[uid]
        else:
          combo[uid] = conts[uid]
    return combo

class Edge:
  def __init__(self):
    self.count = 0 # Num posts in common
    self.total_score = 0
    self.messages = []

  def copy(self):
    copy = Edge()
    copy.count = self.count
    copy.total_score = self.total_score
    copy.messages.extend(self.messages)
    return copy

  def update_edge(self, messages):
    self.count = self.count + len(messages)
    self.messages.extend(messages)
    for message in messages:
      self.total_score = self.total_score + message.score

  def add_edge(self, edge):
    self.count = self.count + edge.count
    self.total_score = self.total_score + edge.total_score
    self.messages.extend(edge.messages)

  def compute_avg(self):
    return self.total_score / float(len(self.messages))

  @staticmethod
  def combine(all_edges):
    combo = {}
    for edges in all_edges:
      for edge_id in edges.keys():
        if edge_id in combo:
          combo[edge_id].add_edge(edges[edge_id])
        else:
          combo[edge_id] = edges[edge_id].copy()
    return combo
