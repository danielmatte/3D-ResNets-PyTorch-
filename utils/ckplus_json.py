import sys
import os
from glob import glob
import json

def getEmotionFromFile(dataset_path, filename):
  emotions = {0: 'neutral', 1: 'anger', 2: 'contempt', 3: 'disgust', 4: 'fear', 5: 'happy', 6: 'sadness', 7: 'surprise'}

  subject = filename.split('/')[-3]
  session = filename.split('/')[-2]
  emotionPath = "{}/Emotion/{}/{}/*.txt".format(dataset_path, subject, session)
  for filename in glob(pathname=emotionPath, recursive=True):
    with open(filename) as f:
      emotion_id = int(float(f.readline()))
      return emotions[emotion_id], emotion_id
  return None, None

def getVideoPath(dataset_path, filename):
    subject = filename.split('/')[-3]
    session = filename.split('/')[-2]
    images_path = "cohn-kanade-images/"
    video_path = os.path.join(subject, session)
    
    if (os.path.isdir(os.path.join(dataset_path,images_path,video_path))):
      return video_path
    else:
      return None

def getAUs(filename):
  AUs = []
  with open(filename) as f:
    for line in f:
      if len(line) > 5:
        AUs.append(int(float(line.split()[0])))
  return AUs
  
def getDataset(dataset_path):
  FACSPath = "{}/FACS/**/*.txt".format(dataset_path)
  labels = []
  dataset = {}
  dataset['labels'] = []
  dataset['database'] = {}
  for filename in glob(pathname=FACSPath, recursive=True):
    video_path = getVideoPath(dataset_path, filename)
    if (video_path):
      dataset['database'][video_path] = {}
      dataset['database'][video_path]['subset'] = 'training'
      dataset['database'][video_path]['annotations'] = {}
      label, _ = getEmotionFromFile(dataset_path, filename)
      if label:
        dataset['database'][video_path]['annotations']['label'] = label
        if label not in labels:
          labels.append(label)

      dataset['database'][video_path]['annotations']['AUs'] = getAUs(filename)

  dataset['labels'] = labels
  return dataset

def convert_ckplus_to_activitynet_json(dataset_path, output_csv):
  dataset = getDataset(dataset_path)
  with open(output_csv, 'w') as dst_file:
      json.dump(dataset, dst_file)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("Usage: python3 {} dataset_path output_json_file".format(sys.argv[0]))
    exit(0)
  
  dataset_path = sys.argv[1]
  output_csv = sys.argv[2]
  convert_ckplus_to_activitynet_json(dataset_path, output_csv)
  