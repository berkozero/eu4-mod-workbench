"""Rehydrate the existing HTML planner using actual compiled scripts and local game art."""
import base64,copy,html,io,json,re
from pathlib import Path
import markdown2
from PIL import Image
from .script import first,parse,dump
from .checks import require,arrow_errors

def png(im):
    data=io.BytesIO();im.convert('RGBA').save(data,format='PNG');return 'data:image/png;base64,'+base64.b64encode(data.getvalue()).decode()

def render(project,mod,game,manifest,specs,nodes,target):
    require(not arrow_errors(nodes),'Cannot render a graph the engine cannot draw')
    meta=json.loads((project/'preview-content.json').read_text()) if (project/'preview-content.json').exists() else {}
    baseline=[m for m in meta.get('missions',[]) if m['scriptId'] in manifest.get('baseline_ids',{}).values()]
    native_to_id={m['scriptId']:m['id'] for m in baseline+specs};sprites={}
    for root in [game,mod]:
        for file in (root/'interface').glob('*.gfx'):
            for block in re.findall(r'spriteType\s*=\s*\{([^{}]*)\}',file.read_text(encoding='utf-8-sig',errors='replace'),re.S):
                name=re.search(r'name\s*=\s*"([^"]+)"',block);texture=re.search(r'texturefile\s*=\s*"([^"]+)"',block,re.I)
                if name and texture:
                    rel=texture[1].replace('//','/');sprites[name[1]]=(mod/rel if (mod/rel).exists() else game/rel)
    metrics={}
    for line in (game/'gfx/fonts/vic_18.fnt').read_text().splitlines():
        if line.startswith('char '):
            values={k:int(v) for k,v in re.findall(r'(\w+)=\s*(-?\d+)',line)};metrics[values['id']]=values
    atlas=Image.open(game/'gfx/fonts/vic_18.tga').convert('RGBA')
    def caption(title):
        width=lambda t:sum(metrics.get(ord(c),metrics[32])['xadvance'] for c in t)
        lines=[];line=''
        for word in title.split():
            if line and width(line+' '+word)>90:lines.append(line);line=word
            else:line=(line+' '+word).strip()
        if line:lines.append(line)
        canvas=Image.new('RGBA',(90,max(36,len(lines)*18)))
        for row,line in enumerate(lines):
            x=(90-width(line))//2
            for c in line:
                g=metrics.get(ord(c),metrics[32]);canvas.alpha_composite(atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height'])),(x+g['xoffset'],row*18+g['yoffset']));x+=g['xadvance']
        if canvas.height>36:canvas=canvas.resize((90,36),Image.Resampling.LANCZOS)
        return png(canvas),lines
    md=lambda text:str(markdown2.markdown(text,extras=['tables']))
    allnames={m['id']:m['title'] for m in baseline+specs};missions=[]
    for m in baseline+specs:
        n=nodes[m['scriptId']];is_new=m in specs
        if is_new:
            rewards='<ul>'+''.join('<li>'+md(e['text'])+'</li>' for e in m['rewards'])+'</ul>'
            for eid in m.get('eventIds',[]):
                event=meta['events'][eid];rewards+='<h3>'+html.escape(event['title'])+'</h3>'+md(event['description'])+'<p>Choose one outcome.</p>'
                for option in event['options']:
                    rewards+='<div class="rewardChoice"><strong>'+html.escape(option['label'])+'</strong>'+''.join(md(c['text']) for c in option['conditions'])+'<ul>'+''.join('<li>'+md(e['text'])+'</li>' for e in option['outcomes'])+'</ul></div>'
                rewards+='<button class="eventButton" data-event="'+eid+'">Inspect / try this event in the planner</button>'
            item=dict(m,titleShort=m['title'],isNew=True,story=bool(m.get('eventIds')),conditionsHTML=md(m['conditions']),rewardsHTML=rewards,conditions=[dict(text=m['conditions'],children=[])],outcomes=[dict(text=e['text'],children=[]) for e in m['rewards']],source_link=dict(url=m.get('source',{}).get('url',''),label='Historical foundation'),historical_root=dict(text=m.get('source',{}).get('root','')),counterfactual_rationale=m.get('why',''),progress=m.get('why',''),review=[m.get('why','')],progression=dict(preparation='Complete '+', '.join(m['parents']),achievement=m['conditions'],payoff=m.get('rewardText',''),review=m.get('why',''),revised=False),main_route=False,claim_reward=bool(m.get('claims')))
        else:item=copy.deepcopy(m)
        item.update(lane=n['lane'],position=n['position'],triggerAST=first(n['script'],'trigger',[]),effectAST=first(n['script'],'effect',[]),nativeTrigger=dump(first(n['script'],'trigger',[])),nativeEffect=dump(first(n['script'],'effect',[])),arrowParents=[native_to_id[p] for p in n['parents']])
        item['checklistParents']=[p for p in item['parents'] if p not in item['arrowParents']]
        # Imported prose is kept, but do not duplicate old dynamic requirement headers.
        item['conditionsHTML']=re.sub(r'<p><strong>(?:Earlier milestones:|Path requirement:).*?</p>','',item['conditionsHTML'],flags=re.S)
        if item['checklistParents']:item['conditionsHTML']='<p><strong>Earlier milestones:</strong> '+', '.join(html.escape(allnames[p]) for p in item['checklistParents'])+'. These remain required.</p>'+item['conditionsHTML']
        if ('has_country_flag',manifest.get('path_flag')) in item['triggerAST']:item['conditionsHTML']='<p><strong>Path requirement:</strong> Complete the campaign path choice before claiming this mission.</p>'+item['conditionsHTML']
        icon=first(n['script'],'icon');require(icon in sprites and sprites[icon].is_file(),('Missing portrait',icon));item['image']=png(Image.open(sprites[icon]));item['caption'],item['captionLines']=caption(item['title']);missions.append(item)
    for m in missions:m['children']=[n['id'] for n in missions if m['id'] in n['parents']];m['decisions']=[d['id'] for d in meta.get('decisions',[]) if m['id'] in d.get('missions',[])]
    # Read decisions/events from built scripts so requirements cannot silently diverge.
    decisions=[];native_decisions={}
    for p in (mod/'decisions').glob('*.txt'):native_decisions.update(dict(first(parse(p.read_text(encoding='utf-8-sig')),'country_decisions',[])))
    for d in meta.get('decisions',[]):
        d=copy.deepcopy(d);n=native_decisions[d['id']];d.update(potentialAST=first(n,'potential',[]),triggerAST=first(n,'allow',[]),effectAST=first(n,'effect',[]),nativeTrigger=dump(first(n,'potential',[])+first(n,'allow',[])),nativeEffect=dump(first(n,'effect',[])));decisions.append(d)
    events=copy.deepcopy(meta.get('events',{}));native_events={}
    for p in (mod/'events').glob('*.txt'):
        for kind,event in parse(p.read_text(encoding='utf-8-sig')):
            if kind=='country_event':native_events[first(event,'id')]=event
    for eid,event in events.items():
        require(eid in native_events,('Preview event missing from scripts',eid))
        options=[v for k,v in native_events[eid] if k=='option']
        require(len(options)==len(event['options']),('Preview event choices are stale',eid))
        for option,native in zip(event['options'],options):
            trigger=first(native,'trigger',[])
            effect=[(k,v) for k,v in native if k not in ['name','trigger','ai_chance']]
            # JSON normalizes tuples to lists. Fail rather than silently leaving stale reward prose.
            require(json.loads(json.dumps(effect))==option.get('effectAST',[]),('Preview event outcome changed; update prose',eid))
            require(json.loads(json.dumps(trigger))==option.get('triggerAST',[]),('Preview event requirements changed; update prose',eid))
            option.update(triggerAST=trigger,effectAST=effect)
    art={name:png(Image.open(game/f'gfx/interface/missions/{name}.dds')) for name in ['mission_icons_frame','mission_icons_frame_locked','mission_icons_frame_complete','mission_trigger','mission_effect']}
    data=dict(tag=manifest['tag'],countryName=manifest.get('country_name',manifest['tag']),missions=missions,decisions=decisions,events=events,effects={},cosmeticNames=meta.get('cosmeticNames',{}),art=art,version=manifest['name'],startMission=manifest.get('start_mission',missions[0]['id']),pathFlag=manifest.get('path_flag'),pathChoiceMission=manifest.get('path_choice_mission'),chapters=manifest.get('chapters',[[missions[0]['id'],'Missions']]),geometry=dict(slotWidth=104,slotHeight=152),audit=dict(revised=0,unresolved=[],titleRisks=[]))
    template=(Path(__file__).parent/'preview.html').read_text();template=template.replace('/*__DATA__*/',json.dumps(data).replace('</','<\\/'))
    template=template.replace('<title>EU4 Mission Preview</title>','<title>'+html.escape(manifest['name'])+'</title>')
    # A project-specific key prevents progress marks leaking into another country's preview.
    template=template.replace('eu4-workbench-preview-v1','eu4-workbench-'+manifest['slug'])
    target.write_text(template);target.with_name('preview-data.json').write_text(json.dumps(data,indent=2)+'\n')
