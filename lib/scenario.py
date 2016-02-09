from lib import selector
from lib import learner
from sklearn import svm
import numpy as np


def forgot_passthought(subjects_data, tasks_list, times):
    '''Scenario 1: A subject forgets his own passthought and tries to authenticate himself.'''

    log_file_name = 'Scenario1_log.txt'
    log = open(log_file_name, 'w')
    print("Scenario 1: Forgot Passthought")
    for target_subject in sorted(subjects_data.keys()):
        print('For subject' + str(target_subject) + ': ')
        # log.write('For subject' + str(target_subject) + ':\n')
        logger = '{"' + target_subject + '":{'

        for task in tasks_list:
            print('For task: ' + task + '\n')
            # log.write('For task: ' + task + ':\n')
            logger += '"' + task + '":{'

            others_list = []
            for other_task in tasks_list:
                if other_task == task:
                    continue
                else:
                    others_list.append(other_task)

            FRR_holder = []
            FAR_holder = []

            for one_sample_run in range(times):
                logger += '"' + str(one_sample_run) + '":{'
                seed, trainer, tester = selector.random_sampler(1)
                # log.write('The ' + str(one_sample_run+1) + 'th sample seed: ' + str(seed))
                logger += '"target":"' + str(seed) + ',' + str(trainer) + ',' + str(tester)
                # print(trainer, [task], len(subjects_data[target_subject][task]))
                train_data_target = selector.sample_mapper(trainer, [task], subjects_data[target_subject])
                test_data_target = selector.sample_mapper(tester, [task], subjects_data[target_subject])
                # print(test_data_target)

                seed, trainer, tester = selector.random_sampler(len(others_list))
                logger += '","other":"' + str(seed) + ',' + str(trainer) + ',' + str(tester) + '"}, '
                train_data_other = selector.sample_mapper(trainer, others_list, subjects_data[target_subject])
                test_data_other = selector.sample_mapper(tester, others_list, subjects_data[target_subject])

                Target = learner.feature_vector_generator(train_data_target)
                Other = learner.feature_vector_generator(train_data_other)
                X, y = learner.labeler([Target, Other])
                # print(learner.crossValidate(X, y))

                lin_clf = svm.LinearSVC()
                lin_clf.fit(X, y)

                Correct = learner.feature_vector_generator(test_data_target)
                test_result_correct = lin_clf.predict(Correct)
                # print(test_result_correct)
                FRR_holder.append(np.mean(test_result_correct))

                Wrong = learner.feature_vector_generator(test_data_other)
                test_result_wrong = lin_clf.predict(Wrong)
                # print(test_result_wrong)
                FAR_holder.append(1 - np.mean(test_result_wrong))
            logger = logger[:-2] + '}, '
            print('  FRR = ' + str(np.mean(FRR_holder)) + ', FAR = ' + str(np.mean(FAR_holder)))
        logger = logger[:-2] + '}}\n'
        log.write(logger)
    log.close()
    return


def passthought_leakage(subjects_data, tasks_list, times):
    '''Scenario 2: A subject's passthought was known and attackers try to impersonate him.'''

    log_file_name = 'Scenario2_log.txt'
    log = open(log_file_name, 'w')
    print("Scenario 2: Passthought Leakage")
    for target_subject in sorted(subjects_data.keys()):
        print('For subject' + str(target_subject) + ': ')
        # log.write('For subject' + str(target_subject) + ':\n')
        logger = '{"' + target_subject + '":{'

        for task in tasks_list:
            print('For task: ' + task + '\n')
            # log.write('For task: ' + task + ':\n')
            logger += '"' + task + '":{'

            others_list = []
            for other_subjects in sorted(subjects_data.keys()):
                if other_subjects == target_subject:
                    continue
                else:
                    others_list.append(other_subjects)

            FRR_holder = []
            FAR_holder = []

            for one_sample_run in range(times):
                logger += '"' + str(one_sample_run) + '":{'

                seed, trainer, tester = selector.random_sampler(1)
                # log.write('The ' + str(one_sample_run+1) + 'th sample seed: ' + str(seed))
                logger += '"target":' + str(seed)
                # print(trainer, [task], len(subjects_data[target_subject][task]))
                train_data_target = selector.sample_mapper(trainer, [task], subjects_data[target_subject])
                test_data_target = selector.sample_mapper(tester, [task], subjects_data[target_subject])

                seed, trainer, tester = selector.random_sampler(len(others_list))
                logger += ',"other":' + str(seed) + '}, '
                train_data_other = selector.subject_mapper(trainer, others_list, task, subjects_data)
                test_data_other = selector.subject_mapper(tester, others_list, task, subjects_data)

                Target = learner.feature_vector_generator(train_data_target)
                Other = learner.feature_vector_generator(train_data_other)
                X, y = learner.labeler([Target, Other])
                # print(learner.crossValidate(X, y))

                lin_clf = svm.LinearSVC()
                lin_clf.fit(X, y)

                Correct = learner.feature_vector_generator(test_data_target)
                test_result_correct = lin_clf.predict(Correct)
                # print(test_result_correct)
                FRR_holder.append(np.mean(test_result_correct))

                Wrong = learner.feature_vector_generator(test_data_other)
                test_result_wrong = lin_clf.predict(Wrong)
                # print(test_result_wrong)
                FAR_holder.append(1 - np.mean(test_result_wrong))
            logger = logger[:-2] + '}, '
            print('  FRR = ' + str(np.mean(FRR_holder)) + ', FAR = ' + str(np.mean(FAR_holder)))
        logger = logger[:-2] + '}}\n'
        log.write(logger)
    log.close()
    return


def bruteforce_attack(subjects_data, tasks_list, times):
    '''Scenario 3: A subject has became a target, but passthought secrecy was kept. Attackers try bruteforce.'''

    log_file_name = 'Scenario3_log.txt'
    log = open(log_file_name, 'w')
    print("Scenario 3: Bruteforce Attack")
    for target_subject in sorted(subjects_data.keys()):
        print('For subject' + str(target_subject) + ': ')
        # log.write('For subject' + str(target_subject) + ':\n')
        logger = '{"' + target_subject + '":{'

        for task in tasks_list:
            print('For task: ' + task + '\n')
            # log.write('For task: ' + task + ':\n')
            logger += '"' + task + '":{'

            others_list = []
            for other_subjects in sorted(subjects_data.keys()):
                if other_subjects == target_subject:
                    continue
                else:
                    others_list.append(other_subjects)

            FRR_holder = []
            FAR_holder = []

            for one_sample_run in range(times):
                logger += '"' + str(one_sample_run) + '":{'

                seed, trainer, tester = selector.random_sampler(1)
                # log.write('The ' + str(one_sample_run+1) + 'th sample seed: ' + str(seed))
                logger += '"target":' + str(seed)
                # print(trainer, [task], len(subjects_data[target_subject][task]))
                train_data_target = selector.sample_mapper(trainer, [task], subjects_data[target_subject])
                test_data_target = selector.sample_mapper(tester, [task], subjects_data[target_subject])

                seed, trainer, tester = selector.random_sampler(len(others_list)*7)
                logger += ',"other":' + str(seed) + '}, '
                train_data_other = selector.space_mapper(trainer, others_list, tasks_list, subjects_data)
                test_data_other = selector.space_mapper(tester, others_list, tasks_list, subjects_data)

                Target = learner.feature_vector_generator(train_data_target)
                Other = learner.feature_vector_generator(train_data_other)
                X, y = learner.labeler([Target, Other])
                # print(learner.crossValidate(X, y))

                lin_clf = svm.LinearSVC()
                lin_clf.fit(X, y)

                Correct = learner.feature_vector_generator(test_data_target)
                test_result_correct = lin_clf.predict(Correct)
                # print(test_result_correct)
                FRR_holder.append(np.mean(test_result_correct))

                Wrong = learner.feature_vector_generator(test_data_other)
                test_result_wrong = lin_clf.predict(Wrong)
                # print(test_result_wrong)
                FAR_holder.append(1 - np.mean(test_result_wrong))
            logger = logger[:-2] + '}, '
            print('  FRR = ' + str(np.mean(FRR_holder)) + ', FAR = ' + str(np.mean(FAR_holder)))
        logger = logger[:-2] + '}}\n'
        log.write(logger)
    log.close()
    return

    # print(len(train_data_target), len(train_data_target[1]), len(train_data_target[0][0]))
    # print(len(test_data_target), len(test_data_target[1]), len(test_data_target[0][0]))
    # print(len(train_data_other), len(train_data_other[1]), len(train_data_other[0][0]))
    # print(len(test_data_other), len(test_data_other[1]), len(test_data_other[0][0]))
    # print(train_data_target[0][0], train_data_target[0][1], train_data_target[0][2])
    # print(train_data_target[0][0])
