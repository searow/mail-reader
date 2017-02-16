import difflib

def _get_box_scores(name_to_match, name_list, box_multiplier):
  """Calculates box score list for each name in name_list and returns scores.

  Calculates score for each name. Only the highest score for each box is saved
  and the rest are discarded.

  Args:
    name_to_match: Name that we are trying to match (ie: 'FOX').
    name_list: Names that we want to score and their associated box numbers
               (ie [['FALCO', 555], ['FOX', 111], ['FRIEND', 2], ...]).
    box_multiplier: List of boxes that should have a multiplied score.

  Returns:
    Nested list of box number and score [[box, score], [box, score], ...].
  """
  # Create differ object here so we don't have to keep setting the first seq
  differ = difflib.SequenceMatcher()
  differ.set_seq1(name_to_match)

  multiplier = 2  # Score multiplier if matches box_multiplier
  box_scores = []
  box_set = set()

  for [name, box] in name_list:
    # Evaluate similarity and only add if unique. If not unique, only the 
    # highest score is saved so update the score if new one is higher.
    differ.set_seq2(name)
    score = differ.ratio()
    if box in box_multiplier:
      score *= multiplier
    score_item = [box, score] 
    if box in box_set:
      # TODO(searow): if box score list evaluation is getting long, consider 
      #               switching to hashing box # for quick finding of existing 
      #               scores. 
      for idx, [b, s] in enumerate(box_scores):
        if b == box:
          if s > score:
            box_scores[idx][1] = s
    else:
      box_set.add(box)
      box_scores.append(score_item)

  return box_scores

def _combine_boxes_scores(box_scores):
  """Returns overall box score list sorted in decreasing score order.

  Args:
    box_scores: Nested list of box score for each name that was checked.

  Returns:
    Overall box score list in decreasing score order.
  """
  pass

class BoxMatcher(object):
  """Performs box matching operations to match MailFields with box number.

  Given a MailFields object and a database to access, finds the best matches
  to the database.

  Attributes:
    __database: Database from which to get box data.
    __fields: MailFields object passed in by get_matches.
  """
  def __init__(self):
    pass

  def get_matches(self, mail_fields):
    """Returns best matches of MailFields to database.

    Args:
      mail_fields: MailFields object to match database data to.

    Returns:
      List of box numbers with associated match score:
        [[box, score], [box, score], ...]
    """
    pass

  def set_database(self, database):
    """Sets database to use for box matching.

    Args:
      database: Database to access.

    Returns:
      None.
    """
    pass

  def _calculate_scores(self):
    """Calculates score for the fields using the database and returns matches.

    Score is calculated using two fields: names in box and probable box. 
    Gets probable matches for each name and calculates similarity score. Best 
    similarity score for each box is saved. If box with similarity score is
    contained in probable box in fields, score is multiplied. Score for each
    box for each name is combined and overall score for each box is saved.

    Returns:
      List of box numbers with associated match score: 
        [[box, score], [box, score], ...]
    """
    pass
