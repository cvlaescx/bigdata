from flask import Flask, request, make_response
from metrics import Metrics
import time
from logging import DEBUG

website = Flask(__name__)
website.logger.setLevel(DEBUG)


@website.route('/favicon.ico')
def favicon():
    pass


@website.route('/query', methods=['GET'])
def index():
    from_datetime = request.args.get('from_datetime')
    to_datetime = request.args.get('to_datetime')
    user = request.args.get('user')
    app = request.args.get('app')
    granularity = request.args.get('granularity')
    group_by = request.args.get('group_by')

    start_time = time.perf_counter()

    response_lst = metrics.query(from_datetime,
                                 to_datetime,
                                 user,
                                 app,
                                 granularity,
                                 group_by)

    website.logger.info("{} record(s) in --- {} milliseconds ---".format(len(response_lst),
                                                                         round(
                                                                             1000 * (time.perf_counter() - start_time))
                                                                         ))
    response_strings_lst = [(*keys, str(metric)) for *keys, metric in response_lst]
    response_text = '\n'.join(map(', '.join, response_strings_lst))
    return make_response(response_text, 200)


if __name__ == '__main__':
    metrics = Metrics('logs4')
    website.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
