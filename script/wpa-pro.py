import os
import time
import random
import openpyxl


iters = 60  # 完全成功个数
num = 0  # 完全成功个数的计数器
count = 0  # opt成功个数的计数器（wpa可能失败）
random.seed(15)

sep = os.path.sep
root_path = '/root/test'
bin_name = 'bash'

work_path = root_path + sep + bin_name
bc_path = work_path + sep + '{0}.bc'.format(bin_name)
temp_bc_path = work_path + sep + 'temp.bc'
opt_path = work_path + sep + 'opt'
nander_path = work_path + sep + 'nander'
fspta_path = work_path + sep + 'fspta'
xlsx_path = work_path + sep + '{0}.xlsx'.format(bin_name)

# cmd0 = 'wllvm -O0 -Xclang -optnone -g -fno-discard-value-names -w {0}/test.c'.format(root_path)
cmd0_2 = ' {0} -o {1}'.format(bc_path, temp_bc_path)
cmd1_2 = 'wpa -nander ' + temp_bc_path
cmd2_2 = 'wpa -fspta ' + temp_bc_path
cmd3 = 'rm ' + root_path + sep + '*.gcno'
cmd4 = 'rm ' + root_path + sep + 'core.*'


workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = '序号（count）'
sheet['B1'] = 'X'
sheet['C1'] = 'opt时间(s)'
sheet['D1'] = 'opt内存(KB)'
sheet['E1'] = 'nander时间(s)'
sheet['F1'] = 'nander内存(KB)'
sheet['G1'] = 'fspta时间(s)'
sheet['H1'] = 'fspta内存(KB)'
sheet['I1'] = 'pass'


# pass
options = []

# 打开文件并读取内容
option_path = root_path + sep + 'opt14.txt'

# 使用 with 语句可以确保文件在读取完毕后自动关闭
with open(option_path, 'r', encoding='utf-8') as file:
    # 读取所有行并存储到列表中
    options = file.readlines()

# 去除每行末尾的换行符（如果需要）
options = [line.strip() for line in options]


def generate_opts(independent):
    result = []
    for k, s in enumerate(independent):
        if s == True:
            result.append(options[k])
    return result


def run(x):
    global num, count

    # 生成 pass 列表
    comb = bin(x).replace('0b', '')
    comb = '0' * (len(options) - len(comb)) + comb
    conf = []
    for s in comb:
        if s == '1':
            conf.append(True)
        else:
            conf.append(False)
    conf = generate_opts(conf)

    print("\033[32m" + '#' * 60 + "\033[39m")
    print("\033[32m" + '#' * 60 + "\033[39m")
    print("\033[32m" + '#' * 60 + "\033[39m")
    count = count + 1

    # opt
    passes = ' '.join(conf)
    cmd0 = '/usr/bin/time -v opt ' + passes + \
        cmd0_2 + ' > {0}.txt 2>&1'.format(opt_path + sep + str(count))
    print(cmd0)
    begin_opt = time.time()
    ret_nander = os.system(cmd0)
    end_opt = time.time()
    if ret_nander > 0:
        count = count - 1
        return

    num = num + 1

    # nander
    cmd1 = '/usr/bin/time -v ' + cmd1_2 + \
        ' > {0}{1}{2}-1.txt'.format(nander_path, sep, str(count)) + \
        ' 2>{0}{1}{2}-2.txt'.format(nander_path, sep, str(count))
    print("\033[33m" + cmd1 + "\033[39m")
    begin_nander = time.time()
    ret_nander = os.system(cmd1)
    end_nander = time.time()

    # fspta
    cmd2 = '/usr/bin/time -v ' + cmd2_2 + \
        ' > {0}{1}{2}-1.txt'.format(fspta_path, sep, str(count)) + \
        ' 2>{0}{1}{2}-2.txt'.format(fspta_path, sep, str(count))
    print("\033[34m" + cmd2 + "\033[39m")
    begin_fspta = time.time()
    ret_fspta = os.system(cmd2)
    end_fspta = time.time()

    # 删除临时文件
    os.system(cmd3)
    os.system(cmd4)
    os.system('rm ' + temp_bc_path)

    opt_time = end_opt - begin_opt

    result = [count, str(x), opt_time, None, None, None, None, None, passes]

    # 打开文件并读取内容
    with open('{0}{1}{2}.txt'.format(opt_path, sep, str(count)), 'r') as file:
        lines = file.readlines()
    # 初始化一个变量来存储找到的数字
    # 遍历文件的每一行
    for line in lines:
        # 检查行是否包含特定的字符串
        if 'Maximum resident set size (kbytes):' in line:
            # 分割字符串并提取数字部分
            parts = line.split(':')
            if len(parts) > 1:
                # 去掉数字前后的空格并转换为整数
                result[3] = int(parts[1].strip())

    if (ret_nander > 0) or (ret_fspta > 0):
        num = num - 1

    if ret_nander > 0:
        result[4] = 'error'
        result[5] = 'error'
    else:
        nander_time = end_nander - begin_nander
        result[4] = nander_time
        # 打开文件并读取内容
        with open('{0}{1}{2}-2.txt'.format(nander_path, sep, str(count)), 'r') as file:
            lines = file.readlines()
        # 初始化一个变量来存储找到的数字
        # 遍历文件的每一行
        for line in lines:
            # 检查行是否包含特定的字符串
            if 'Maximum resident set size (kbytes):' in line:
                # 分割字符串并提取数字部分
                parts = line.split(':')
                if len(parts) > 1:
                    # 去掉数字前后的空格并转换为整数
                    result[5] = int(parts[1].strip())

    if ret_fspta > 0:
        result[6] = 'error'
        result[7] = 'error'
    else:
        fspta_time = end_fspta - begin_fspta
        result[6] = fspta_time
        # 打开文件并读取内容
        with open('{0}{1}{2}-2.txt'.format(fspta_path, sep, str(count)), 'r') as file:
            lines = file.readlines()
        # 初始化一个变量来存储找到的数字
        # 遍历文件的每一行
        for line in lines:
            # 检查行是否包含特定的字符串
            if 'Maximum resident set size (kbytes):' in line:
                # 分割字符串并提取数字部分
                parts = line.split(':')
                if len(parts) > 1:
                    # 去掉数字前后的空格并转换为整数
                    result[7] = int(parts[1].strip())

    sheet.append(result)
    workbook.save(xlsx_path)

    return


def main():
    training_indep = set()
    while num < iters:
        x = random.randint(0, 2 ** len(options))
        if x not in training_indep:
            training_indep.add(x)
            run(x)
    return


if __name__ == '__main__':

    if not os.path.exists(opt_path):
        os.makedirs(opt_path)
    if not os.path.exists(nander_path):
        os.makedirs(nander_path)
    if not os.path.exists(fspta_path):
        os.makedirs(fspta_path)

    main()


