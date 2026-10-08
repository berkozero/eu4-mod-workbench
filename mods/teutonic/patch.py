"""Country-specific visibility and Teutonic Jerusalem succession policy."""
from workbench.script import first,parse

JERUSALEM = 'tag = KOJ was_tag = TEU has_country_flag = teu_crusader_path has_dlc = "Lions of the North"'
OPENING_SERIES = {'teu_livonian_mission_slot', 'teu_danzig_and_poland_mission_slot', 'teu_army_mission_slot'}

def apply(files,manifest):
    committed=('has_country_flag','teu_crusader_path')
    visible=parse('OR = { has_country_flag = teu_crusader_path NOT = { has_country_flag = teu_prussian_path } }')[0]
    successor=parse('AND = { '+JERUSALEM+' }')[0]
    for name,col in files['SCA_Teutonic_Missions.txt']:
        potential=first(col,'potential')
        if name in OPENING_SERIES:
            first(potential,'OR').append(successor)
        if name.startswith('teu_crusader_'):
            assert committed in potential
            potential[potential.index(committed)]=visible
            potential[potential.index(('tag','TEU'))]=('OR',[('tag','TEU'),successor])
            for _,mission in col:
                if isinstance(mission,list) and first(mission,'icon'):first(mission,'trigger').insert(0,committed)
        elif name.startswith('teu_dummy_mission_slot_'):potential.append(('always','no'))
    # The successor retains the extended Order campaign instead of competing
    # with Emperor's five native Crusader series for the same slots.
    for _,col in files['EMP_CrusaderMissions.txt']:
        first(col,'potential').append(('NOT',parse(JERUSALEM)))
