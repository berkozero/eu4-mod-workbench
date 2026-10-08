"""Game-independent successor assignment and native preservation regressions."""
import copy
import importlib.util
from pathlib import Path
import unittest
from workbench.script import parse, first
from workbench.checks import assignment, series_nodes, evaluate

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('teutonic_patch', ROOT/'mods/teutonic/patch.py')
patch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

class JerusalemTests(unittest.TestCase):
    def test_successor_tree_and_native_exclusion(self):
        files = {'SCA_Teutonic_Missions.txt': parse('''
        teu_army_mission_slot = { slot = 4 potential = { has_dlc = "Lions of the North" OR = { tag = TEU AND = { tag = PRU was_tag = TEU } } }
          opening = { icon = army position = 1 trigger = { always = yes } effect = { add_prestige = 1 } } }
        teu_crusader_military_mission_slot = { slot = 4 potential = { has_dlc = "Lions of the North" tag = TEU has_country_flag = teu_crusader_path }
          crusade = { icon = army position = 2 required_missions = { opening } trigger = { religion = catholic } effect = { add_prestige = 2 } } }
        '''), 'EMP_CrusaderMissions.txt': parse('''
        EMP_crusader_4 = { slot = 4 potential = { has_dlc = "Emperor" OR = { tag = KOJ tag = KNI } }
          native = { icon = army position = 1 trigger = { religion = catholic } effect = { add_prestige = 3 } } }
        ''')}
        before=copy.deepcopy(files)
        patch.apply(files,{})
        series=sum((series_nodes(v) for v in files.values()),[])
        successor={'tag':'KOJ','was':['TEU'],'flags':['teu_crusader_path']}
        self.assertEqual(assignment(series,successor),assignment(series,dict(successor,tag='TEU')))
        self.assertEqual(set(assignment(series,successor)),{'opening','crusade'})
        for state in [{'tag':'KOJ'},dict(successor,was=[]),dict(successor,flags=[]),dict(successor,dlcs=['Emperor']),{'tag':'KNI'}]:
            self.assertEqual(set(assignment(series,state)),{'native'})
        for name,col in files['EMP_CrusaderMissions.txt']:
            original=first(before['EMP_CrusaderMissions.txt'],name)
            self.assertEqual([(k,v) for k,v in col if k!='potential'],[(k,v) for k,v in original if k!='potential'])
        trigger=first(first(first(files['SCA_Teutonic_Missions.txt'],'teu_crusader_military_mission_slot'),'crusade'),'trigger')
        self.assertIn(('has_country_flag','teu_crusader_path'),trigger)

    def test_dlc_and_random_new_world_conditions(self):
        self.assertTrue(evaluate(parse('has_dlc = "Emperor" is_random_new_world = no'),{'dlcs':['Emperor']}))
        self.assertFalse(evaluate(parse('has_dlc = "Lions of the North"'),{'dlcs':['Emperor']}))
        self.assertFalse(evaluate(parse('is_random_new_world = no'),{'random_new_world':True}))
