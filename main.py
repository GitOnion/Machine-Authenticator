from functools import reduce
from lib import reader
from lib import scenarios

dataset_foler = 'dataset'
# tasks_list = ['breath', 'song', 'hear', 'face', 'cube']
tasks_list = ['breath', 'blink', 'ocular', 'song', 'hear', 'face', 'cube']
times_of_sampling = 1
vector_resolution = 3
cut_off_begin = 2  # When giving non-zeor value here, also remember to change the "task_total_seconds" in lib.selector.
cut_off_end = 0
warm_up_trial = 0


def main():
    ''' Loading all of the data for only once.'''
    fileslist = reader.get_all_data_files(dataset_foler)
    subjects_data = {}
    for subject in fileslist:
        subject_name = subject[8:11]
        subject_data_in_Json = reader.read_file(subject)
        parsed_data = reader.form_subject_object(subject_data_in_Json)
        vectorized_data = reader.feature_vector_transformer(parsed_data, tasks_list, vector_resolution, cut_off_begin, cut_off_end, warm_up_trial)
        subjects_data[subject_name] = (vectorized_data, reduce(lambda x, y: x + y, [sum(vectorized_data[task][1]) for task in tasks_list]))

    # scenarios.pair_comparison(subjects_data, tasks_list)
    scenarios.forgot_passthought(subjects_data, tasks_list, times_of_sampling)
    scenarios.passthought_leakage(subjects_data, tasks_list, times_of_sampling)
    scenarios.bruteforce_attack(subjects_data, tasks_list, times_of_sampling)

if __name__ == '__main__':
    main()
