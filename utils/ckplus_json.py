import sys
import os
from glob import glob
import json

def getEmotionFromFile(filename):
  emotions = {0: 'neutral', 1: 'anger', 2: 'contempt', 3: 'disgust', 4: 'fear', 5: 'happy', 6: 'sadness', 7: 'surprise'}
  with open(filename) as f:
    emotion_id = int(float(f.readline()))
    return emotions[emotion_id], emotion_id

def getVideoPath(dataset_path, emotionFilename):
    subject = emotionFilename.split('/')[-3]
    subject_video = emotionFilename.split('/')[-2]
    video_path = "cohn-kanade-images/{}/{}".format(subject, subject_video)
    if (os.path.isdir(dataset_path+video_path)):
      return video_path
    else:
      return None

def getDataset(dataset_path):
  emotionsPath = "{}/Emotion/**/*.txt".format(dataset_path)
  labels = []
  dataset = {}
  dataset['labels'] = []
  dataset['database'] = {}
  for filename in glob(pathname=emotionsPath, recursive=True):
    video_path = getVideoPath(dataset_path, filename)
    if (video_path):
      label, _ = getEmotionFromFile(filename)
      if label not in labels:
        labels.append(label)

      dataset['database'][video_path] = {}
      dataset['database'][video_path]['subset'] = 'training'
      dataset['database'][video_path]['annotations'] = {'label': label}

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
  