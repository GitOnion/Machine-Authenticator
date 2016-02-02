from lib import reader
from lib import scenario

dataset_foler = 'dataset'
# tasks_list = ['breath', 'blink']
tasks_list = ['breath', 'blink', 'ocular', 'song', 'hear', 'face', 'cube']
times_of_sampling = 100


def main():
    fileslist = reader.get_all_data_files(dataset_foler)
    for subject_num, subject in enumerate(fileslist):
        subject_data = reader.read_file(subject)
        parsed_data = reader.form_subject_object(subject_data)
        # print(parsed_data['breath'][0][0]['binnedPS'])
        print('For subject' + str(subject_num+1) + ': ')
        scenario.forgot_passthought(tasks_list, parsed_data, times_of_sampling)

    # passthought_leakage(task)
    # brute_force(task)

    # subject's data checker:
    #     print(len(data))
    #     print(len(parsed_data))
    #     for i in parsed_data:
    #         print(i)
    #         print(type(parseddata[i]), len(parseddata[i]))
    #         h = []
    #         for j in parsed_data[i]:
    #             h.append(len(j))
    #             for k in j:
    #                 if k['sq'] != 0:
    #                     print(k['sq'])
    #         print(max(h), min(h))


if __name__ == '__main__':
    main()
