# Unable to use python logger due to its incompatibility with flask at the moment
from datetime import datetime

def log_error(msg):
    # The output will be as the following example:
    #   [2020-05-15 17:08:53.508167] Unable to connect
    current_time = datetime.now()
    with open('./log/error.log', 'a') as log:
        log.write("[{}] {}\n".format(str(current_time), str(msg)))
