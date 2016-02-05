from lib import reader
from lib import scenario

dataset_foler = 'dataset'
# tasks_list = ['breath', 'blink']
tasks_list = ['breath', 'blink', 'ocular', 'song', 'hear', 'face', 'cube']
times_of_sampling = 100


def main():
    # Loading all of the data for only once.
    fileslist = reader.get_all_data_files(dataset_foler)
    subjects_data = {}
    for subject in fileslist:
        file_handle = reader.read_file(subject)
        parsed_data = reader.form_subject_object(file_handle)
        subject_name = subject[8:11]
        subjects_data[subject_name] = parsed_data
    # Check if the data loads correctly.
    # print(subjects_data.keys())
    # print(len(subjects_data['001']))
    # print(subjects_data['001'].keys())
    # print(subjects_data['001']['breath'][0][0]['binnedPS'])
    # reader.subject_data_checker(subjects_data)

    scenario.forgot_passthought(subjects_data, tasks_list, times_of_sampling)
    scenario.passthought_leakage(subjects_data, tasks_list, times_of_sampling)
    scenario.bruteforce_attack(subjects_data, tasks_list, times_of_sampling)

if __name__ == '__main__':
    main()
