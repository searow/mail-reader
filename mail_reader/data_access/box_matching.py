import difflib
from operator import itemgetter

def _get_box_scores(name_to_match, name_list, box_multiplier):
  """Calculates box score dict for each name in name_list and returns scores.

  Calculates score for each name. Only the highest score for each box is saved
  and the rest are discarded.

  Args:
    name_to_match: Name that we are trying to match (ie: 'FOX').
    name_list: Names that we want to score and their associated box numbers
               (ie [['FALCO', 555], ['FOX', 111], ['FRIEND', 2], ...]).
    box_multiplier: List of boxes that should have a multiplied score.

  Returns:
    Dictionary of scores, keys = box number as int, values = best score.
  """
  # Create differ object here so we don't have to keep setting the first seq
  differ = difflib.SequenceMatcher()
  differ.set_seq1(name_to_match)

  multiplier = 2  # Score multiplier if matches box_multiplier
  box_scores = {}

  for [name, box] in name_list:
    # Evaluate similarity and only add if unique. If not unique, only the 
    # highest score is saved so update the score if new one is higher.
    differ.set_seq2(name)
    score = differ.ratio()
    if box in box_multiplier:
      score *= multiplier
    if box in box_scores:
      if score > box_scores[box]:
        box_scores[box] = score
    else:
      box_scores[box] = score

  return box_scores

def _combine_boxes_scores(box_scores):
  """Returns overall box score list sorted in decreasing score order.

  Args:
    box_scores: List of dictionaries of box scores, which is a list of the 
                results from _get_box_scores.

  Returns:
    Overall box score list in decreasing score order [(box, score), 
    (box, score), (box, score), ...]
  """
  # Add the score for each box into a new dictionary, adding values as needed.
  temp_scores = {}
  for box_scores_for_name in box_scores:
    for box in box_scores_for_name:
      if box not in temp_scores:
        temp_scores[box] = 0
      temp_scores[box] += box_scores_for_name[box]

  # Convert to list so we can sort by final score
  final_scores = sorted(temp_scores.items(), key=itemgetter(1), reverse=True) 

  return final_scores

class BoxMatcher(object):
  """Performs box matching operations to match MailFields with box number.

  Given a MailFields object and a database to access, finds the best matches
  to the database.

  Attributes:
    __db_conn: Database connection from which to get box data.
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
    box_multipliers = mail_fields.probable_box
    scores = []
    for name in mail_fields.addressee_line['all_names']:
      possible_names = self.__get_active_names_for_letter(name[0].upper())
      name_score = _get_box_scores(name.upper(), possible_names, 
                                   box_multipliers)
      scores.append(name_score)

    final_score = _combine_boxes_scores(scores)

    return final_score

  def set_database_connection(self, db_conn):
    """Sets sqlite3 database connection to use for box matching.

    Args:
      db_conn: Database connect to use.

    Returns:
      None.
    """
    self.__db_conn = db_conn

  def __get_active_names_for_letter(self, letter):
    """Queries database for matches beginning with letter.

    First letter of string is given. Queries database for names starting with
    that string and returns the names along with their boxes. Only returns 
    names if they are active.

    Args:
      letter: First letter of name to search.

    Returns:
      Nested list of names and associated boxes [['NAME1', 20], ['NAME2', 30]]
    """
    # TODO(searow): need to add a way to access and assess both active and
    #               inactive people eventually.
    c = self.__db_conn.cursor()
    c.execute('''
        SELECT DISTINCT n.unique_entity_name, b.box_id
                   FROM unique_entity_names as n
                        INNER JOIN box_entities as b
                                ON n.entity_id=b.entity_id
                        INNER JOIN entity_statuses as s
                                ON s.entity_id=b.entity_id
                     WHERE n.unique_entity_name 
                           LIKE ?
                       AND s.current=1;
    ''', (letter+'%',))

    return c.fetchall()
