# coding:utf-8



class Accuracy:
    def __init__(self):
        self.mean = None
        self.median = None
        self.variance = None
        self.semiVariance = None
        self.expectedValue = None



class Model:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.data = ""
        self.categoryID = 0
        self.filterList = {}
        self.accuracy = Accuracy()

    def get_input(self):
        return self.data

    def get_filter(self, filter_id):
        return self.filterList.get(filter_id)

    def set_filter(self, key_id, value):
        self.filterList[key_id] = value

    
    def train(self):
        return

    def run(self):
        return

    def predict(self):
        return

    def calculate_mean(self):
        return

    def calculate_median(self):
        return

    def calculate_variance(self):
        return

    def calculate_semi_variance(self):
        return

    def calculate_expected_value(self):
        return

    def get_best_filter(self):
        return

    
    def add_into_category(self, id, filter_id):
        return