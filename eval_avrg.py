import sys
import numpy as np
import glob


import utils

if len(sys.argv) != 3:
    sys.exit("Usage: python eval_avrg.py <predictions_path> [subset=test]")

predictions_path_all = glob.glob(sys.argv[1] + "*")

print "shape of metadata_path_all"
print(len(predictions_path_all))

mybool = False
for predictions_path in predictions_path_all:
    print(predictions_path)
    if not mybool:
        predictions = np.load(predictions_path)#.ravel()
        mybool = True
    else:
        predictions = predictions + np.load(predictions_path)#.ravel()
print "shape of predictions"
print(predictions.shape)
print(predictions.max())

import data

if len(sys.argv) == 3:
    subset = sys.argv[2]
    assert subset in ['train', 'valid', 'test', 'test_valid']
else:
    subset = 'test'

if subset == "test":
    y = data.labels_test
    mask = data.mask_test
elif subset == "train":
    y = data.labels_train
    mask = data.mask_train
elif subset == "train_valid":
    y = data.labels
    mask = data.mask
else:
    y = data.labels_valid
    mask = data.mask_valid

acc = utils.proteins_acc(predictions, y, mask)

print "Accuracy (%s) is: %.5f" % (subset,acc)

## Alternative model avrg!! ##

john = np.zeros((640,data.seqlen,data.d))
for predictions_path in predictions_path_all:
    print(predictions_path)
    predictions = np.load(predictions_path)#.ravel()
    predictions = np.argmax(predictions, axis=2)
    for i in range(640):
        for j in range(data.seqlen):
            num = predictions[i, j]
            john[i, j, num] = john[i, j, num] + 1

acc = utils.proteins_acc(john, y, mask)

print "Alternative accuracy (%s) is: %.5f" % (subset,acc)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
