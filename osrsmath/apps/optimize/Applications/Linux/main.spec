# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['../../main.py'],
             pathex=['/mnt/c/Users/nawar/Documents/GitHub/OSRSmath/osrsmath/apps/optimize/Applications/Linux'],
             binaries=[],
             datas=[('/mnt/c/Users/nawar/Documents/GitHub/OSRSmath/osrsmath/model/data', 'DATA/model/data'), ('/mnt/c/Users/nawar/Documents/GitHub/OSRSmath/osrsmath/apps/GUI/shared/stylesheets', 'DATA/apps/GUI/shared/stylesheets'), ('/mnt/c/Users/nawar/Documents/GitHub/OSRSmath/osrsmath/apps/optimize/data', 'DATA/apps/optimize/data')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
