import os, time, sys
import configparser
import glob
from datetime import datetime
import logging
import gzip
import shutil

SECS_PER_DAY = 86400


def load_config(cfg_filename):
    config = configparser.ConfigParser()
    config.read(cfg_filename)
    logfile = config['Logging']['LogFile'] + datetime.now().strftime('-%Y%m%d.log')
    loglevel = config['Logging']['LogLevel']
    logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s',
                        filename=logfile, encoding='utf-8', level=loglevel, filemode="a+")
    return config


def compress_file(filename):
    with open(filename, 'rb') as f_in:
        with gzip.open(f'{filename}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def compress_old_files(config):
    compress_after_days = int(config['Compress']['CompressAfterDays'])
    if compress_after_days <= 0:
        logging.info(f'compress after {compress_after_days} days so NO COMPRESSION')
        return

    path = config['FileRemover']['Folder']
    file_filter = config['Compress']['Filter']
    compress_after_days = int(config['Compress']['CompressAfterDays'])
    logging.info(f'compress after {compress_after_days} days, Folder {path} filter {file_filter}')
    now = time.time()

    file_list = glob.glob(path + f"\\{file_filter}")
    for f in file_list:
        logging.info(f'{f},' + str(os.stat(f)))
        if os.stat(f).st_mtime < now - compress_after_days * SECS_PER_DAY:
            if os.path.isfile(f):
                logging.info(f'Compress {f} ')
                compress_file(f)
                os.remove(f)


def remove_old_files(config):
    path = config['FileRemover']['Folder']
    file_filter = config['FileRemover']['Filter']
    keep_days = int(config['FileRemover']['KeepDays'])
    logging.info(f'Keep {keep_days} days, Folder {path} filter {file_filter}')
    now = time.time()

    file_list = glob.glob(path + f"\\{file_filter}")
    for f in file_list:
        logging.info(f'{f},' + str(os.stat(f)))
        if os.stat(f).st_mtime < now - keep_days * SECS_PER_DAY:
            if os.path.isfile(f):
                logging.info(f'Remove {f}')
                os.remove(f)


if __name__ == '__main__':
    config_handler = load_config('FileRemover.cfg')
    logging.info(f'**** START {sys.argv[0]} ****')
    remove_old_files(config_handler)
    compress_old_files(config_handler)
    logging.info(f'**** END {sys.argv[0]} ****')
