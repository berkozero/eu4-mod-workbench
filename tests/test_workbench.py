import json,sqlite3,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
from workbench.script import parse,dump
from workbench.checks import assignment,series_nodes,arrow_errors,acyclic,loading_check,load_order_check,ValidationError
from workbench.install import install
from workbench.scaffold import scaffold

class RegressionTests(unittest.TestCase):
    def test_parser_preserves_repeated_keys_and_lists(self):
        source='x = { OR = { a = yes a = no } required_missions = { first second } title = "a # b" } # comment'
        self.assertEqual(parse(source),parse(dump(parse(source))))
    def test_parser_rejects_truncated_script(self):
        for bad in ['x = {','x =','x = }','x = { y = }','}']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):parse(bad)
    def test_series_overlap_even_without_duplicate_cells(self):
        series=series_nodes(parse('a = { slot = 1 first = { icon = x position = 2 } last = { icon = x position = 4 } } b = { slot = 1 middle = { icon = x position = 3 } }'))
        with self.assertRaisesRegex(ValidationError,'Overlapping'):assignment(series,{})
    def test_mutually_exclusive_series_do_not_conflict(self):
        s=series_nodes(parse('a = { slot = 1 potential = { has_country_flag = branch } x = { icon = x position = 1 } } b = { slot = 1 potential = { NOT = { has_country_flag = branch } } y = { icon = x position = 1 } }'))
        self.assertEqual(set(assignment(s,{})),{'y'});self.assertEqual(set(assignment(s,{'flags':['branch']})),{'x'})
    def test_unsupported_assignment_condition_fails_closed(self):
        s=series_nodes(parse('a = { slot = 1 potential = { unknown = yes } x = { icon = x position = 1 } }'))
        with self.assertRaisesRegex(ValidationError,'does not support'):assignment(s,{})
    def test_annex_and_hospitaller_diagonal_regression(self):
        for distance in [2,13]:
            nodes={'parent':dict(lane=0,position=1,parents=[]),'child':dict(lane=1,position=1+distance,parents=['parent'])}
            self.assertTrue(arrow_errors(nodes));nodes['child']['position']=2;self.assertFalse(arrow_errors(nodes))
    def test_vertical_line_cannot_pass_through_optional_mission(self):
        nodes={'parent':dict(lane=0,position=1,parents=[]),'optional':dict(lane=0,position=2,parents=[]),'child':dict(lane=0,position=3,parents=['parent'])}
        self.assertTrue(arrow_errors(nodes));nodes.pop('optional');self.assertFalse(arrow_errors(nodes))
    def test_backward_missing_and_cycles(self):
        self.assertTrue(arrow_errors({'x':dict(lane=0,position=1,parents=['missing'])}))
        with self.assertRaises(ValidationError):acyclic({'x':{'y'},'y':{'x'}})
    def test_loading_selector_zero_divisor_regression(self):
        with self.assertRaises(ValidationError):loading_check('',{'load_0.dds'})
        with self.assertRaises(ValidationError):loading_check('replace_path="gfx/loadingscreens"',{'a.dds','b.dds'})
        loading_check('',{'load_0.dds','load_37.dds'})
    def test_launcher_invalid_manual_mode_regression(self):
        with self.assertRaises(ValidationError):load_order_check('manual')
        load_order_check('custom')
    def test_install_preserves_playsets_enabled_mods_and_backup(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);package=root/'package';source=package/'test_mod';source.mkdir(parents=True)
            (source/'descriptor.mod').write_text('name="Test"\n');(source/'mission.txt').write_text('new');(package/'test_mod.mod').write_text('')
            user=root/'user';dest=user/'mod/test_mod';dest.mkdir(parents=True);(dest/'old.txt').write_text('old')
            (user/'mod/unrelated').mkdir();(user/'mod/unrelated/keep').write_text('unchanged')
            config=b'{"enabled_mods":["mod/general.mod"],"disabled_dlcs":["keep"]}';(user/'dlc_load.json').write_bytes(config)
            c=sqlite3.connect(user/'launcher-v2.sqlite');c.execute('create table playsets(name text,loadOrder text)');c.execute("insert into playsets values ('Mine','custom')");c.commit();c.close();db=(user/'launcher-v2.sqlite').read_bytes()
            result=install(package,user,root/'backup',check_processes=False)
            self.assertEqual((user/'dlc_load.json').read_bytes(),config);self.assertEqual((user/'launcher-v2.sqlite').read_bytes(),db)
            self.assertEqual((user/'mod/unrelated/keep').read_text(),'unchanged');self.assertFalse((dest/'old.txt').exists())
            self.assertEqual((Path(result['backup'])/'test_mod/old.txt').read_text(),'old')
            # Repeat install must also preserve unrelated state and replace only its owned folder.
            install(package,user,root/'backup',check_processes=False);self.assertEqual((user/'launcher-v2.sqlite').read_bytes(),db)
    def test_failed_first_install_rolls_back_new_folder(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);package=root/'package';source=package/'test_mod';source.mkdir(parents=True)
            (source/'descriptor.mod').write_text('name="Test"\n');(package/'test_mod.mod').write_text('')
            user=root/'user'
            with patch.object(Path,'write_text',side_effect=OSError('simulated descriptor write failure')):
                with self.assertRaises(OSError):install(package,user,root/'backups',check_processes=False)
            self.assertFalse((user/'mod/test_mod').exists())

    def test_cli_refuses_draft_install_before_build(self):
        import eu4
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);scaffold(root,'france','FRA')
            with patch.object(eu4,'ROOT',root),patch('sys.argv',['eu4.py','install','france']):
                with self.assertRaisesRegex(ValueError,'Draft country'):eu4.main()
            self.assertFalse((root/'dist').exists())

    def test_example_authoring_contract(self):
        root=Path(__file__).resolve().parents[1]
        for project in (root/'mods').iterdir():
            if not (project/'project.json').exists():continue
            manifest=json.loads((project/'project.json').read_text());specs=json.loads((project/'missions.json').read_text())
            meta=json.loads((project/'preview-content.json').read_text()) if (project/'preview-content.json').exists() else {}
            baseline=[m for m in meta.get('missions',[]) if m['scriptId'] in manifest.get('baseline_ids',{}).values()]
            entries=baseline+specs;ids={m['id']:m for m in entries}
            self.assertEqual(len(ids),len(entries));self.assertEqual(len({m['scriptId'] for m in entries}),len(entries))
            cells=set();nodes={}
            for m in entries:
                cell=(m['lane'],m['position']);self.assertNotIn(cell,cells);cells.add(cell)
                arrows=m.get('arrowParents',m['parents']);nodes[m['id']]=dict(lane=m['lane'],position=m['position'],parents=arrows)
                if m in specs:
                    self.assertFalse(set(arrows)&set(m['checklistParents']))
                    self.assertEqual(set(arrows)|set(m['checklistParents']),set(m['parents']))
                    parse(m['trigger']);parse(m['effect'])
                    self.assertTrue(m['source']['root']);self.assertTrue(m['why'])
                    self.assertTrue(m['rewards'])
            self.assertFalse(arrow_errors(nodes));acyclic({m['id']:set(m['parents']) for m in entries})

    def test_scaffold_is_country_neutral_and_draft(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);scaffold(root,'france','FRA');p=json.loads((root/'mods/france/project.json').read_text())
            self.assertEqual(p['tag'],'FRA');self.assertTrue(p['draft']);self.assertNotIn('teu',json.dumps(p).lower())
            with self.assertRaises(ValidationError):scaffold(root,'france','FRA')

if __name__=='__main__':unittest.main()
