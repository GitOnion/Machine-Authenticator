from random import shuffle
from random import random

vector_resolution = 3
trial_times = 10  # 10
seconds_per_trial = 12  # 12
samples_per_trial = seconds_per_trial / vector_resolution  # 4

task_total_seconds = trial_times * seconds_per_trial  # 120
task_total_samples = task_total_seconds / vector_resolution  # 40
task_split_samples = task_total_samples / 2  # 20

task_list = ['breath', 'blink', 'ocular', 'song', 'hear', 'face', 'cube']
task_number = len(task_list)
# subject_total_seconds = task_total_seconds * task_number #840
# subject_other_seconds = subject_total_seconds - task_total_seconds #720
# subject_other_samples = subject_other_seconds / vector_resolution #240
# subject_split_samples = subject_other_samples / 2 #120

signal_quality = 30
# TODO Need to incorporate the signal_quality selection


def random_sampler(number_of_tasks):
    '''Return a tuple of two list, each specifying a lists of random integers for training
    or testing. Each random integer falls within the range of the respective calling scenario.'''
    holder = [x for x in range(number_of_tasks * task_total_samples)]  # 40
    seed = random()
    shuffle(holder, lambda: seed)
    train_data = holder[:task_split_samples]
    test_data = holder[task_split_samples:task_total_samples]
    # print(holder)
    return(seed, train_data, test_data)


def sample_mapper(sample_list, target_task_list, parsed_data):
    '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
    Do a try-except test before grouping the samples.'''
    sample_data = []
    for sample in sample_list:
        select_task = target_task_list[(sample / task_total_samples)]
        select_trial = (sample % task_total_samples) / samples_per_trial
        select_sample = (sample % samples_per_trial) * vector_resolution
        try:
            parsed_data[select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
        except IndexError:
            continue
        grouper = []
        # print(select_task, select_trial, select_sample)
        for i in range(vector_resolution):
            grouper.append(parsed_data[select_task][select_trial][select_sample+i]['binnedPS'])
        sample_data.append(grouper)
    return(sample_data)


def subject_mapper(sample_list, subject_list, task, parsed_data):
    '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
    Do a try-except test before grouping the samples.'''
    sample_data = []
    for sample in sample_list:
        select_subject = subject_list[(sample / task_total_samples)]
        select_trial = (sample % task_total_samples) / samples_per_trial
        select_sample = (sample % samples_per_trial) * vector_resolution
        try:
            parsed_data[select_subject][task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
        except IndexError:
            continue
        grouper = []
        # print(select_task, select_trial, select_sample)
        for i in range(vector_resolution):
            grouper.append(parsed_data[select_subject][task][select_trial][select_sample+i]['binnedPS'])
        sample_data.append(grouper)
    return(sample_data)


def space_mapper(sample_list, subject_list, task_list, parsed_data):
    '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
    Do a try-except test before grouping the samples.'''
    sample_data = []
    # print(sample_list)
    # print(subject_list)
    # print(len(subject_list)*task_total_samples)
    for sample in sample_list:
        select_subject = subject_list[(sample / (len(task_list)*task_total_samples))]
        select_task = task_list[(sample % (len(task_list)*task_total_samples)) / task_total_samples]
        select_trial = (sample % task_total_samples) / samples_per_trial
        select_sample = (sample % samples_per_trial) * vector_resolution
        # print(select_subject, select_task, select_trial, select_sample)

        try:
            parsed_data[select_subject][select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
        except IndexError:
            continue
        grouper = []
        for i in range(vector_resolution):
            grouper.append(parsed_data[select_subject][select_task][select_trial][select_sample+i]['binnedPS'])
        sample_data.append(grouper)
    return(sample_data)
