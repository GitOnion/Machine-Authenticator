import random

vector_resolution = 3
task_total_seconds = 10 * 12  # Change here if there will be cut-off time at the beginning.
task_total_samples = task_total_seconds / vector_resolution  # 40
task_split_samples = task_total_samples / 2  # 20


def random_sampler(number_of_samples):
    '''Return a tuple of two list, each specifying a lists of random integers for training
    or testing. Each random integer falls within the range of the respective calling scenario.'''
    holder = random.sample(xrange(number_of_samples), number_of_samples)
    train_data = holder[:task_split_samples]
    test_data = holder[task_split_samples:task_total_samples]
    return(train_data, test_data)


def sample_mapper(sample_list, subject_list, task_list, subject_sample_numbers, task_sample_numbers, subjects_data):
    '''Return actual samples based on the sample_list.'''
    sample_data = []
    for sample in sample_list:
        for subject_index, subject_total_samples in enumerate(subject_sample_numbers):
            if sample >= subject_total_samples:
                sample -= subject_total_samples
            else:
                select_subject = subject_list[subject_index]
                break
        for task_index, task_total_samples in enumerate(task_sample_numbers[subject_list.index(select_subject)]):
            if sample >= task_total_samples:
                sample -= task_total_samples
            else:
                select_task = task_list[task_index]
                break
        for trial_index, trial_total_samples in enumerate(subjects_data[select_subject][0][select_task][1]):
            if sample >= trial_total_samples:
                sample -= trial_total_samples
            else:
                select_trial = trial_index
                select_sample = subjects_data[select_subject][0][select_task][0][trial_index][sample]
                break
        sample_data.append(select_sample)
    return(sample_data)
