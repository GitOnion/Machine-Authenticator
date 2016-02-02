from random import shuffle

vector_resolution = 3
trial_times = 10 #10
seconds_per_trial = 12 #12
samples_per_trial = seconds_per_trial / vector_resolution #4

task_total_seconds = trial_times * seconds_per_trial #120
task_total_samples = task_total_seconds / vector_resolution #40
task_split_samples = task_total_samples / 2 #20

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
    # For scenario 'passthought', the return random samples are drawn from one task of one single subject.
    # For scenario 'forgot_passthought', random samples are drawn from all tasks other than the one
    # passthought of one single subject.
    #
    # if scenario == 'forgot_passthought':
    #     holder = [x for x in range(subject_other_samples)] #240
    # # elif scenario == 'passthought_leakage':
    # #     holder = [x for x in range(task_total_samples)]
    # # elif scenario == 'brute_force':
    # #     holder = [x for x in range(task_total_samples)]
    # elif scenario == 'passthought':
    holder = [x for x in range(number_of_tasks * task_total_samples)] #40
    shuffle(holder)
    train_data = holder[:task_split_samples]
    test_data = holder[task_split_samples:task_total_samples]
    return(train_data, test_data)


def sample_mapper(sample_list, target_task_list, parsed_data):
    '''Return actual Based on the sample_list, '''
    sample_data = []
    for sample in sample_list:
        select_task = target_task_list[(sample / task_total_samples)]
        select_trial = (sample % task_total_samples) / samples_per_trial
        select_sample = (sample % samples_per_trial) * vector_resolution
        try:
            poke = parsed_data[select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS']
        except IndexError:
            continue
        grouper = []
        # print(select_task, select_trial, select_sample)
        for i in range(vector_resolution):
            grouper.append(parsed_data[select_task][select_trial][select_sample+i]['binnedPS'])
        sample_data.append(grouper)
    return(sample_data)


            # if len(target_task_list) == 1:
            #     test_sample.pop()
            #     continue
            # else:
            #     select_task, select_trial, select_sample = sample_mapper(sample_range[task_total_samples])
            #     task_total_samples += 1
            #     sample = parsed_data[select_task][select_trial][select_sample+i]['binnedPS'])


# def random_sampler(target_task_list, parsed_data):
#     '''Return actual Based on the sample_list, '''
#     sample_range = [x for x in range(len(target_task_list) * task_total_samples)] #40
#     shuffle(sample_range)
#     train_sample = sample_range[:task_split_samples]
#     test_sample = sample_range[task_split_samples:task_total_samples]
#
#     select_task, select_trial, select_sample = sample_mapper(train_sample)
#     train_data = []
#     grouper = []
#     # print(select_task, select_trial, select_sample)
#     for i in range(vector_resolution):
#         try:
#             sample = parsed_data[select_task][select_trial][select_sample+(vector_resolution-1)]['binnedPS'])
#         except IndexError:
#             continue
#         grouper.append(sample)
#     train_data.append(grouper)
#
#     test_data = []
#
#
#
#
#
#
#     for sample in [train_sample, test_sample]:
#     return(sample_data)
#     return(train_data, test_data)
#
#
# def sample_mapper(sample_list):
#     for sample in sample_list:
#         select_task = target_task_list[(sample / task_total_samples)]
#         select_trial = (sample % task_total_samples) / samples_per_trial
#         select_sample = (sample % samples_per_trial) * vector_resolution
#     return(select_task, select_trial, select_sample)
#
#
# def sample_getter():

# def sample_logger():
    # TODO
