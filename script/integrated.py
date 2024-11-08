import os
import re
import time
import random
import openpyxl
import argparse

from tqdm import tqdm

# CLI args
parser = argparse.ArgumentParser(description="Set the BITCODE_NAME.")
parser.add_argument('--bc', help="Specify the bitcode name", required=True)

# Custom constants
ROOT_PATH = '/home/yyy/sea-dsa/yyytest'
ARGS_FILE = 'opt14.txt'
# BITCODE_NAME = 'bash'
args = parser.parse_args()
BITCODE_NAME = args.bc

# Constants
TOTAL_ITER = 100 # Total combinations of passes to run
RANDOM_SEED = 15
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[39m"

# Globals
success_count = 0

# Init
random.seed(RANDOM_SEED)
work_path = os.path.join(ROOT_PATH, BITCODE_NAME)
output_path = os.path.join(work_path, "output")
bc_path = os.path.join(work_path, f'{BITCODE_NAME}.bc')
temp_bc_path = os.path.join(output_path, 'temp.bc')
opt_path = os.path.join(output_path, 'opt')
nander_path = os.path.join(output_path, 'nander')
fspta_path = os.path.join(output_path, 'fspta')
seadsa_path = os.path.join(output_path, 'seadsa')
xlsx_path = os.path.join(output_path, f'{BITCODE_NAME}.xlsx')

# cmd0 = 'wllvm -O0 -Xclang -optnone -g -fno-discard-value-names -w {0}/test.c'.format(root_path)
raw_part = f' {bc_path} -o {temp_bc_path}'
nander_part = f'wpa -nander {temp_bc_path}'
fspta_part = f'wpa -fspta {temp_bc_path}'
seadsa_part = f'seadsa -sea-dsa=butd-cs -sea-dsa-type-aware --stats -sea-dsa-stats {temp_bc_path}'

rm_gcno = f"rm {os.path.join(ROOT_PATH, '*.gcno')}"
rm_core = f"rm {os.path.join(ROOT_PATH, 'core.*')}"


workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = '#(count)'
sheet['B1'] = 'X'
sheet['C1'] = 'opt time(s)'
sheet['D1'] = 'opt MSS(KB)'
sheet['E1'] = 'nander time(s)'
sheet['F1'] = 'nander MSS(KB)'
sheet['G1'] = 'fspta time(s)'
sheet['H1'] = 'fspta mem(KB)'
sheet['I1'] = 'sea-dsa time(s)'
sheet['J1'] = 'sea-dsa mem(KB)'
sheet['K1'] = 'pass args'

# pass
options = []

# Read pass arguments to iterate on
option_path = os.path.join(ROOT_PATH, ARGS_FILE)

with open(option_path, 'r', encoding='utf-8') as file:
    options = file.readlines()

# delete newline at the end
options = [line.strip() for line in options]

def colored_line(text, color_code = GREEN):
    print(color_code + text + RESET)

def choose_opt_args(bitvec):
    result = []
    for k, s in enumerate(bitvec):
        if s == True:
            result.append(options[k])
    return result

def extract_max_resident_size(file_path):
    """Extracts the 'Maximum resident set size (kbytes)' from the specified file."""
    pattern = r"Maximum resident set size \(kbytes\):\s*(\d+)"
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                return int(match.group(1))
    return None

def process_result(result, time, file_path, time_key, mem_key):
    """Updates the result dictionary with time and memory size from the specified file."""
    result[time_key] = time
    result[mem_key] = extract_max_resident_size(file_path)

def run(x, log_id = None):
    global success_count
    if not log_id:
        log_id = success_count
    # Generate the list of passes to run
    comb = bin(x).replace('0b', '')
    comb = '0' * (len(options) - len(comb)) + comb
    conf = []
    for s in comb:
        if s == '1':
            conf.append(True)
        else:
            conf.append(False)
    conf = choose_opt_args(conf)

    #! opt
    passes = ' '.join(conf)
    opt_cmd = f"/usr/bin/time -v opt {passes} {raw_part} > {os.path.join(opt_path, str(log_id))}.txt 2>&1"
    print(opt_cmd)
    
    # Record args
    with open(os.path.join(opt_path, f'{str(log_id)}-args.txt'), 'w') as file:
        file.write(opt_cmd + '\n')
        file.flush()
    begin_opt = time.time()
    ret_opt = os.system(opt_cmd)
    end_opt = time.time()
    opt_time = end_opt - begin_opt

    if ret_opt != 0:
        colored_line('opt command: FAILED!', RED)
        return

    #! nander
    nander_cmd = f"/usr/bin/time -v {nander_part} > {os.path.join(nander_path, str(log_id))}-stdout.txt " \
                 f"2>{os.path.join(nander_path, str(log_id))}-stderr.txt"

    colored_line(nander_cmd, YELLOW)
    begin_nander = time.time()
    ret_nander = os.system(nander_cmd)
    end_nander = time.time()

    #! fspta
    fspta_cmd = f"/usr/bin/time -v {fspta_part} > {os.path.join(fspta_path, str(log_id))}-stdout.txt " \
                f"2>{os.path.join(fspta_path, str(log_id))}-stderr.txt"
    colored_line(fspta_cmd, BLUE)
    begin_fspta = time.time()
    ret_fspta = os.system(fspta_cmd)
    end_fspta = time.time()
    
    #! sea-dsa
    seadsa_cmd = f"/usr/bin/time -v {seadsa_part} > {os.path.join(seadsa_path, str(log_id))}-stdout.txt " \
                f"2>{os.path.join(seadsa_path, str(log_id))}-stderr.txt"
    colored_line(seadsa_cmd, CYAN)
    begin_seadsa = time.time()
    ret_seadsa = os.system(seadsa_cmd)
    end_seadsa = time.time()

    if ret_nander != 0:
        colored_line('nander command: FAILED!', RED)
    if ret_fspta != 0:
        colored_line('fspta command: FAILED!', RED)
    if ret_seadsa != 0:
        colored_line('seadsa command: FAILED!', RED)
    
    # Remove temp files
    os.system(rm_gcno)
    os.system(rm_core)
    os.system('rm ' + temp_bc_path)

    result = {
        'opt_success_count': success_count,
        'x': str(x),
        'opt_time': opt_time,
        'opt_mem_usage': None,
        'nander_time': None,
        'nander_mem_usage': None,
        'fspta_time': None,
        'fspta_mem_usage': None,
        'passes': passes,
    }

    # Extract memory usage for opt
    opt_file_path = os.path.join(opt_path, f"{log_id}.txt")
    result['opt_mem_usage'] = extract_max_resident_size(opt_file_path)
    

    # Process nander result
    if ret_nander > 0:
        result['nander_time'] = 'error'
        result['nander_mem_usage'] = 'error'
    else:
        nander_time = end_nander - begin_nander
        nander_file_path = f"{os.path.join(nander_path, str(log_id))}-stderr.txt"
        process_result(result, nander_time, nander_file_path, 'nander_time', 'nander_mem_usage')

    # Process fspta result
    if ret_fspta > 0:
        result['fspta_time'] = 'error'
        result['fspta_mem_usage'] = 'error'
    else:
        fspta_time = end_fspta - begin_fspta
        fspta_file_path = f"{os.path.join(fspta_path, str(log_id))}-stderr.txt"
        process_result(result, fspta_time, fspta_file_path, 'fspta_time', 'fspta_mem_usage')
    
    # Process sea-dsa result
    if ret_seadsa > 0:
        result['seadsa_time'] = 'error'
        result['seadsa_mem_usage'] = 'error'
    else:
        seadsa_time = end_seadsa - begin_seadsa
        seadsa_file_path = f"{os.path.join(seadsa_path, str(log_id))}-stderr.txt"
        process_result(result, seadsa_time, seadsa_file_path, 'seadsa_time', 'seadsa_mem_usage')

    # Append result to sheet and save workbook
    sheet.append(list(result.values()))
    print(result)
    workbook.save(xlsx_path)
    
    success_count += 1
    

if __name__ == '__main__':
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(opt_path):
        os.makedirs(opt_path)
    if not os.path.exists(nander_path):
        os.makedirs(nander_path)
    if not os.path.exists(fspta_path):
        os.makedirs(fspta_path)
    if not os.path.exists(seadsa_path):
        os.makedirs(seadsa_path)

    workbook.save(xlsx_path)
    training_indep = set()
    
    for i in tqdm(range(TOTAL_ITER)):
        
        colored_line('#' * 60)
        colored_line(f'Iteration {i + 1}/{TOTAL_ITER}')
        colored_line('#' * 60)
        
        x = random.randint(0, 2 ** len(options))
        if x not in training_indep:
            training_indep.add(x)
            run(x, i)
    colored_line(f'Successed: {success_count}/{TOTAL_ITER}')
