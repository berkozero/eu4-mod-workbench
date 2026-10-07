"""Copy one verified mod. Never write launcher SQLite, playsets or enabled_mods."""
import datetime,hashlib,json,shutil,subprocess
from pathlib import Path
from .checks import require

def install(package,user_dir,backup_dir,check_processes=True):
    if check_processes:
        command=['tasklist'] if __import__('os').name=='nt' else ['ps','-axo','comm']
        processes=subprocess.check_output(command,text=True).lower()
        require(not any(term in processes for term in ['/eu4.app/contents/macos/eu4','/eu4','eu4.exe','paradox launcher.app/contents/macos/paradox launcher','paradox launcher.exe','/dowser']),'Close EU4 and its launcher before installing')
    descriptors=list(package.glob('*.mod'));require(len(descriptors)==1,'Expected one external descriptor')
    slug=descriptors[0].stem;source=package/slug;require(source.is_dir(),'Missing mod folder')
    mods=user_dir/'mod';mods.mkdir(parents=True,exist_ok=True);dest=mods/slug;external=mods/(slug+'.mod')
    # Restrict replacement to this package and reject symlink escapes.
    require(not dest.is_symlink() and not external.is_symlink(),'Refuse symlinked install targets')
    preserve={p:p.read_bytes() for name in ['dlc_load.json','launcher-v2.sqlite'] if (p:=user_dir/name).exists()}
    backup=backup_dir/(slug+'-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'));backup.mkdir(parents=True)
    stage=mods/(slug+'.workbench-staging');require(not stage.exists(),'Remove or inspect the previous staging folder first')
    shutil.copytree(source,stage)
    def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
    expected=hashes(source);require(hashes(stage)==expected,'Staged copy differs from build')
    replaced=False;had_external=external.exists()
    try:
        if dest.exists():dest.rename(backup/slug)
        if external.exists():shutil.copy2(external,backup/external.name)
        stage.rename(dest);replaced=True
        external.write_text((dest/'descriptor.mod').read_text()+f'path="{dest.as_posix()}"\n')
        require(hashes(dest)==expected,'Installed copy differs from build')
        for p,data in preserve.items():require(p.read_bytes()==data,('Launcher state unexpectedly changed',p.name))
    except Exception:
        if replaced and dest.exists():shutil.rmtree(dest)
        if (backup/slug).exists():(backup/slug).rename(dest)
        if (backup/external.name).exists():shutil.copy2(backup/external.name,external)
        elif not had_external and external.exists():external.unlink()
        raise
    return dict(installed_path=str(dest),files_verified=len(expected),launcher_configuration_untouched=True,backup=str(backup),game_launched=False)
