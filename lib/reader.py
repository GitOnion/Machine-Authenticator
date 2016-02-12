import json
import fnmatch
from os import listdir
from os import path
import numpy as np
from lib import brainlib
from lib import learner


def get_all_data_files(dataset_folder):
    '''Get all subjects' reading files into a list.'''
    return(path.join(dataset_folder, subject) for subject in fnmatch.filter(listdir(dataset_folder), '*.csv'))


def read_file(file_name):
    '''Get one subject's readings, which is stored in JSON, and return lists'''
    rawdata = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            rawdata.append(json.loads(line[:-2]))
        return(rawdata)


def clean_readings(reading):
    '''Take in the 'reading' JSON object, get the raw_values, and cast all values into float.'''
    vals = reading['raw_values'].split(',')
    return(np.array(vals).astype(np.float))


def fft_power_spectrum(reading):
    '''Make the reading power spectrum. Put a wrapper here to make the data transformation clear.'''
    return([brainlib.pSpectrum(reading)])


def bin_power_spectrum(power_spectrum):
    '''Create 100, log10-spaced bins for each power spectrum. See the work of Merrill et al.:
    Merrill, N., Maillart, T., Johnson, B., & Chuang, J. "Improving Physiological Signal
    Classification Using Logarithmic Quantization and a Progressive Calibration Technique."
    Physiological Computing Systems 2015. Angers, France.'''
    return(brainlib.binnedPowerSpectra(power_spectrum, 100))


def binned_PS(reading):
    '''Put everything together'''
    return({'sq': reading['signal_quality'], 'binnedPS': bin_power_spectrum(fft_power_spectrum(clean_readings(reading)))[0]})
    # Note: The BinnesPS is a layer of list inside, which is somewhat redundant.


def form_subject_object(subject_data_in_Json):
    ''' For one subject, create a dictionary of tasks, in which the keys are the task names,
    and values are lists (to preseve the order) of trials. Trials are seperated using the
    'receivedAt' value. In each task list are trial lists, each contains seconds (in our setting,
    it should be 12 seconds per trial ideally, but can vary from 8 to 16, due to the instability
    of the connection between Mindwave device and data collection server).Each second is a
    dictionary of 'raw', binned power spectrum of the raw values, and 'sq', the signal quality.'''

    parsed_data = {}
    for sec in subject_data_in_Json:
        if sec['tag'] not in parsed_data:
            parsed_data[sec['tag']] = [[binned_PS(sec['reading'])]]
            trial_start_time = sec['receivedAt']
        else:
            if sec['receivedAt'] == trial_start_time:
                parsed_data[sec['tag']][-1].append(binned_PS(sec['reading']))
            else:
                parsed_data[sec['tag']].append([binned_PS(sec['reading'])])
                trial_start_time = sec['receivedAt']
    return(parsed_data)


def subject_object_checker(subjects_data):
    for subj in subjects_data:
        print('Subject ' + subj + ' has data for ' + str(len(subjects_data[subj])) + ' tasks.')
        for i in subjects_data[subj]:
            print('for task ' + i)
            print(type(subjects_data[subj][i]), len(subjects_data[subj][i]))
            h = []
            print('Instances that signal quality greater than 0 are: ')
            for j in subjects_data[subj][i]:
                h.append(len(j))
                for k in j:
                    if k['sq'] != 0:
                        print k['sq'],  # This is only For Python2.
            print('\nMax data entries: ' + str(max(h)) + ', Min data entries: ' + str(min(h)) + '\n')


def feature_vector_transformer(subject_data, tasks_list, vector_resolution):
    '''Generate feature vectors from all data of a subject, with the given vector resolution.
    For each trial in each task, there are supposed to be certain number of feature vectors.
    Check if there's enough data for each feature vector. if so, generate one. If not, dispose
    the data. Keep track of the numbers of feature vectors in all trials in a seperate list.
    Finally, return the new task data as a tuple of 1. the feature vectors and 2. the list.'''
    new_subject_object = {}
    for task_key in tasks_list:
        new_task_object = []
        sample_numbers = []  # keeps track of sample numbers of each trial.
        for trial_data in subject_data[task_key]:
            sample_counts = len(trial_data)/vector_resolution
            new_trial_object = []
            for vector in range(sample_counts):
                sample_start = vector*(vector_resolution)
                try:
                    trial_data[sample_start+(vector_resolution-1)]['binnedPS']
                except IndexError:
                    continue
                grouper = []
                # print(select_task, select_trial, select_sample)
                for i in range(vector_resolution):
                    grouper.append(trial_data[sample_start+i]['binnedPS'])
                new_trial_object.append(learner.feature_vector_generator(grouper))
            new_task_object.append(new_trial_object)
            sample_numbers.append(len(new_trial_object))
        new_subject_object[task_key] = (new_task_object, sample_numbers)
        # print(task_key, sample_numbers)
        # print(new_subject_object[task_key][1])
    return(new_subject_object)
