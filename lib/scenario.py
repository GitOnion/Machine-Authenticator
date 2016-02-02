from lib import selector
from lib import learner
from sklearn import svm
import numpy as np


def forgot_passthought(tasks_list, parsed_data, times):
    '''Scenario 1: A subject forgets his own passthought, trying to authenticate himself.'''
    for task in tasks_list:
        FRR_holder = []
        FAR_holder = []
        print('For task: ' + task)
        for sample in range(times):

            trainer, tester = selector.random_sampler(1)
            train_data_target = selector.sample_mapper(trainer, [task], parsed_data)
            test_data_target = selector.sample_mapper(tester, [task], parsed_data)

            others_list = []
            for other_task in tasks_list:
                if other_task == task:
                    continue
                else:
                    others_list.append(other_task)

            trainer, tester = selector.random_sampler(len(others_list))
            train_data_other = selector.sample_mapper(trainer, others_list, parsed_data)
            test_data_other = selector.sample_mapper(tester, others_list, parsed_data)

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
        print('  FRR = ' + str(np.mean(FRR_holder)) + ', FAR = ' + str(np.mean(FAR_holder)))





    # print(len(train_data_target), len(train_data_target[1]), len(train_data_target[0][0]))
    # print(len(test_data_target), len(test_data_target[1]), len(test_data_target[0][0]))
    # print(len(train_data_other), len(train_data_other[1]), len(train_data_other[0][0]))
    # print(len(test_data_other), len(test_data_other[1]), len(test_data_other[0][0]))
    # print(train_data_target[0][0], train_data_target[0][1], train_data_target[0][2])
    # print(train_data_target[0][0])


# subject's data checker:
    # print(len(data))
    # print(len(parseddata))
    # for i in parseddata:
    #     print(i)
    #     print(type(parseddata[i]), len(parseddata[i]))
    #     # h = []
    #     for j in parseddata[i]:
    #         # h.append(len(j))
    #         print(type(j), len(j))
    #         for k in j:
    #             if k['sq'] != 0:
    #                 print(k['sq'])
    #     print(max(h), min(h))

# Scenario that test for all subjects
    # alldata = datareader.integrate_all_subject(fileslist)
