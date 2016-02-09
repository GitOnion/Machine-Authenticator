from itertools import combinations
from operator import itemgetter
from sklearn import svm
from lib import selector
from lib import learner
import numpy as np


def pair_comparison(subjects_data, tasks_list, times):
    '''Scenario 0: Get the highest mean cross_validation score of two taks, from all possible task pairs within subject.'''

    log_file_name = 'Scenario0_log.txt'
    log = open(log_file_name, 'w')
    print("Scenario 0: Pair Comparison")
    for target_subject in sorted(subjects_data.keys()):
        print('For subject ' + str(target_subject) + ' : ')
        logger = '{"' + target_subject + '":{'

        all_possible_pairs = combinations(tasks_list, 2)
        scores_holder = []
        for tasks_pair in all_possible_pairs:
            task1 = reduce(lambda x, y: x + y, subjects_data[target_subject][0][tasks_pair[0]][0])
            task2 = reduce(lambda x, y: x + y, subjects_data[target_subject][0][tasks_pair[1]][0])
            X, y = learner.labeler([task1, task2])
            scores_holder.append([learner.crossValidate(X, y), tasks_pair[0], tasks_pair[1]])
            logger += '"' + tasks_pair[0] + ' vs. ' + tasks_pair[1] + '": "' + str(scores_holder[-1][0]) + '", '
        best_pair = max(scores_holder, key=itemgetter(0))
        print(best_pair)

        logger = logger[:-2] + '}}\n'
        log.write(logger)
    log.close()
    return


def forgot_passthought(subjects_data, tasks_list, times):
    '''Scenario 1: A subject forgets his own passthought and tries to authenticate himself.'''

    log_file_name = 'Scenario1_log.txt'
    log = open(log_file_name, 'w')
    print("Scenario 1: Forgot Passthought")
    for target_subject in sorted(subjects_data.keys()):
        print('For subject ' + str(target_subject) + ' : ')
        logger = '{"' + target_subject + '":{'
        subject_sample_numbers = subjects_data[target_subject][1]
        print(subject_sample_numbers)

        for task in tasks_list:
            print('For task: ' + task)
            logger += '"' + task + '":{'
            task_sample_numbers = sum(subjects_data[target_subject][0][task][1])

            others_list = []
            others_sample_numbers = []
            for other_task in tasks_list:
                if other_task == task:
                    continue
                else:
                    others_list.append(other_task)
                    others_sample_numbers.append(sum(subjects_data[target_subject][0][other_task][1]))

            FRR_holder = []
            FAR_holder = []

            for one_sample_run in range(times):
                logger += '"' + str(one_sample_run) + '":{'

                trainer, tester = selector.random_sampler(task_sample_numbers)
                logger += '"target":"' + str(trainer) + ',' + str(tester)
                print(trainer, tester)
                train_data_target = selector.sample_mapper(trainer, [target_subject], [task], [subject_sample_numbers], [task_sample_numbers], subjects_data)
                test_data_target = selector.sample_mapper(tester, [target_subject], [task], [subject_sample_numbers], [task_sample_numbers], subjects_data)

                trainer, tester = selector.random_sampler(sum(others_sample_numbers))
                logger += '","other":"' + str(trainer) + ',' + str(tester) + '"}, '
                print(trainer, tester)
                train_data_other = selector.sample_mapper(trainer, [target_subject], others_list, [subject_sample_numbers], others_sample_numbers, subjects_data)
                test_data_other = selector.sample_mapper(tester, [target_subject], others_list, [subject_sample_numbers], others_sample_numbers, subjects_data)

                X, y = learner.labeler([train_data_target, train_data_other])

                lin_clf = svm.LinearSVC()
                lin_clf.fit(X, y)

                test_result_correct = lin_clf.predict(test_data_target)
                FRR_holder.append(np.mean(test_result_correct))

                test_result_wrong = lin_clf.predict(test_data_other)
                FAR_holder.append(1 - np.mean(test_result_wrong))
            logger = logger[:-2] + '}, '
            print('  FRR = ' + str(np.mean(FRR_holder)) + ', FAR = ' + str(np.mean(FAR_holder)))
        logger = logger[:-2] + '}}\n'
        log.write(logger)
    log.close()
    return
