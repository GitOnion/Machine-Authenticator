import random

vector_resolution = 3
task_total_seconds = 10 * 12  # 120
task_total_samples = task_total_seconds / vector_resolution  # 40
task_split_samples = task_total_samples / 2  # 20


# def random_sampler(number_of_tasks):
#     '''Return a tuple of two list, each specifying a lists of random integers for training
#     or testing. Each random integer falls within the range of the respective calling scenario.'''
#     holder = random.sample(range(number_of_tasks * task_total_samples), 40)  # 40
#     seed = random.random()
#     # random.shuffle(holder, lambda: seed)
#     train_data = holder[:task_split_samples]
#     test_data = holder[task_split_samples:task_total_samples]
#     # print(holder)
#     return(seed, train_data, test_data)
#
#
def random_sampler(number_of_samples):
    '''Return a tuple of two list, each specifying a lists of random integers for training
    or testing. Each random integer falls within the range of the respective calling scenario.'''
    holder = random.sample(xrange(number_of_samples), number_of_samples)  # 40
    train_data = holder[:task_split_samples]
    test_data = holder[task_split_samples:task_total_samples]
    return(train_data, test_data)


def sample_mapper(sample_list, subject_list, task_list, subject_sample_numbers, task_sample_numbers, subjects_data):
    '''Return actual samples based on the sample_list.'''
    sample_data = []
    # print(sample_list, subject_list, task_list, subject_sample_numbers, task_sample_numbers)
    for sample in sample_list:
        # print(sample)
        for subject_index, subject_total_samples in enumerate(subject_sample_numbers):
            if sample >= subject_total_samples:
                sample -= subject_total_samples
            else:
                select_subject = subject_list[subject_index]
                # print(sample, select_subject)
                break
        for task_index, task_total_samples in enumerate(task_sample_numbers):
            if sample >= task_total_samples:
                sample -= task_total_samples
            else:
                select_task = task_list[task_index]
                # print(sample, select_task)
                break
        for trial_index, trial_total_samples in enumerate(subjects_data[select_subject][0][select_task][1]):
            if sample >= trial_total_samples:
                sample -= trial_total_samples
            else:
                # select_trial = trial_index
                select_sample = subjects_data[select_subject][0][select_task][0][trial_index][sample]
                break
        # print(select_subject, select_task, select_trial, sample)
        sample_data.append(select_sample)
    return(sample_data)


# def sample_mapper(sample_list, target_task_list, parsed_data):
#     '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
#     Do a try-except test before grouping the samples.'''
#     sample_data = []
#     for sample in sample_list:
#         select_task = target_task_list[(sample / task_total_samples)]
#         select_trial = (sample % task_total_samples) / samples_per_trial
#         select_sample = (sample % samples_per_trial) * vector_resolution
#         try:
#             parsed_data[select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
#         except IndexError:
#             continue
#         grouper = []
#         # print(select_task, select_trial, select_sample)
#         for i in range(vector_resolution):
#             grouper.append(parsed_data[select_task][select_trial][select_sample+i]['binnedPS'])
#         sample_data.append(grouper)
#     return(sample_data)
#
#
# def subject_mapper(sample_list, subject_list, task, parsed_data):
#     '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
#     Do a try-except test before grouping the samples.'''
#     sample_data = []
#     for sample in sample_list:
#         select_subject = subject_list[(sample / task_total_samples)]
#         select_trial = (sample % task_total_samples) / samples_per_trial
#         select_sample = (sample % samples_per_trial) * vector_resolution
#         try:
#             parsed_data[select_subject][task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
#         except IndexError:
#             continue
#         grouper = []
#         # print(select_task, select_trial, select_sample)
#         for i in range(vector_resolution):
#             grouper.append(parsed_data[select_subject][task][select_trial][select_sample+i]['binnedPS'])
#         sample_data.append(grouper)
#     return(sample_data)
#
#
# def space_mapper(sample_list, subject_list, task_list, parsed_data):
#     '''Return actual samples based on the sample_list, but given not all trials have the same 12 secs length,
#     Do a try-except test before grouping the samples.'''
#     sample_data = []
#     # print(sample_list)
#     # print(subject_list)
#     # print(len(subject_list)*task_total_samples)
#     for sample in sample_list:
#         select_subject = subject_list[(sample / (len(task_list)*task_total_samples))]
#         select_task = task_list[(sample % (len(task_list)*task_total_samples)) / task_total_samples]
#         select_trial = (sample % task_total_samples) / samples_per_trial
#         select_sample = (sample % samples_per_trial) * vector_resolution
#         # print(select_subject, select_task, select_trial, select_sample)
#
#         try:
#             parsed_data[select_subject][select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
#         except IndexError:
#             continue
#         grouper = []
#         for i in range(vector_resolution):
#             grouper.append(parsed_data[select_subject][select_task][select_trial][select_sample+i]['binnedPS'])
#         sample_data.append(grouper)
#     return(sample_data)
