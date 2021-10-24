import os, time, sys
import configparser
import glob
from datetime import datetime
import logging

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('FileRemover.cfg')

    logfile = config['Logging']['LogFile'] + datetime.now().strftime('-%Y%m%d.log')
    loglevel = config['Logging']['LogLevel']
    logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s',
                        filename=logfile, encoding='utf-8', level=loglevel, filemode="a+")

    logging.info(f'**** START {sys.argv[0]} ****')
    path = config['FileRemover']['Folder']
    file_filter = config['FileRemover']['Filter']
    now = time.time()

    file_list = glob.glob(path + f"\\{file_filter}")
    for f in file_list:
        logging.info(f'{f},' + str(os.stat(f)))
        if os.stat(f).st_mtime < now - 7 * 86400:
            if os.path.isfile(f):
                logging.info(f'Remove {f}')
                os.remove(os.path.join(path, f))
    logging.info(f'**** END {sys.argv[0]} ****')
