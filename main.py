import cv2
import time
import mail_reader.vision.hardware.access_webcam as access_webcam
import mail_reader.data_access.database_creator as database_creator
import mail_reader.data_access.box_matching as box_matching
import mail_reader.vision.processing.image_process as image_process
import mail_reader.vision.processing.ocr_processor as ocr_process
import mail_reader.addressee_identification.text_analyzer as text_analyzer
import mail_reader.addressee_identification.addressee_reader as addressee_reader

# Create database from file
dbpath = './20161209.xlsx'
print('Creating database from file: ' + dbpath)
creator = database_creator.BapDatabaseCreator()
db_conn = creator.create_database_from_excel(dbpath)

# Set box matcher onto database connection
matcher = box_matching.BoxMatcher()
matcher.set_database_connection(db_conn)

print('Creating analyzers')
# Create and set image processor
processor = image_process.ImageProcessor(ocr_process.TesseractProcessor())

# Create and set text analyzer
analyzer = text_analyzer.TextAnalyzer()

# Create and set addressee reader
reader = addressee_reader.AddresseeReader(processor, analyzer)

print('Opening webcam')
# Initialize webcam
cam = access_webcam.LogitechC270()
cam.open_webcam_id(1)

print('Initializing main loop')

def print_matches(match):
  print('Box: ' + '{:03d}'.format(match['box_number'],))
  print('Score: ' + '{:01.2f}'.format(match['score'],))
  print('*Names*')
  for name in match['all_names']:
    print(name)

while True:
  print('loop')
  image = cam.get_frame()
  cv2.imshow('img', image)
  # Exit if ESC pressed
  k = cv2.waitKey(10)
  if k == 27:  # ESC
    break
  read_fields = reader.get_mail_fields(image)

  n = read_fields.addressee_line['all_names'] 
  a = []
  for idx, item in enumerate(n):
    if item not in ['Or','Current','Resident']:
      a.append(item)
  read_fields.addressee_line['all_names'] = a
  if not read_fields.is_populated():
    print('skipped')
    time.sleep(1)
  matches = matcher.get_matches(read_fields)
  if len(matches) == 0:
    print('no matches available')
    continue


  print('----------------------- Matches ----------------------')
  print('Names: ' + str(read_fields.addressee_line['all_names']))
  print('Score0: ' + '{:01.2f}'.format(matches[0]['score']) + 
        ' Box: ' + '{:03d}'.format(matches[0]['box_number']))
  print('Score1: ' + '{:01.2f}'.format(matches[1]['score']) +
        ' Box: ' + '{:03d}'.format(matches[1]['box_number']))
  print('Score2: ' + '{:01.2f}'.format(matches[2]['score']) +
        ' Box: ' + '{:03d}'.format(matches[2]['box_number']))  
  print('-------------')
  print('Best box: ' + '{:03d}'.format(matches[0]['box_number'],))
  print('-------------')
  print('-- Match 0 --')
  print_matches(matches[0])
  if matches[0]['score'] - matches[1]['score'] < 1.0:
    print('-- Match 1 --')
    print_matches(matches[1])
  # print(matches[0])

  time.sleep(1)

cam.close_camera()

