"""Behavior of the imported image library and offline preview entry."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from asset_library import catalog,child,preview,verify


class AssetLibraryTests(unittest.TestCase):
    def test_all_published_images_decode_and_match_frozen_source_bytes(self):
        result=verify()
        self.assertEqual(result['status'],'PASS',result['errors'])
        self.assertEqual((result['packs'],result['images']),(5,43))
        base,data=catalog()
        for pack in data['packs']:
            m=json.loads((base/pack['manifest']).read_text())
            self.assertTrue(all(x['sha256']==x['source_sha256'] for x in m['files']))
        self.assertAlmostEqual(data['selection']['ratio'],5/19)

    def test_preview_is_actual_image_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'new/preview.png';preview('paper-classroom',out)
            with Image.open(out) as im:
                im.load();self.assertGreater(im.width,600);self.assertGreater(im.height,200)
            original=out.read_bytes()
            with self.assertRaises(FileExistsError):preview('paper-classroom',out)
            self.assertEqual(original,out.read_bytes())

    def test_cli_works_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            result=subprocess.run([sys.executable,str(ROOT/'tools/asset_library.py'),'verify','--pack','poetry-book'],cwd=temp,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['images'],7)

    def test_path_escape_and_unknown_pack_do_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):child(Path(temp),'../outside.png')
            out=Path(temp)/'should-not-exist.png'
            with self.assertRaises(ValueError):preview('not-a-pack',out)
            self.assertFalse(out.exists())

    def test_changed_image_is_reported_without_claiming_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);base=root/'assets/library/demo';base.mkdir(parents=True)
            (base/'image.png').write_bytes(b'changed')
            (base/'manifest.json').write_text(json.dumps({'id':'demo','license':'MIT','files':[{'file':'image.png','sha256':'0'*64,'size':[1,1]}]}))
            (base.parent/'catalog.json').write_text(json.dumps({'license':'MIT','packs':[{'id':'demo','manifest':'demo/manifest.json','image_count':1}],'image_count':1}))
            result=verify(root)
            self.assertEqual(result['status'],'FAIL')
            self.assertIn('SHA mismatch',result['errors'][0])


if __name__=='__main__':unittest.main()
