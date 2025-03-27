import sys
from loguru import logger
import utils.path as path

# 路径引入
log_file = path.log_path

# 移除默认配置
logger.remove()

# 添加控制台输出
# logger.add(
#     sys.stderr,
#     format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}:{line}</cyan> - <level>{message}</level>",
#     level="INFO"
# )

# 添加文件日志配置
logger.add(
    log_file,
    rotation="00:00",  # 每天午夜轮换
    retention="7 days",  # 保留7天
    enqueue=True,  # 线程安全
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{line} - {message}",
    level="INFO"
)

__all__ = ["logger"]
