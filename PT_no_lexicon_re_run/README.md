This directory contains outputs (correction rate and accuracy) from a
replication of the Perceptron experiment on the Finnish historical OCR
data. These are results **without** a lexicon.

Note that, as stated in Section 7 of Silfverberg et al. 2016, we
**combine the training set and development set** before training and
running the final model.

The results for the ten folds are:

```
0.
ec=297 ce=46 cc=2895 ee=409
Correction Rate (tp - fp) / (tp + fn): 0.35552
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.87524

1.
ec=255 ce=54 cc=2898 ee=440
Correction Rate (tp - fp) / (tp + fn): 0.28921
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.86455

2.
ec=255 ce=47 cc=2911 ee=434
Correction Rate (tp - fp) / (tp + fn): 0.30189
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.86811

3.
ec=291 ce=51 cc=2878 ee=427
Correction Rate (tp - fp) / (tp + fn): 0.33426
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.86893

4.
ec=266 ce=49 cc=2911 ee=421
Correction Rate (tp - fp) / (tp + fn): 0.31587
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.87113

5.
ec=271 ce=65 cc=2903 ee=408
Correction Rate (tp - fp) / (tp + fn): 0.30339
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.87030

6.
ec=298 ce=70 cc=2893 ee=386
Correction Rate (tp - fp) / (tp + fn): 0.33333
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.87497

7.
ec=288 ce=58 cc=2884 ee=417
Correction Rate (tp - fp) / (tp + fn): 0.32624
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.86976

8.
ec=256 ce=56 cc=2911 ee=424
Correction Rate (tp - fp) / (tp + fn): 0.29412
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.86838

9.
ec=270 ce=53 cc=2909 ee=415
Correction Rate (tp - fp) / (tp + fn): 0.31679
Accuracy: (tp + tn)/(tp+tn+fp+fn): 0.87168

Average correction rate: 0.317062
Average accuracy: 0.870305
```

The average correction rate is a little bit lower (0.3%-points) than in the 2016 paper. I believe this is a result of the fact that the perceptron toolkit [FinnPos](https://github.com/mpsilfve/FinnPos/tree/master/src), used in these experiments, runs beam search by default, which has a slight negative impact on the results. The original experiments in the 2016 paper used a finite-state implementation of the perceptron system which ran exact inference. Unfortunately, running the original finite-state system would have require non-trivial modifications to the code because the API of the finite-state library has changed since 2016. In any case, note that the replicated results are within the error margins given in the 2016 paper.  
