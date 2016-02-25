# Machine-Authenticator
---
Machine-Authenticator trains a linear classifier with subjects performing different mental tasks. The learner is then tested to see if it can discern different subjects and tasks. The results of testing is reported in terms of False Rejecton Rate (FRR) and False Acceptance Rate (FAR).

- scenarios.py:
 - Use different training and testing strategy to see the robustness of the authentication ability of the learner.
   - Scenario 0: Use cross_validation.cross_val_score() to cross validate the classifier's effectiveness in discerning pairs of mental tasks of the same subject. Returns the most discernible pair of task and its cross validation score (mean and standard deviation) of each subject.
   - Scenario 1: For each participant, for each task as target task, draw from it half of its total sample as training data, the other half as testing data. From all other tasks from the same participant, known as "other tasks", draw the same amount of samples as training data, and same amount of samples as testing data. Train a binary liner classifier with the two training data sets, then have it predicts the label of the two testing sets. Get a False Rejection Rate (FRR) and False Acceptance Rate (FAR) from the predicted labels.
   - Scenario 2: Similar to scenario 1, but the "others" are now the same task performed by subjects other than the target  subject.
   - Scenario 3: Similar to scenario 1, but the "others" are now all tasks performed by subjects other than the target subject.

- reader.py:
 - Provides functions to read EEG data gather with Neurosky Mindwave headset from JSON format. Fast Fourier Transform the data, bin the data into 100 bins, and average the data across numbers determined by "vector resolution" into feature vector.

- selector.py
  - Generate random numbers and map the numbers into subjects, tasks, trials, and samples.
    - random_sampler: Generate two lists of Random integers that lies within the range of the total samples.
    - sample_mapper: Map each elements in the list of random integers to a specific subject, task, trial and sample, according to the numbers of samples in each level.

- learner.py
  - Label data according to its role (target, or other), so the labelled data could be used for linear classifier in scenarios. Also has the wrapper of cross_validation.

# Prerequisite
---
- scikit-learn
- Numpy

# Notes
---
The logic to build feature vectors are based on @wazaahhh's brainlib, and @elsewhere's feature_vector_generator.

Subject 002 was later discovered to have ADHD, and was therefore excluded from the dataset.

Subject 011's task 'face' has only 9 trials.
