# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\..\\main.py'],
             pathex=['C:\\Users\\nawar\\Documents\\GitHub\\OSRSmath\\osrsmath\\apps\\optimize\\Applications\\Windows'],
             binaries=[],
             datas=[('c:\\\\users\\\\nawar\\\\documents\\\\github\\\\osrsmath\\\\osrsmath\\\\model\\\\data', 'DATA\\\\model\\\\data'), ('c:\\\\users\\\\nawar\\\\documents\\\\github\\\\osrsmath\\\\osrsmath\\\\apps\\\\GUI\\\\shared\\\\stylesheets', 'DATA\\\\apps\\\\GUI\\\\shared\\\\stylesheets'), ('c:\\\\users\\\\nawar\\\\documents\\\\github\\\\osrsmath\\\\osrsmath\\\\apps\\\\optimize\\\\data', 'DATA\\\\apps\\\\optimize\\\\data')],
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
