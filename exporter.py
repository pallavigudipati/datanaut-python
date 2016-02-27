import json

class Exporter:
  @staticmethod
  def export(contributions, node_hash, edges):
    outs = {}
    group_ids = contributions.keys()
    for group_id in group_ids:
      nodes_ids = contributions[group_id].keys()
      out = {}
      jnodes = []
      jedges = []
      i = 1
      for node_id in nodes_ids:
        jnode = {}
        jnode['name'] = node_hash[node_id].name
        jnode['job'] = node_hash[node_id].job
        jnode['pic'] = node_hash[node_id].pic
        jnode['group'] = i
        jnode['value'] = contributions[group_id][node_id]
        i = i + 1
        jnodes.append(jnode)
      for edge_id in edges[group_id].keys():
        ends = edge_id.split(':')
        idxa = nodes_ids.index(int(ends[0]))
        idxb = nodes_ids.index(int(ends[1]))
        jedge = {}
        jedge['source'] = idxa
        jedge['target'] = idxb
        jedge['value'] = edges[group_id][edge_id].count
        score = edges[group_id][edge_id].compute_avg() # -1 to 1
        score_percent = (score + 1.0) * 50.0
        jedge['score'] = score_percent
        jedges.append(jedge)
      out['nodes'] = jnodes
      out['links'] = jedges
      outs[group_id] = json.dumps(out)
    return outs
