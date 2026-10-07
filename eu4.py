#!/usr/bin/env python3
"""Small EU4 mod workbench. Run --help for the complete command set."""
import argparse,json,os,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def game_path(value):
    if value:return Path(value).expanduser().resolve()
    if os.environ.get('EU4_GAME_PATH'):return Path(os.environ['EU4_GAME_PATH']).expanduser().resolve()
    config=ROOT/'local.json'
    if config.exists() and json.loads(config.read_text()).get('game'):return Path(json.loads(config.read_text())['game']).expanduser().resolve()
    for p in [Path.home()/'Library/Application Support/Steam/steamapps/common/Europa Universalis IV',Path.home()/'.local/share/Steam/steamapps/common/Europa Universalis IV',Path('C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis IV')]:
        if (p/'missions').is_dir():return p
    raise ValueError('Set EU4_GAME_PATH, --game, or game in gitignored local.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    for command in ['build','check','install']:
        p=sub.add_parser(command);p.add_argument('country');p.add_argument('--game')
        if command=='install':p.add_argument('--user-dir',default=str(Path.home()/'Documents/Paradox Interactive/Europa Universalis IV'))
    p=sub.add_parser('new');p.add_argument('country');p.add_argument('--tag',required=True)
    sub.add_parser('test')
    args=parser.parse_args()
    if args.action=='test':return subprocess.call([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],cwd=ROOT)
    if not re.fullmatch('[a-z][a-z0-9_-]*',args.country):raise ValueError('Country folder must be a simple lowercase slug')
    if args.action=='new':
        from workbench.scaffold import scaffold
        scaffold(ROOT,args.country,args.tag);print('Created mods/'+args.country+'. Edit missions.json and project.json, then build.');return 0
    if args.action=='install' and json.loads((ROOT/'mods'/args.country/'project.json').read_text()).get('draft'):
        raise ValueError('Draft country: review native mission integration and set draft=false before installation')
    from workbench.build import build
    if args.action=='check':
        from workbench.checks import verify
        project=ROOT/'mods'/args.country;manifest=json.loads((project/'project.json').read_text());report,_=verify(project,ROOT/'dist'/args.country/manifest['slug'],game_path(args.game),json.loads((project/'missions.json').read_text()),manifest)
        print(json.dumps(report,indent=2));return 0
    package,report=build(ROOT,args.country,game_path(args.game));print(json.dumps(report,indent=2));print('Preview:',package/'preview.html');print('Drop-in package:',package)
    if args.action=='install':
        from workbench.install import install
        result=install(package,Path(args.user_dir).expanduser().resolve(),ROOT/'.local/install-backups');(package/'installation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print('If this is a new mod, enable it in your chosen launcher playset. Existing mods and playsets are preserved.')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,AssertionError,FileNotFoundError) as error:print('ERROR:',error,file=sys.stderr);sys.exit(1)
