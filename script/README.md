## Usage

Make your bitcode file `your_name.bc` prepared in `your_test_dir/your_name/`.

1. `tmux new` or `screen ...`
2. `cd your_test_dir`
3. `python sea-dsa-benchmark.py --bc your_name`
4. Press `Ctrl+b`, then press `d`, then drink your coffee.

## Usage(legacy)

1. 安装 screen、time 和 file
2. 将 opt14.txt 和 wpa-pro.py 放到某个空目录下，比如叫 test
3. 以 bash.bc 为例：使用 bc 文件不含扩展名的部分（bash）在 test 目录下创建一个目录 bash ，并将 bash.bc 放到 test/bash 目录中 
4. 将 wpa-pro.py 中 `bin_name` 的值修改为 `bash`，将 `root_path` 的值修改为 test 目录的绝对路径
5. 使用 conda 或者 pip 安装 openpyxl 这个库
6. 运行 wpa-pro.py 这个脚本（建议使用 screen 创建后台会话）