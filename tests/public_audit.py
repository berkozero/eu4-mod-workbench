"""Audit only the git index: generated/private local files are never scanned or published."""
import os,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
paths=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
assert any(paths),'No tracked files to audit'
errors=[]
for name in filter(None,paths):
    p=root/name
    if any(part in ['.local','dist','reports','.venv','node_modules'] for part in p.relative_to(root).parts):errors.append((name,'private/generated directory'))
    if p.suffix in ['.sqlite','.eu4','.log','.asm']:errors.append((name,'private/runtime artifact'))
    if p.name in ['SCA_Teutonic_Missions.txt','EMP_Prussian_Missions.txt','Brandenburgian_and_Prussian_Missions.txt']:errors.append((name,'full native game script'))
    if p.is_symlink():
        if not (name=='CLAUDE.md' and os.readlink(p)=='AGENTS.md' and p.resolve()==root/'AGENTS.md' and (root/'AGENTS.md').is_file() and not (root/'AGENTS.md').is_symlink()):
            errors.append((name,'unexpected or nonportable symlink'));continue
    if p.stat().st_size>50_000_000:errors.append((name,'oversized asset'))
    if p.suffix in ['.png','.dds','.ogg','.bmp']:continue
    data=p.read_text(encoding='utf-8-sig')
    patterns=['/'+'Users'+r'/[^/\s]+/',r'(?m)(?:^|[\s"<>])/home/[^/\s]+/',r'data:image/\w+;base64,[A-Za-z0-9+/]{100}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----']
    for pattern in patterns:
        if re.search(pattern,data):errors.append((name,'private path, credential or embedded image'))
assert not errors,errors
print('Public index audit passed:',len(list(filter(None,paths))),'files')
