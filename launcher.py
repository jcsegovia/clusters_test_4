import os
import sys
import datetime
from utils import Utils


SCRIPT = './main.py'
METRICS_SCRIPT = './metrics_summary.py'


def print_help():
    print(f'Wrong numer of arguments.')
    print(f'Expected: python launcher.py <directory>')
    print(f'\t e.g: python launcher.py ./test_1')


if len(sys.argv) < 2:
    print_help()
    exit()

DIRECTORY = sys.argv[1]

if not os.path.exists(DIRECTORY):
    raise ValueError(f"Not found source directory {DIRECTORY}")
    pass

MODEL='all'

EXEC_CLASSIFY = [
    f'-dir={DIRECTORY}/AA_618_A59 -task=classify -cluster=UBC8 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_618_A59 -task=classify -cluster=UBC17_a -model={MODEL}',
    f'-dir={DIRECTORY}/AA_618_A59 -task=classify -cluster=UBC17_b -model={MODEL}',
    f'-dir={DIRECTORY}/AA_635_A45 -task=classify -cluster=UBC106 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_635_A45 -task=classify -cluster=UBC186 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_635_A45 -task=classify -cluster=UBC570 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_661_A118 -task=classify -cluster=UBC1004 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_661_A118 -task=classify -cluster=UBC1015 -model={MODEL}',
    f'-dir={DIRECTORY}/AA_661_A118 -task=classify -cluster=UBC1565 -model={MODEL}'
]


now = datetime.datetime.now()
date_formatted = now.strftime("%Y%m%dT%H%M%S")
metrics_file_tmp = f'./metrics_file_{date_formatted}.tmp'
metrics_file_arg = f'-metrics_file={metrics_file_tmp}'

extra_args = []
for i in range(2, len(sys.argv)):
    extra_args.append(sys.argv[i])

for arg in EXEC_CLASSIFY:
    # items = arg.split(' ')
    # if len(extra_args) > 0:
    #     for extra_arg in extra_args:
    #         items.append(extra_arg)
    items_dict = Utils.create_dictionary_from_args(arg)
    for extra_arg in extra_args:
        Utils.overwrite_dictionary(items_dict, extra_arg)
    items = []
    for k in items_dict.keys():
        items.append(f'{k}={items_dict[k]}')
    print(f'{items}')
    sys.argv.clear()
    sys.argv.append(SCRIPT)
    for i in items:
        sys.argv.append(i)
    sys.argv.append(metrics_file_arg)
    with open(SCRIPT) as f:
        exec(f.read())

# Launch metrics
print('Metrics summary')
sys.argv.clear()
sys.argv.append(METRICS_SCRIPT)
sys.argv.append(DIRECTORY)
sys.argv.append(metrics_file_tmp)
with open(METRICS_SCRIPT) as f:
    exec(f.read())


os.remove(metrics_file_tmp)

print('Done')
