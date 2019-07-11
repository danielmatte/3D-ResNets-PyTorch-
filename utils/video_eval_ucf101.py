import sys
from eval_ucf101 import UCFclassification

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("Usage: python3 {} annotation_filename prediction_filename".format(sys.argv[0]))
    exit(0)

  ucfClassification = UCFclassification(ground_truth_filename=sys.argv[1], 
                                        prediction_filename=sys.argv[2], 
                                        subset='validation', 
                                        verbose=True, 
                                        top_k=5)

  ucfClassification.evaluate()
  print(ucfClassification.hit_at_k)