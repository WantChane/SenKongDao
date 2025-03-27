from datetime import datetime
from utils.logger import logger
import utils.path as path

# 路径引入
lock_dir = path.lock_dir

def daily_lock_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            lock_file_name = f"{today}.lock"            
            
            lock_file_path = lock_dir / lock_file_name
            
            if lock_file_path.exists():
                logger.info("今日任务已执行，跳过。")
                return

            # 执行任务
            result = func(*args, **kwargs)

            # 清理旧锁文件
            deleted_files = []
            for file in lock_dir.glob("*.lock"):
                if file.name != lock_file_name:
                    try:
                        file.unlink()
                        deleted_files.append(file.name)
                    except Exception as e:
                        logger.error(f"删除旧锁文件失败：{file.name} - {str(e)}")
            
            if deleted_files:
                logger.info(f"已删除旧锁文件：{', '.join(deleted_files)}")
                
            # 创建锁文件
            try:
                lock_file_path.touch(exist_ok=False)
                logger.info(f"创建今日锁文件：{lock_file_name}")
            except FileExistsError:
                logger.warning("锁文件已存在，跳过执行。")
                return
            except Exception as e:
                logger.error(f"创建锁文件失败：{str(e)}")
                return
                
            return result
            
        except Exception as e:
            logger.critical(f"装饰器发生未预期错误：{str(e)}")
            raise
            
    return wrapper
