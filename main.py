from lib import reader
# from lib import scenario
from lib import scenarios

dataset_foler = 'dataset'
# tasks_list = ['breath', 'blink']
tasks_list = ['breath', 'blink', 'ocular', 'song', 'hear', 'face', 'cube']
times_of_sampling = 1
vector_resolution = 3


def main():
    # Loading all of the data for only once.
    fileslist = reader.get_all_data_files(dataset_foler)
    subjects_data = {}
    for subject in fileslist:
        subject_name = subject[8:11]
        subject_data_in_Json = reader.read_file(subject)
        parsed_data = reader.form_subject_object(subject_data_in_Json)
        # Check if the data loads correctly:
        # reader.subject_object_checker(parsed_data)

        # Use pre-feature_vectorized data:
        # subjects_data[subject_name] = parsed_data

        vectorized_data = reader.feature_vector_transformer(parsed_data, vector_resolution)
        subjects_data[subject_name] = (vectorized_data, reduce(lambda x, y: x + y, [sum(vectorized_data[task][1]) for task in vectorized_data]))
        # Check if the vectorized_data is equivalent to parsed_data:
        # print(subjects_data['001'][0]['breath'][0][0][0])
        # print(learner.feature_vector_generator([parsed_data['breath'][0][0]['binnedPS'], parsed_data['breath'][0][1]['binnedPS'], parsed_data['breath'][0][2]['binnedPS']]))

    scenarios.pair_comparison(subjects_data, tasks_list, times_of_sampling)
    scenarios.forgot_passthought(subjects_data, tasks_list, times_of_sampling)
    # scenario.passthought_leakage(subjects_data, tasks_list, times_of_sampling)
    # scenario.bruteforce_attack(subjects_data, tasks_list, times_of_sampling)

if __name__ == '__main__':
    main()
