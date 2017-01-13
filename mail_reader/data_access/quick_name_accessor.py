import mail_reader.data_access.store_data_formatter as sdf
import difflib
import mail_reader.data_access.name_scoring as name_scoring

class QuickNameAccess(object):
  '''Allows quick name lookups to get related box numbers

  Names are accessed via dictionary that has its keys set as the first letter
  in the word. This splits the lookup space by ~26, but must have first letter
  of name from OCR be correct.

  Attributes:
    letter_access: dictionary of letters containing names starting with
                   that letter
  '''

  def __init__(self):
    '''Init with empty access dictionary'''
    self.letter_access = {}

    # TODO(searow): consider switching the NameScorer to be passed in
    #               at init so we can alter the name scoring methods
    self.scorer = name_scoring.NameScorer()

  def create_entries_with_formatter(self, data_formatter):
    while data_formatter.has_next_customer():
      line = data_formatter.format_next_customer()

      # Each line can have multiple customers, so process each individually
      for item in line:
        name = item[0]
        box = item[1]
        letter = name[0]
        entry = QuickAccessEntry(name, box)
        self.add_entry(letter, entry)

  def find_matches_by_names(self, names):
    '''Given a set of names to identify boxholder, returns best box matches

    Args:
      names: list of strings of name to identify boxholder

    Returns:
      List of boxes and scores in decreasing match strength:
      [[box_number, box_score], [box_number, box_score]]
    '''

    box_scores = {}

    # Evaluate each name's contribution to box scores separately
    for name in names:
      # Get the entries for the corresponding letter and pass to scorer
      letter = name[0]
      entries = self._get_entries_by_letter(letter)
      entry_names = [e.name for e in entries]

      self.scorer.set_name_to_match(name)
      self.scorer.set_match_list(entry_names)
      name_scores = self.scorer.get_scores()

      # Filter out any duplicate box scores. Each box should only contribute
      # once per name scoring. If there are 5 Smith names in box 101, then 
      # box 101 should only contribute once to the Smith name. This prevents
      # boxes with a BUNCH of names from unevenly contributing to a box score
      # simply because it has a lot of names
      filtered_scores = self._filter_boxes_by_highest_score(entries, 
                                                            name_scores)

      # Add to the box scores to the overall list
      for box_num, score in filtered_scores:

        # Add the box number to the score dict if it doesn't exist
        if box_num not in box_scores.keys():
          box_scores[box_num] = 0

        # Scoring mechanism: for each box, create a running total of match
        # scores obtained for every name given, adding scores as a box is 
        # hit multiple times
        box_scores[box_num] += score

    sorted_boxes = self._reorder_box_scores(box_scores)

    return sorted_boxes

  def _filter_boxes_by_highest_score(self, entries, name_scores):
    '''Removes duplicates from name_scores based on box number

    Goes through name_scores and looks for duplicate box numbers. If a 
    duplicate exists, it removes all duplicates that have a lower score. This
    ensures that a box can only contribute once to a box score for a 
    given name. Call this after we get scores for a given name, but before
    we add the scores to the overall scores list.

    Args:
      entries: list of QuickAccessEntry objects, used to cross reference
               the indices in name_scores with box numbers in entries
      name_scores: result from NameScorer.get_scores

    Returns:
      Filtered results as nested list [[box_num, score], [box_num, score]]
    '''
    filtered = []

    # Evaluate every name score item, getting the resultant box number and 
    # saving only the box numbers that have the highest scores for duplicated
    # box numbers
    for score, idx in name_scores:
      box_num = entries[idx].box_num

      # Check to see if the box number already exists in the filtered results
      box_is_new = True
      for filter_idx, [filter_box, filter_score] in enumerate(filtered):
        if filter_box == box_num:
          # If we get a match, we can break the loop. Only save the score if 
          # it's higher than the already saved score
          box_is_new = False
          if score > filter_score:
            filtered[filter_idx][1] = score

      # No existing boxes -> just add to the filtered list
      if box_is_new:
        filtered.append([box_num, score])

    return filtered

  def _reorder_box_scores(self, box_scores):
    '''Reorders dict of boxes based on box score

    Args:
      box_scores: dict of box scores, box_scores = {box_num : score}

    Returns:
      List of boxes and corresponding scores [[box, score],[box,score]] in
      decreasing order of box score
    '''
    sorted_scores = sorted(box_scores.keys(), key=lambda box: box_scores[box],
                           reverse=True)
    sorted_boxes_and_scores = [[box, box_scores[box]] for box in sorted_scores]

    return sorted_boxes_and_scores


  def _get_entries_by_letter(self, letter):
    '''Returns list of names of all QuickAccessEntry for that letter

    Args:
      letter: string of single letter that is being accessed (e.g.: 'F' for 
              the name Fox and 'M' for McCloud)

    Returns:
      List of QuickAccessEntry objects registered to that letter
    '''
    entries = self.letter_access[letter]
    return entries

  def add_entry(self, letter, entry):
    '''Adds entry to the access object

    Args:
      letter: letter to add the to entry
      entry: QuickAccessEntry object to add 
    '''

    # TODO(searow): add checks for letters being only 1 letter

    # We need to create the letter dict entry if it doesn't exist
    if not letter in self.letter_access.keys():
      self.letter_access[letter] = []

    self.letter_access[letter].append(entry)

class QuickAccessEntry(object):
  '''Entries for the QuickNameAccess object'''

  def __init__(self, name, box_num):
    '''Inits entry with a name associated with a box number

    Args:
      name: string name to be added
      box_num: box number that the name is registered to

    Returns:
      None
    '''

    self.name = name
    self.box_num = box_num
