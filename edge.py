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

class Edge:
  def __init__(self):
    self.count = 0 # Num posts in common
    self.total_score = 0
    self.messages = []

  def update_edge(self, messages):
    self.count = self.count + len(messages)
    self.messages.extend(messages)
    for message in messages:
      self.total_score = self.total_score + message.score

  def compute_avg(self):
    return self.total_score / float(len(self.messages))
