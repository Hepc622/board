import time, datetime, sys, logging, os

LOG_PATH = os.path.abspath(os.path.join(os.getcwd(), "logs"))


def get_logger():
    i_logger = logging.getLogger(__name__)
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    LOG_FILE = now_time + str(".log")
    # 文件日志
    file_handler = logging.FileHandler("%s/%s" % (LOG_PATH, LOG_FILE))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    i_logger.addHandler(file_handler)
    i_logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    i_logger.setLevel(logging.DEBUG)
    return i_logger


def logger(fn):
    def inner(*args, **kwargs):
        log = get_logger()
        begin = time.time()
        log.debug("in method:" + getattr(fn, '__name__'))
        log.debug("in params:" + str(args))
        result = fn(*args, **kwargs)
        log.debug("out params:" + str(result))
        log.debug("out method:" + getattr(fn, '__name__'))
        end = time.time()
        log.debug("time:" + str(end - begin))

        return result
    return inner