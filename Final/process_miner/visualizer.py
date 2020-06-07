# coding:utf-8

from pm4py.objects.log.importer.csv import factory as csv_importer  
from pm4py.objects.log.importer.xes import factory as importer      
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as visualizer
from pm4py.util import constants
import global_util
import os
# filter
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.cases import case_filter
from pm4py.objects.log.log import EventLog


class Pm4pyTools(object):
    def __init__(self, file):
        file_path = None
        if not os.path.abspath(file):
            # If it's not absolute path, get path
            self.fileName = global_util.get_full_path_input_file(file)
        else:
            # otherwise set file_path as file
            self.fileName = file
        self.log = None

    def get_xes_log(self):
        # importing log to time sort
        parameters = {"timestamp_sort": True}
        self.log = importer.apply(self.fileName, variant="nonstandard", parameters=parameters)
        return self.log

    # return the time sorted object
    def get_all_sorted_time(self):
        timestamp_list = []
        if self.log is not None:
            for trace in self.log:
                for event in trace:
                    # print(type(event.get("time:timestamp")))
                    timestamp_list.append(event.get("time:timestamp"))
        return timestamp_list

    def set_log(self, log):
        self.log = log

    def filter_time_data(self, timestamps, time_weight):
        if not isinstance(time_weight, float):
            raise TypeError

        if time_weight > 1 or time_weight < 0:
            raise ValueError

        if timestamps is None or len(timestamps) == 0:
            return False

        event_size = len(timestamps)
        used = int(event_size * time_weight)
        filtered = event_size - used
        if event_size == 0 or used == 0:
            return None

        begin = int(filtered/2)
        end = begin + used - 1
        begin_time = timestamps[begin].strftime("%Y-%m-%d %H:%M:%S")
        end_time = timestamps[end].strftime("%Y-%m-%d %H:%M:%S")
        df_times_intersecting = timestamp_filter.filter_traces_intersecting(self.log, begin_time, end_time)
        return df_times_intersecting

    @staticmethod
    def filter_case_data(log):
        return log

    def show_log(self, log):
        # Miner application log file
        net, initial_marking, final_marking = alpha_miner.apply(log)

        # Visual interface application analysis results
        gviz = visualizer.apply(net, initial_marking, final_marking)

        
        file, _ = os.path.splitext(os.path.basename(self.fileName))
        output_full_name = "output_time_filtered_" + file + ".png"

      
        output_file = global_util.get_full_path_output_file(output_full_name)
        print(output_file)

       
        visualizer.save(gviz, output_file)

      
        return output_full_name


# Import event log
def import_xes_data(filename):
    if not os.path.abspath(filename):
       
        file_path = global_util.get_full_path_input_file(filename)
    else:
        file_path = filename
        filename = os.path.basename(filename)

    # import the name of log
    parameters = {"timestamp_sort": True}
    log = importer.apply(file_path, variant="nonstandard", parameters=parameters)
    print(log)

    # file of miner application log
    net, initial_marking, final_marking = alpha_miner.apply(log)

    # Visual interface application analysis results
    gviz = visualizer.apply(net, initial_marking, final_marking)

    # Generate output file name
    file, _ = os.path.splitext(filename)
    output_full_name = "output_" + file + ".png"
    # Generate the full path of the output file
    output_file = global_util.get_full_path_output_file(output_full_name)

    # save document
    visualizer.save(gviz, output_file)
    # Returns the output file name
    return output_full_name



def import_csv_file(filename):
    filename = os.path.basename(filename)
    
    file_path = global_util.get_full_path_input_file(filename)

    
    event_stream = csv_importer.import_event_stream(file_path)
    # dataframe = csv_import_adapter.import_dataframe_from_path(file_path, sep=",")

    
    log = conversion_factory.apply(event_stream, parameters={constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "日期和时间"})

    
    net, initial_marking, final_marking = alpha_miner.apply(log)

    
    gviz = visualizer.apply(net, initial_marking, final_marking)

   
    visualizer.view(gviz)


def test_import_xes_data(filename):
    filename = os.path.basename(filename)

    
    file_path = global_util.get_full_path_test_file(filename)

   
    log = importer.apply(file_path)
    for case_index, case in enumerate(log):
        print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
        for event_index, event in enumerate(case):
            print("event index: %d  event activity: %s" % (event_index, event["concept:name"]))

    
    parameters = {"timestamp_sort": True}
    log = importer.apply(file_path, variant="nonstandard", parameters=parameters)
    for case_index, case in enumerate(log):
        print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
        for event_index, event in enumerate(case):
            print("event index: %d  event activity: %s" % (event_index, event["concept:name"]))


if __name__ == "__main__":
    # test_import_xes_data("running.xes")
    # import_xes_data("running.xes")

    curr_path = os.path.dirname(os.path.abspath(__file__))
    print(curr_path)
    input_file = os.path.join(curr_path, "..", "input_file", "running.xes")
    print(os.path.abspath(input_file))
    tool = Pm4pyTools(os.path.abspath(input_file))
    log = tool.get_xes_log()
    tool.filter_case_data(log)
    # timestamps = tool.get_all_sorted_time()
    # tool.filter_time_data(timestamps, 0.3)
