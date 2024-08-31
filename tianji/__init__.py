from pathlib import Path
from loguru import logger
import tianji


def get_tianji_package_path():
    """Get the root directory of the installed package."""
    package_root = Path(tianji.__file__).parent.parent
    for i in (".git", ".gitignore"):
        if (package_root / i).exists():
            break
    else:
        package_root = Path.cwd()

    if (
        not (package_root / ".gitignore").exists()
        or not (package_root / "tianji").exists()
        or not (package_root / "run").exists()
    ):
        raise FileNotFoundError(
            "当前目录缺少 .gitignore 文件或 tianji 目录，可能不是根目录，请重新 `pip install -e .` 安装!"
        )
    logger.info(f"初始化完毕,当前执行根目录为 {str(package_root)}")
    return package_root


TIANJI_PATH = get_tianji_package_path()
