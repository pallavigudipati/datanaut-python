#!/usr/bin/env python
import MySQLdb

class SQLHandler:

  def __init__(self):
    self.db = MySQLdb.connect(host="localhost", user="user-datanaut", \
        passwd="Pwd-Data-16", db="datanaut")

  def get_feeds(self, yammer_id):
    cursor = self.db.cursor()
    sql_cmd = "SELECT * FROM messages_my_feed WHERE yammer_id  = '%s'" % (yammer_id)
    feeds = None
    try:
      cursor.execute(sql_cmd)
      results = cursor.fetchall()
      for row in results:
        feeds = row[2]
    except:
      pass
      #print "ERROR: Unable to fetch data"
    #  feeds = None
    return feeds

  def insert_plots(self, yammer_id, plots, group_hash):
    cursor = self.db.cursor()
    for group_num in plots.keys():
    #  print group_num
      group_id = str(group_num)
      sql_cmd = "SELECT * FROM group_plots_data WHERE yammer_id  = '%s' \
          AND group_id = '%s'" % (yammer_id, group_id)
      try:
        cursor.execute(sql_cmd)
        results = cursor.fetchall()
        if len(results) == 0:
   #       print 'insert'
          sql_cmd = "INSERT INTO group_plots_data(yammer_id, \
              group_id, group_name, group_plot_json) VALUES ('%s', '%s', '%s', '%s')" % \
              (yammer_id, group_id, group_hash[group_num], plots[group_num])
        else:
    #      print 'update'
          sql_cmd = "UPDATE group_plots_data SET group_plot_json = '%s' WHERE \
              yammer_id = '%s' AND group_id = '%s'" % (plots[group_num], yammer_id, group_id)
        try:
          cursor.execute(sql_cmd)
          self.db.commit()
        except:
    #      print 'ERROR'
          self.db.rollback()
      except:
        #print "ERROR: Unable to fetch data"
        return False
    return True

  def cleanup(self):
    self.db.close()
