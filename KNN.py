import numpy as np


class KNN:
    def __init__(self, k_value, x_train, y_train, y_name):
        # 군집 수 k를 k_value로 저장
        self.k_value = k_value
        # 학습용 데이터
        self.x_train = x_train
        self.y_train = y_train
        self.y_name = y_name
        # 가까운 k개의 점과 그 거리를 저장한다.
        self.distance_result = np.zeros(self.x_train.shape[0])
        self.result = np.zeros(self.k_value)

    # 두 점 사이의 거리를 구한다.
    def distance(self, p1, p2):
        return np.sqrt(np.sum(np.power((p2 - p1), 2)))

    # 가장 가까운 점을 구한다.
    def get_neareast_k(self, test_data):
        # 거리들을 구하기 위해 데이터 차수만큼 거리를 저장할 리스트를 생성
        # test data와 기존 데이터(학습 데이터)와 거리 차이를 구한다.
        for i in range(self.x_train.shape[0]):
            self.distance_result[i] = KNN.distance(self, self.x_train[i], test_data)

        # 거리를 기준으로 가까운 것들을 정렬한다.
        sorted_index = np.argsort(self.distance_result)[:self.k_value]

        # 거리를 짧은 순서대로 정렬한다.
        np.sort(self.distance_result)
        # result에 가까운 점들의 객체 종류를 담는다.
        for i in range(self.k_value):
            self.result[i] = self.y_train[sorted_index[i]]

    def majority_vote(self):
        # 주변 꽃 종류 개수 결과를 담기 위한 리스트
        # 순서대로 0 = setosa, 1 = versicolor, 2 = virginica
        vote_result = [0 for _ in range(self.y_name.shape[0])]

        # 가까운 k개가 어떤 종류인지 count해준다.
        for i in range(self.result.shape[0]):
            vote_result[int(self.result[i])] = vote_result[int(self.result[i])] + 1

        # 가장 유력한 꽃을 정렬 (= 결과 값)
        output_result = np.argsort(vote_result)[:len(vote_result)]
        return self.y_name[output_result[len(vote_result) - 1]]

    def weighted_majority_vote(self):
        # 주변 꽃 개수 결과를 담기 위한 리스트
        # 순서대로 0 = setosa, 1 = versicolor, 2 = virginica
        vote_result = [0 for _ in range(self.y_name.shape[0])]

        # 가중치를 더한다. 이 때 가중치는 거리에 1/(시그모이드 함수를 씌운 값)으로 정한다..
        for i in range(self.result.shape[0]):
            vote_result[int(self.result[i])] = vote_result[int(self.result[i])] + 1 / (KNN.sigmoid(self,
                                                                                                   self.distance_result[
                                                                                                       i]))

        # 가장 유력한 꽃 (= 결과 값)
        output_result = np.argsort(vote_result)[:len(vote_result)]
        return self.y_name[output_result[len(vote_result) - 1]]

    # 데이터 차수가 얼마나 되는지 화면에 보여주기 위한 메소
    def show_dim(self):
        print("Input Dimension: ", self.x_train.shape)
        print("Output Dimension: ", self.y_train.shape)

    # 시그모이드 함수
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # 다음 테스트 데이터를 위해 가까운 점과 거리를 초기화한다.
    def reset(self):
        self.distance_result = np.zeros(self.x_train.shape[0])
        self.result = np.zeros(self.k_value)
