import difflib

class NameScorer(object):
  def __init__(self):
    pass

  def set_name_to_match(self, name):
    '''Sets name string that is to be matched

    Args:
      name: string of name that is trying to be matched

    Returns:
      None
    '''
    self.name_to_match = name

  def set_match_list(self, match_list):
    '''Sets potential match list

    Args:
      match_list: list of strings of potential matches

    Returns:
      None
    '''
    self.match_list = match_list

  def get_scores(self):
    '''Calculates score match values for each name

    Uses list of names ['FOX', 'FALCO', 'FROG'] and name to match
    ['FALLON'], returns scores for each of the names that represent a match
    score, with the highest score representing the best match to the name

    Args:
      None

    Returns:
      List of scores and index [[score, index], [score, index]] in decreasing
      score order (first is best match). Index is the index of the item in
      entry_names for quick access.
    '''

    # TODO(searow): currently using difflib, but consider switching to alternate
    #               methods to improve speed and reliability

    # Only change seq2 in differ object for each name
    differ = difflib.SequenceMatcher()
    differ.set_seq1(self.name_to_match)

    # scores is a list of [name, score] for every entry_name given
    scores = []

    for idx, name in enumerate(self.match_list):
      differ.set_seq2(name)
      score_item = [differ.ratio(), idx]
      scores.append(score_item)

    scores = sorted(scores, key=lambda lst: lst[0], reverse=True)

    return scores
