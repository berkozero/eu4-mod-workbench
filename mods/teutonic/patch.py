"""Country-specific visibility policy; shared tooling contains no country assumptions."""
from workbench.script import first,parse

def apply(files,manifest):
    committed=('has_country_flag','teu_crusader_path')
    visible=parse('OR = { has_country_flag = teu_crusader_path NOT = { has_country_flag = teu_prussian_path } }')[0]
    for name,col in files['SCA_Teutonic_Missions.txt']:
        if name.startswith('teu_crusader_'):
            potential=first(col,'potential');assert committed in potential
            potential[potential.index(committed)]=visible
            for _,mission in col:
                if isinstance(mission,list) and first(mission,'icon'):first(mission,'trigger').insert(0,committed)
        elif name.startswith('teu_dummy_mission_slot_'):first(col,'potential').append(('always','no'))
