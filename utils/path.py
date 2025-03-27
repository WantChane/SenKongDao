import sys
from pathlib import Path

# 获取主脚本的绝对路径并解析符号链接
_main_script_path = Path(sys.argv[0]).resolve()
# 主脚本所在目录
MAIN_DIR = _main_script_path.parent

# cookie路径
cookie_path = MAIN_DIR / "SenKongDao_config.txt"

# 日志目录
log_dir = MAIN_DIR / "logs"
# 日志路径
log_path = log_dir / "SenKongDao.log"

# 锁路径
lock_dir = MAIN_DIR
