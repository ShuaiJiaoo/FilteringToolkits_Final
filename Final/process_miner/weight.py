# coding:utf-8


class WeightSetting:
    def __init__(self):
        self.name = "default"
        self.data = None

    @staticmethod
    def get_weight(types):
        if types == "time":
            return TimeWeight(types)
        elif types == "storage":
            return StorageWeight(types)
        elif types == "accuracy":
            return AccuracyWeight(types)
        else:
            print("type %s not found", types)

    def set_value(self, data):
        self.data = data

    def calculate_score(self):
        score = -1
        
        return score

    def get_best_filter(self, score):
        return filter


class TimeWeight(WeightSetting):
    def __init__(self):
        self.name = "time"

    def calculate_score(self):
        score = -1
        
        return score


class StorageWeight(WeightSetting):
    def __init__(self):
        self.name = "storage"

    def calculate_score(self):
        score = -1
        
        return score


class AccuracyWeight(WeightSetting):
    def __init__(self):
        self.name = "accuracy"

    def calculate_score(self):
        score = -1
        
        return score

