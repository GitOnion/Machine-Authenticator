import json
import fnmatch
from os import listdir
from os import path
import numpy as np
from lib import brainlib


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
    #Note: The BinnesPS is a layer of list inside, which is somewhat redundant.


def form_subject_object(task_data):
    ''' For one subject, create a dictionary of tasks, in which the key is the task name,
    and value is a list (to preseve the order of trials). In the value list are 10 lists,
    each consists of the readings (a dictionary of raw, raw values, and sq, the signal
    quality) of the trial. Trials are seperated by the receivedAt value'''
    parsed_data = {}
    for sec in task_data:
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
