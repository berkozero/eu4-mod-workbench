"""Build a country package from custom content and the user's own EU4 installation."""
import copy,hashlib,importlib.util,json,shutil
from pathlib import Path
from .script import parse,first,dump
from .checks import require,verify

def build(root,country,game):
    project=root/'mods'/country
    manifest=json.loads((project/'project.json').read_text());specs=json.loads((project/'missions.json').read_text())
    require(game.is_dir() and (game/'missions').is_dir(),'Set EU4_GAME_PATH or --game to your EU4 installation')
    for filename,sha in manifest.get('base_sha256',{}).items():
        require(hashlib.sha256((game/'missions'/filename).read_bytes()).hexdigest()==sha,('Base-game mission file changed; review compatibility first',filename))
    out=root/'dist'/country;stage=root/'dist'/(country+'.building')
    if stage.exists():shutil.rmtree(stage)
    mod=stage/manifest['slug'];shutil.copytree(project/'content',mod)
    aliases=dict(manifest.get('baseline_ids',{}));aliases.update({m['id']:m['scriptId'] for m in specs})
    files={name:parse((game/'missions'/name).read_text(encoding='utf-8-sig')) for name in manifest.get('base_mission_files',[])}
    hook=project/'patch.py'
    if hook.exists():
        module_spec=importlib.util.spec_from_file_location('country_patch',hook);module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module);module.apply(files,manifest)
    primary=manifest.get('primary_mission_file','workbench_missions.txt');ast=files.setdefault(primary,[])
    for name,definition in manifest.get('series',{}).items():ast.append((name,parse(definition)))
    mapping=manifest.get('native_series_by_slot',{})
    for m in specs:
        require(set(m['arrowParents']).isdisjoint(m['checklistParents']),(m['id'],'Repeated logical parent'))
        require(set(m['arrowParents'])|set(m['checklistParents'])==set(m['parents']),(m['id'],'Every prerequisite must have an explicit representation'))
        series=m.get('series') or mapping[str(m['lane']+1)];col=first(ast,series)
        require(col is not None,(m['id'],'Missing target series',series));require(int(first(col,'slot'))==m['lane']+1,(m['id'],'Wrong column for target series'))
        path_gate='has_country_flag = '+manifest['path_flag']+' not_in_mission_preview_mode = { key = '+manifest['tag']+' } ' if manifest.get('path_flag') else ''
        checklist=' '.join('mission_completed = '+aliases[p] for p in m['checklistParents'])
        node=parse('icon = '+m['icon']+' position = '+str(m['position'])+' required_missions = { '+' '.join(aliases[p] for p in m['arrowParents'])+' } provinces_to_highlight = { } trigger = { '+path_gate+checklist+' '+m['trigger']+' } effect = { '+m['effect']+' }')
        col.append((m['scriptId'],node))
    for name,columns in files.items():
        for _,col in columns:
            if not isinstance(col,list):continue
            missions=[(k,v) for k,v in col if isinstance(v,list) and first(v,'icon')]
            if missions and all(first(v,'position') is not None for _,v in missions):
                metadata=[(k,v) for k,v in col if not (isinstance(v,list) and first(v,'icon'))];col[:]=metadata+sorted(missions,key=lambda pair:int(first(pair[1],'position')))
        target=mod/'missions'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(dump(columns)+'\n')
    # Keep custom mission titles/descriptions in sync with their editable specifications.
    locdir=mod/'localisation';locdir.mkdir(exist_ok=True)
    def quote(s):return s.replace('−','-').replace('\\','\\\\').replace('"',"'").replace('\n','\\n')
    loc=['l_english:']
    # Replace current custom keys in the source localization, avoiding duplicate-key ambiguity.
    keys={m['scriptId']+suffix for m in specs for suffix in ['_title','_desc']}
    import re
    for p in locdir.glob('*_l_english.yml'):
        lines=p.read_text(encoding='utf-8-sig').splitlines();p.write_text('\n'.join(line for line in lines if not (match:=re.match(r'\s*([^:]+):',line)) or match[1] not in keys)+'\n',encoding='utf-8-sig')
    for m in specs:
        source=m.get('source',{});desc='Historical root: '+source.get('root','')+' Fictional continuation: '+m.get('why','')+' Source: '+source.get('url','')
        loc.extend([' '+m['scriptId']+'_title:0 "'+quote(m['title'])+'"',' '+m['scriptId']+'_desc:0 "'+quote(desc)+'"'])
    (locdir/(manifest['namespace']+'_missions_l_english.yml')).write_text('\n'.join(loc)+'\n',encoding='utf-8-sig')
    if manifest.get('loading_rotation'):
        target=mod/'gfx/loadingscreens';target.mkdir(parents=True,exist_ok=True)
        names={p.name for p in (game/'gfx/loadingscreens').glob('*.dds')}|{'load_37.dds'}
        for name in names:shutil.copy2(project/'assets/loading.dds',target/name)
        shutil.copy2(project/'assets/init.bmp',target/'init.bmp')
    report,nodes=verify(project,mod,game,specs,manifest)
    report['draft']=manifest.get('draft',False)
    from .preview import render
    render(project,mod,game,manifest,specs,nodes,stage/'preview.html')
    (stage/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (stage/(manifest['slug']+'.mod')).write_text((mod/'descriptor.mod').read_text()+f'path="mod/{manifest["slug"]}"\n')
    # Publish a build only after checks and preview generation succeed.
    if out.exists():shutil.rmtree(out)
    stage.rename(out)
    return out,report
