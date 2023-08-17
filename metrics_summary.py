import os
import sys
import pandas as pd
import datetime
from utils import Utils


def print_help():
    print(f'Wrong numer of arguments.')
    print(f'Expected: python metrics_summary.py <directory> [<input_reports_file>]')
    print(f'\t e.g: python metrics_summary.py ./test_1')


if len(sys.argv) < 2:
    print_help()
    exit()

DIRECTORY = sys.argv[1]

if not os.path.exists(DIRECTORY):
    raise ValueError(f"Not found source directory {DIRECTORY}")

DIRECTORIES = [
    f'./{DIRECTORY}/AA_618_A59/output',
    f'./{DIRECTORY}/AA_635_A45/output',
    f'./{DIRECTORY}/AA_661_A118/output'
]

MAIN_METRICS_REPORT_DIR = './main_metrics_reports'

if not os.path.exists(MAIN_METRICS_REPORT_DIR):
    os.mkdir(MAIN_METRICS_REPORT_DIR)

now = datetime.datetime.now()
date_formatted = now.strftime("%Y%m%dT%H%M%S")
report_dir = 'main_metrics_report_' + date_formatted
subdir = f'{MAIN_METRICS_REPORT_DIR}/{report_dir}'
os.mkdir(subdir)

# create output reports file
now_report = datetime.datetime.now()
date_formatted_report = now_report.strftime("%Y%m%dT%H%M%S")
OUTPUT_REPORTS_FILE = f'{subdir}/input_reports_{date_formatted_report}'

df_all = {}
clusters_all = []
hyper_params_all = []

test_run = 0
with open(OUTPUT_REPORTS_FILE, 'w') as output_report_file_handler:
    if len(sys.argv) > 2:
        input_reports_file = sys.argv[2]
        print(f'Using input report file: {input_reports_file}')
        if not os.path.exists(input_reports_file):
            raise ValueError(f'Not found input reports file: {input_reports_file}')
        # read lines -> report for input
        reports = Utils.read_file_by_lines(input_reports_file)
        for path in reports:
            Utils.add_report_for_metrics(path, df_all, clusters_all, hyper_params_all, test_run)
            output_report_file_handler.write(f'{path}\n')
            test_run = test_run + 1
    else:
        print(f'Using default reports mechanism. Reading all report directories')
        for work_dir in DIRECTORIES:
            report_directories = os.listdir(work_dir)
            report_directories.sort()
            for report_dir in report_directories:
                if report_dir.startswith('report_'):
                    path = f'{work_dir}/{report_dir}'
                    Utils.add_report_for_metrics(path, df_all, clusters_all, hyper_params_all, test_run)
                    output_report_file_handler.write(f'{path}\n')
                    test_run = test_run + 1

new_files, new_plus_files = Utils.generate_metrics_summary(df_all, subdir)
counts_file = Utils.create_counts_report(df_all, subdir)
Utils.generate_metrics_summary_html(subdir, new_files, new_plus_files, clusters_all, hyper_params_all, counts_file)

print('Done.')
