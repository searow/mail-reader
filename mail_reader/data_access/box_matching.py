import difflib
from operator import itemgetter

def _prune_common_words(names):
  """Removes common words from list of names.

  Args:
    names: List of names as strings input.
  Returns:
    Same list of names, but with common words removed.
  """
  common_words = set(['OWNER', 
      'REGISTERED', 'BUSINESS',
      'CURRENT', 'RESIDENT',
      'OR', 'AND', 'TO'
      ])

  pruned = [name for name in names if name.upper() not in common_words]
  return pruned

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
  as_list = [[k, v] for (k, v) in temp_scores.items()]
  final_scores = sorted(as_list, key=itemgetter(1), reverse=True) 

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
    all_names = mail_fields.addressee_line['all_names']
    all_names = _prune_common_words(all_names)
    scores = []
    for name in all_names:
      possible_names = self.__get_active_names_for_letter(name[0].upper())
      name_score = _get_box_scores(name.upper(), possible_names, 
                                   box_multipliers)
      scores.append(name_score)

    combined_score = _combine_boxes_scores(scores)
    final_score = self.__resolve_conflicts(combined_score, all_names)

    final_matches = []
    for [box, score] in final_score:
      d = {}
      d['box_number'] = box
      d['score'] = score
      d['all_names'] = self._get_active_names_in_box(box)
      final_matches.append(d)

    return final_matches

  def _get_active_names_in_box(self, box_number):
    c = self.__db_conn.cursor()
    c.execute('''
        SELECT e.original_name
          FROM box_entities as b
               INNER JOIN entity_statuses as e
                       ON b.entity_id=e.entity_id
         WHERE b.box_id=?
           AND e.current=1;
     ''', (box_number,))

    return c.fetchall()

  def __resolve_conflicts(self, scores, names):
    """Resolves cases where top scores are same for multiple boxes.

    Args:
      scores: Result from _combine_boxes_scores().
    Returns:
      Final scores list, with scores increased for top contenders.
    """
    # Exit and return empty match list if scores is empty since top_score 
    # relies on indexing scores[0]
    if len(scores) == 0:
      return []
    # scores is already sorted in desc order, so save the top score and modify
    # each score until we don't have the top score anymore. 
    top_score = scores[0][1]
    idx = 0
    while scores[idx][1] >= top_score:
      # For each box with a score that we need to reevaluate, grab the entity
      # names in that box. Those (entity_names) are individually scored again
      # against each of the original names that were being checked (names). For
      # each of the original names, calculate the scores and sum them up based
      # on the entity_id instead, which consolidates an overall entity name 
      # into a contributing score. The best of these are then added onto the 
      # original data and then sorted again.
      (box, score) = scores[idx]
      entity_names = self.__get_entity_names_for_box(box)
      entity_scores = []
      for name in names:
        entity_scores.append(_get_box_scores(name, entity_names, []))
        # best = sorted(entity_scores.items(), key=itemgetter(1), reverse=True)[0]
      combined_entity_scores = _combine_boxes_scores(entity_scores)
      best = sorted(combined_entity_scores, key=itemgetter(1), reverse=True)[0]
      scores[idx][1] += best[1]
      idx += 1

    return sorted(scores, key=lambda x: x[1], reverse=True)

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

  def __get_entity_names_for_box(self, box_number):
    """Queries db for all entities and their names in box_number.

    Args:
      box_number: Box number to query.
    Returns:
      Nested list of names and associated boxes [['NAME1', 20], ['NAME2', 30]].
    """
    c = self.__db_conn.cursor()
    c.execute('''
        SELECT n.unique_entity_name, n.entity_id 
               FROM unique_entity_names as n
                    INNER JOIN box_entities as b
                            ON n.entity_id=b.entity_id
                    INNER JOIN entity_statuses as s
                            ON s.entity_id=b.entity_id
              WHERE s.current=1
                AND b.box_id=?;
    ''', (box_number,))

    return c.fetchall()
    # sql_result = c.fetchall()

    # entity_names = {}

    # # Add each entry to the dictionary, creating a new list for new ids
    # for (entity_id, name) in sql_result:
    #   if entity_id not in entity_names:
    #     entity_names[entity_id] = []
    #   entity_names[entity_id].append(name)

    # return entity_names
