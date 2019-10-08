# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import (
    Analysis,
    PYZ,
    EXE,
    COLLECT
)
import os
import re
from typing import (
    List,
    Iterable
)


def project_path() -> str:
    return os.path.realpath(f"./{SPEC}/../../")


def enumerate_modules(path: str) -> Iterable[str]:
    source_re = re.compile(r"\.(py|pyx)$")
    actual_path: str = os.path.realpath(path)
    prefix_length: int = len(actual_path.split(os.sep)) - 1

    for dirpath, dirnames, filenames in os.walk(actual_path):
        pkg_components: List[str] = dirpath.split(os.sep)[prefix_length:]
        for filename in filenames:
            if filename == "__init__.py":
                yield ".".join(pkg_components)
            elif source_re.search(filename):
                module_name: str = source_re.sub("", filename)
                yield ".".join(pkg_components) + f".{module_name}"


if "SPEC" in globals():
    block_cipher = None

    hidden_imports: List[str] = list(enumerate_modules(os.path.join(project_path(), "hummingbot")))
    hidden_imports.extend([
        "aiokafka"
    ])

    import _strptime

    a = Analysis(['../bin/bot'],
                 pathex=['/Users/martin_kou/Development/hummingbot'],
                 binaries=[],
                 datas=[(_strptime.__file__, ".")],
                 hiddenimports=hidden_imports,
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)

    pyz = PYZ(a.pure, a.zipped_data,
              cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              [],
              exclude_binaries=True,
              name='bot',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=True)
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   upx_exclude=[],
                   name='bot')
