"""Create an intentionally un-installable draft until its native integration is reviewed."""
import json,re
from .checks import require

def scaffold(root,country,tag):
    require(re.fullmatch('[A-Z0-9]{3}',tag),'Use a three-character uppercase country tag')
    project=root/'mods'/country;require(not project.exists(),'Country folder already exists')
    (project/'content/localisation').mkdir(parents=True)
    namespace='wb_'+country.replace('-','_');series=namespace+'_missions';slug=namespace
    manifest=dict(name=country.title()+' mission extension',country_name=country.title(),slug=slug,namespace=namespace,tag=tag,supported_version='1.37.*',draft=True,primary_mission_file=namespace+'_missions.txt',series={series:'slot = 1 generic = no ai = yes potential = { tag = '+tag+' }'},baseline_ids={},start_mission='M01',chapters=[['M01','Opening']])
    specs=[]
    for index,(title,trigger,conditions,effect,reward) in enumerate([('Prepare the Army','army_size_percentage = 0.8','Reach 80% of force limit.','add_prestige = 5','Gain 5 prestige.'),('Fund the Campaign','treasury = 100','Hold 100 ducats.','add_army_tradition = 5','Gain 5 army tradition.')],1):
        id='M0'+str(index);parents=[] if index==1 else ['M01']
        specs.append(dict(id=id,scriptId=namespace+'_'+id.lower(),title=title,lane=0,position=index,series=series,parents=parents,arrowParents=parents,checklistParents=[],icon='mission_build_up_to_force_limit',trigger=trigger,conditions=conditions,effect=effect,rewards=[dict(script=effect,text=reward)],rewardText=reward,why='Draft gameplay example; replace with researched country context.',source=dict(root='Draft; no historical claim.',url=''),claims=[],eventIds=[],intermediate=False))
    (project/'project.json').write_text(json.dumps(manifest,indent=2)+'\n');(project/'missions.json').write_text(json.dumps(specs,indent=2)+'\n')
    (project/'content/descriptor.mod').write_text(f'name="{manifest["name"]}"\nversion="0.1.0"\nsupported_version="1.37.*"\ntags={{ "Missions And Decisions" }}\n')
    (project/'README.md').write_text('''# Country draft

These two missions demonstrate the file format; they are not researched historical content. `draft: true` blocks installation. Building a preview is safe and does not enable the mod.

Before installation, inspect this tag's native mission files and DLC/flag assignment. For an existing tree, list its `base_mission_files`, choose `primary_mission_file`, put the target series in `native_series_by_slot`, remove the standalone `series` entry, and replace each mission's `series` field with the actual native series. Put missions after its occupied range; list the native baseline aliases needed in `baseline_ids`. Author baseline preview summaries in `preview-content.json` if those entries appear in the preview. Add assignment fixtures and check the effective tree. Only then set `draft` to false.

Use the Teutonic example for the file format, not as a required country design. Keep shared tools country-neutral.
''')
