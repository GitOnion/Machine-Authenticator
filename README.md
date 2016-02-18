# Machine-Authenticator
---
Machine-Authenticator trains a linear classifier with subjects performing different mental tasks. The learner is then tested to see if it can discern different subjects and tasks. The results of testing is reported in terms of False Rejecton Rate (FRR) and False Acceptance Rate (FAR).

- scenarios.py:
 - Use different training and testing strategy to see the robustness of the authentication ability of the learner.
   - Scenario 0: Use cross_validation.cross_val_score() to cross validate the classifier with pairs of mental tasks.

- reader.py:
 - Provides functions to read EEG data gather with Neurosky Mindwave headset from JSON format.  

# Prerequisite
---
- scikit-learn
- Numpy

# Notes
---

The logic to build feature vectors are based on @wazaahhh's brainlib, and @elsewhere's feature_vector_generator.
