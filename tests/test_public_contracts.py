"""Mutation checks for omitted handoffs and invalid classified capability data."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from check_package import check_video_contracts


class PublicContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.catalog=json.loads((ROOT/'catalog.json').read_text())
        defaults=self.catalog['framework']['video_defaults']
        paths=set(self.catalog['framework']['property_targets'])
        paths.update(defaults[k] for k in ('role','skill','record_template'))
        paths.update(r['workflow'] for r in self.catalog['routes'])
        for rel in paths:
            out=self.root/rel
            out.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/rel,out)

    def test_current_contracts_and_candidate_statuses_are_valid(self):
        self.assertEqual(check_video_contracts(self.root,self.catalog),[])
        self.assertEqual(sum(r['status']=='candidate' for r in self.catalog['routes']),3)

    def test_missing_workflow_handoff_is_detected(self):
        route=self.catalog['routes'][0]
        p=self.root/route['workflow']
        p.write_text(p.read_text().replace('../agents/制作视频.md#public-entry','../agents/导演与策划.md'))
        self.assertTrue(any('must hand off' in x for x in check_video_contracts(self.root,self.catalog)))

    def test_omitted_public_atom_is_detected(self):
        p=self.root/self.catalog['framework']['video_defaults']['skill']
        p.write_text('\n'.join(x for x in p.read_text().splitlines() if not x.startswith('|[AN13 ')))
        self.assertTrue(any('atom IDs' in x for x in check_video_contracts(self.root,self.catalog)))

    def test_bad_or_missing_properties_do_not_pass(self):
        p=self.root/'standards/atom-properties.md'
        original=p.read_text()
        for broken in [original.replace('atom_nature:', 'missing_nature:',1),
                       original.replace('atom_nature: "method"','atom_nature: "invalid"',1),
                       original.replace('atom_secondary_natures: ["principle", "operation", "acceptance"]',
                                        'atom_secondary_natures: ["method"]',1),
                       original.replace('"## AT01 按正文判断"','"## NONEXISTENT"',1)]:
            with self.subTest(broken=broken[:40]):
                p.write_text(broken)
                self.assertTrue(check_video_contracts(self.root,self.catalog))
        p.write_text(original)

    def test_malformed_group_map_returns_a_failure_instead_of_crashing(self):
        p=self.root/'standards/atom-properties.md'
        original=p.read_text()
        import re
        for value in ['null','{}','[null]','["invalid"]','[{"selector": null}]']:
            with self.subTest(value=value):
                p.write_text(re.sub(r'^atom_nature_map:.*$',
                                    'atom_nature_map: '+value,original,flags=re.M))
                self.assertTrue(check_video_contracts(self.root,self.catalog))


if __name__=='__main__':unittest.main()
