"""Engine-informed structural checks. This is not an EU4 emulator."""
import itertools,json,re
from pathlib import Path
from .script import parse,first,descend

class ValidationError(ValueError):pass

def require(ok,message):
    if not ok:raise ValidationError(str(message))

def series_nodes(ast):
    out=[]
    for series,col in ast:
        if not isinstance(col,list):continue
        slot=int(first(col,'slot','0'));row=0;nodes=[]
        for id,n in col:
            if isinstance(n,list) and first(n,'icon'):
                row=int(first(n,'position',str(row+1)))
                nodes.append(dict(id=id,lane=slot-1,position=row,parents=[p for p,_ in first(n,'required_missions',[])],script=n,series=series))
        if nodes:out.append(dict(id=series,slot=slot,nodes=nodes,potential=first(col,'potential',[])))
    return out

def evaluate(ast,state):
    """Assignment fixture evaluator; refuse unsupported conditions instead of guessing."""
    def one(k,v):
        if k=='OR':return any(one(a,b) for a,b in v)
        if k=='AND':return all(one(a,b) for a,b in v)
        if k=='NOT':return not all(one(a,b) for a,b in v)
        if k=='always':return v=='yes'
        if k=='tag':return state.get('tag')==v
        if k=='was_tag':return v in state.get('was',[])
        if k=='has_country_flag':return v in state.get('flags',[])
        if k=='has_dlc':return state.get('dlc',True)
        if k=='map_setup':return state.get('random',False)
        if k=='has_mission':return v in state.get('missions',[])
        raise ValidationError('Fixture evaluator does not support '+k)
    return all(one(k,v) for k,v in ast)

def assignment(series,state):
    spans={};nodes={};cells={}
    for s in series:
        if not evaluate(s['potential'],state):continue
        lo=min(n['position'] for n in s['nodes']);hi=max(n['position'] for n in s['nodes'])
        for name,a,b in spans.get(s['slot'],[]):require(hi<a or lo>b,('Overlapping mission series',s['id'],name,(lo,hi),(a,b)))
        spans.setdefault(s['slot'],[]).append((s['id'],lo,hi))
        for n in s['nodes']:
            cell=(n['lane'],n['position']);require(cell not in cells,('Duplicate cell',n['id'],cells.get(cell)))
            require(n['id'] not in nodes,('Duplicate mission',n['id']));cells[cell]=n['id'];nodes[n['id']]=n
    return nodes

def arrow_errors(nodes):
    errors=[]
    for id,n in nodes.items():
        require(0<=n['lane']<5 and n['position']>0,('Invalid coordinates',id))
        for p in n['parents']:
            if p not in nodes:errors.append((p,id,'missing parent'));continue
            parent=nodes[p];dy=n['position']-parent['position']
            if dy<=0:errors.append((p,id,'parent must be above child'))
            elif n['lane']!=parent['lane'] and dy!=1:errors.append((p,id,'cross-column arrow skips rows'))
            elif n['lane']==parent['lane']:
                blockers=[k for k,v in nodes.items() if v['lane']==n['lane'] and parent['position']<v['position']<n['position']]
                if blockers:errors.append((p,id,'vertical arrow crosses '+', '.join(blockers)))
    return errors

def acyclic(graph):
    done=set()
    def visit(k,stack=()):
        require(k not in stack,('Mission dependency cycle',stack+(k,)))
        if k in done:return
        for p in graph[k]:require(p in graph,('Unknown mission',p));visit(p,stack+(k,))
        done.add(k)
    for k in graph:visit(k)

def loading_check(descriptor,names):
    require(not re.search(r'replace_path\s*=\s*"gfx/loadingscreens/?"',descriptor),'Do not replace the native loading-screen directory')
    require(len(set(names))>1,'Loading selector needs at least two effective DDS entries')

def load_order_check(mode):require(mode in ['custom','alphabetical','reverse-alphabetical'],('Unsupported launcher load order',mode))

def verify(project,mod,game,specs,manifest):
    series=[]
    for path in (mod/'missions').glob('*.txt'):
        if manifest.get('primary_mission_file') and path.name!=manifest['primary_mission_file']:continue
        series+=series_nodes(parse(path.read_text(encoding='utf-8-sig')))
    state=dict(tag=manifest['tag']);nodes=assignment(series,state)
    aliases=dict(manifest.get('baseline_ids',{}));aliases.update({m['id']:m['scriptId'] for m in specs})
    require(set(nodes)==set(aliases.values()),'Opening assignment differs from the intended mission set')
    require(not arrow_errors(nodes),arrow_errors(nodes))
    # Path fixtures, kept project data rather than country assumptions in the checker.
    fixture_counts={}
    for label,fixture in manifest.get('fixtures',{}).items():
        found=assignment(series,fixture['state']);fixture_counts[label]=len(found)
        require(len(found)==fixture['count'],('Unexpected assignment',label,len(found)))
        if 'same_as_game' in fixture:
            native=series_nodes(parse((game/'missions'/fixture['same_as_game']).read_text(encoding='utf-8-sig')))
            require(set(found)==set(assignment(native,fixture['state'])),('Changed original assignment',label))
    spec_by={m['scriptId']:m for m in specs};logical={};cases=0
    for id,n in nodes.items():
        top=first(n['script'],'trigger',[]);remote={v for k,v in top if k=='mission_completed'}
        actual=set(n['parents'])|remote
        if id in spec_by:
            m=spec_by[id];wanted={aliases[p] for p in m['parents']}
            require(actual==wanted,('Lost or added logical prerequisite',id,wanted,actual))
            require(not set(n['parents'])&remote,('Repeated prerequisite',id))
            for bits in itertools.product([False,True],repeat=len(wanted)):
                completed={p for p,b in zip(sorted(wanted),bits) if b}
                require((wanted<=completed)==(set(n['parents'])<=completed and remote<=completed),('Gate equivalence',id));cases+=1
            gate=parse('has_country_flag = '+manifest['path_flag']) if manifest.get('path_flag') else []
            prefix=gate+(parse('not_in_mission_preview_mode = { key = '+manifest['tag']+' }') if manifest.get('path_flag') else [])
            checks=[('mission_completed',aliases[p]) for p in m['checklistParents']]
            require(top==prefix+checks+parse(m['trigger']),('World condition changed',id))
            require(first(n['script'],'effect')==parse(m['effect']),('Reward changed',id))
        logical[id]=set(n['parents'])|{v for k,v in descend(top) if k=='mission_completed'}
        for p in logical[id]:require(p in nodes and nodes[p]['position']<n['position'],('Prerequisite below or absent',p,id))
    acyclic(logical)
    # Compare baseline directly against the user's installed game, including coordinates.
    baseline={}
    for file in manifest.get('base_mission_files',[]):
        for s in series_nodes(parse((game/'missions'/file).read_text(encoding='utf-8-sig'))):
            baseline.update({n['id']:n for n in s['nodes']})
    for id in manifest.get('baseline_ids',{}).values():
        before=baseline[id];after=nodes[id]
        require((before['lane'],before['position'],before['parents'])==(after['lane'],after['position'],after['parents']),('Changed original layout',id))
        for field in ['icon','effect']:require(first(before['script'],field)==first(after['script'],field),('Changed original field',id,field))
        trigger=first(before['script'],'trigger',[])
        if id in manifest.get('gated_baseline_ids',[]):trigger=[('has_country_flag',manifest['path_flag'])]+trigger
        require(trigger==first(after['script'],'trigger',[]),('Changed original trigger',id))
    # Parse all shipped scripts; verify custom events, modifier/area/building references.
    asts=[(p,parse(p.read_text(encoding='utf-8-sig'))) for p in list(mod.rglob('*.txt'))+list(mod.rglob('*.gfx')) if p.name!='MUSIC-CREDITS.txt']
    events={first(v,'id'):v for p,a in asts if p.parent.name=='events' for k,v in a if k=='country_event'}
    loc={}
    for p in (mod/'localisation').glob('*_l_english.yml'):
        require(p.read_bytes().startswith(b'\xef\xbb\xbf'),('Localization needs UTF-8 BOM',p.name))
        text=p.read_text(encoding='utf-8-sig');text.encode('cp1252')
        loc.update(dict(re.findall(r'^\s*([^:]+):\d*\s+"(.*)"',text,re.M)))
    for id in spec_by:require(id+'_title' in loc and id+'_desc' in loc,('Missing localization',id))
    areas=dict(parse((game/'map/area.txt').read_text()));regions=dict(parse((game/'map/region.txt').read_text()))
    supers=dict(parse((game/'map/superregion.txt').read_text()));mods=set();buildings=set()
    for root in [game,mod]:
        for p in (root/'common/event_modifiers').glob('*.txt'):mods.update(k for k,v in parse(p.read_text(encoding='utf-8-sig',errors='replace')))
        for p in (root/'common/buildings').glob('*.txt'):buildings.update(k for k,v in parse(p.read_text(encoding='utf-8-sig',errors='replace')))
    custom=[(id,nodes[id]['script']) for id in spec_by]
    custom += [(str(p),a) for p,a in asts if p.parent.name in ['events','decisions']]
    for name,ast in custom:
        for k,v in descend(ast):
            if k in ['area','region','superregion']:require(v in {'area':areas,'region':regions,'superregion':supers}[k],(name,'Unknown map scope',v))
            if k=='has_building':require(v in buildings,(name,'Unknown building',v))
            if k in ['add_country_modifier','add_province_modifier']:require(first(v,'name') in mods,(name,'Unknown modifier',first(v,'name')))
            if k=='country_event' and isinstance(v,list):require(first(v,'id') in events,(name,'Unknown custom event',first(v,'id')))
    for id,m in specs_by_id(specs).items():
        for target in m.get('claims',[]):require(target in areas or target in regions,('Unknown claim',target))
        for k,v in descend(parse(m['trigger'])):
            if k in ['num_of_owned_provinces_with','num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with']:
                region=first(v,'region');area=first(v,'area');amount=int(first(v,'value'))
                if region:require(amount<=sum(sum(p.isdigit() for p,_ in areas[a]) for a,_ in first(regions[region],'areas',[])),('Impossible regional count',id))
                if area:require(amount<=sum(p.isdigit() for p,_ in areas[area]),('Impossible area count',id))
    def ancestors(id):
        out=set(logical[id])
        for p in logical[id]:out|=ancestors(p)
        return out
    for parent,child in manifest.get('claim_routes',[]):
        require(aliases[parent] in ancestors(aliases[child]),('Claim supplied after objective',parent,child))
        require(specs_by_id(specs)[parent]['claims'],('Claim provider has no claims',parent))
    for eid,event in events.items():
        options=[v for k,v in event if k=='option'];require(any(not first(o,'trigger') for o in options),('No fallback event option',eid))
        for option in options:
            for k,v in option:
                if k=='add_treasury' and float(v)<0:require(float(first(first(option,'trigger',[]),'treasury','0'))>=-float(v),('Unguarded paid choice',eid))
    loading_check((mod/'descriptor.mod').read_text(),{p.name for root in [game,mod] for p in (root/'gfx/loadingscreens').glob('*.dds')})
    return dict(missions=len(nodes),native_arrows=sum(len(n['parents']) for n in nodes.values()),checklist_prerequisites=sum(len(m['checklistParents']) for m in specs),prerequisite_cases=cases,series_overlaps=0,arrow_errors=0,cycles=0,original_missions_preserved=len(manifest.get('baseline_ids',{})),claim_routes=len(manifest.get('claim_routes',[])),assignment_fixtures=fixture_counts,game_launched=False),nodes

def specs_by_id(specs):return {m['id']:m for m in specs}
