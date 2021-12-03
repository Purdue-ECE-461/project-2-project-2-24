# import metric functions # pragma: no cover
from responsiveness import responsiveness # pragma: no cover
from bus_factor import bus_factor # pragma: no cover
from correctness import correctness # pragma: no cover
from ramp_up_time import ramp_up_time # pragma: no cover
from license_compatability import license_compatability # pragma: no cover
from fraction_dependency import fraction_dependency # pragma: no cover
from metric_helper import metric_helper # pragma: no cover
import tempfile # pragma: no cover

class Repository:
    '''
    Stores Repository objects that are being analyzed.
    '''
    NUM_METRICS=6 # pragma: no cover
    RAMP_UP=0 # pragma: no cover
    BUS_FACTOR=1 # pragma: no cover
    CORRECTNESS=2 # pragma: no cover
    LICENSE=3 # pragma: no cover
    RESPONSIVENESS=4 # pragma: no cover
    FRACTION_DEPENDENCY=5 # pragma: no cover

    def __init__(self):
        self.met_help = None
        self.url= ''
        self.repo_owner=''
        self.repo_name=''
        self.overall_score=0
        self.metric_scores = [0]*self.NUM_METRICS
        self.dir = tempfile.TemporaryDirectory()

    def calc_overall(self):
        '''
        Calculates a weighted net score based on the individual metrics calculated
        '''
        self.overall_score=((self.metric_scores[self.RESPONSIVENESS]*0.4) + (self.metric_scores[self.CORRECTNESS]*0.2) \
            +(self.metric_scores[self.RAMP_UP]*0.15)+(self.metric_scores[self.BUS_FACTOR]*0.15)+(self.metric_scores[self.LICENSE]*0.1)
            +(float(self.metric_scores[self.FRACTION_DEPENDENCY])*0.2))
    
    def calc_metrics(self, dependency_list):
        self.metric_scores[self.RESPONSIVENESS] = responsiveness(self.met_help)
        self.metric_scores[self.BUS_FACTOR] = bus_factor(self.met_help)
        self.metric_scores[self.CORRECTNESS] = correctness(self.dir.name)
        self.metric_scores[self.RAMP_UP] = ramp_up_time(self.dir.name)
        self.metric_scores[self.LICENSE] = license_compatability(self.dir.name)
        self.metric_scores[self.FRACTION_DEPENDENCY] = fraction_dependency(dependency_list)
    
    def print_metrics(self):
        '''
        Prints out the metrics in the example provided by the client
        '''
        print(self.url,end=" ")
        print("%.1f" % (self.overall_score),end=" ")
        print("%.1f" % (self.metric_scores[Repository.RAMP_UP]),end=" ")
        print("%.1f" % (self.metric_scores[Repository.CORRECTNESS]),end=" ")
        print("%.1f" % (self.metric_scores[Repository.BUS_FACTOR]),end=" ")
        print("%.1f" % (self.metric_scores[Repository.RESPONSIVENESS]),end=" ")
        print("%.1f" % (self.metric_scores[Repository.LICENSE]),end=" ")
        print("%.1f" % float((self.metric_scores[Repository.FRACTION_DEPENDENCY])))

    def flag_check(self):
        if round(self.metric_scores[self.RESPONSIVENESS],1) >= 0.5 and round(self.metric_scores[self.BUS_FACTOR],1) >= 0.5 and round(self.metric_scores[self.CORRECTNESS],1) >= 0.5 and round(self.metric_scores[self.RAMP_UP],1) >= 0.5 and round(self.metric_scores[self.LICENSE],1) >= 0.5 and round(float(self.metric_scores[self.FRACTION_DEPENDENCY]),1) >= 0.5:
            return True
        return False     
