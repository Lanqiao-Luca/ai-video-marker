"""Behavioral checks for preservation, configuration and actual media operations."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from attach_audio import attach
from check_video import inspect
from init_project import create
from media import decode_frames,ffmpeg_path,probe,run,sha256
from pixel_engine import PixelRenderer,load_scene,validate_scene
from check_pixel_baseline import verify
from garden_drawing import GardenRenderer,PALETTES
from make_video import make_scene
from harbor_drawing import HarborRenderer
from harbor_assets import build as build_harbor_assets


class HarborTests(unittest.TestCase):
    def test_asset_kit_can_be_regenerated_and_reused_without_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'kit'
            manifest=build_harbor_assets(out)
            shipped=json.loads((ROOT/'assets/harbor/manifest.json').read_text())
            self.assertEqual(manifest,shipped)
            self.assertEqual(len(manifest['files']),12)
            self.assertTrue(all(sha256(out/name)==v['sha256'] for name,v in manifest['files'].items()))
            with self.assertRaises(FileExistsError):build_harbor_assets(out)

    def test_broken_asset_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit=Path(temporary)/'kit';shutil.copytree(ROOT/'assets/harbor',kit)
            (kit/'robot-head.png').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'SHA mismatch'):
                HarborRenderer(make_scene(42,'sunset','harbor'),asset_root=kit)

    def test_pickup_installation_and_power_have_continuous_identity(self):
        scene=make_scene(42,'sunset','harbor');scene['output_size']=[180,320]
        renderer=HarborRenderer(scene)
        for c in scene['cells']:
            for event in (c['pick'],c['insert']):
                before=renderer.frame(event-.001)[1];after=renderer.frame(event+.001)[1]
                b=next(x for x in before['cells'] if x['asset']==c['asset'])
                a=next(x for x in after['cells'] if x['asset']==c['asset'])
                self.assertLess(sum(abs(x-y) for x,y in zip(a['world'],b['world'])),.02)
        previous=0
        for k in range(36*24):
            tr=renderer.frame(k/24)[1]
            self.assertLess(sum(abs(a-b) for a,b in zip(tr['right_hand_world'],tr['requested_hand_world'])),1e-7)
            self.assertGreaterEqual(tr['inserted_cells'],previous);previous=tr['inserted_cells']
            if k<24*24:self.assertEqual(tr['beacon_power'],0)
            self.assertTrue(all(0<=v<=1 for v in tr['robot_normalized_bbox']))
        final=renderer.frame(35)[1]
        self.assertEqual([c['state'] for c in final['cells']],['installed']*3)
        self.assertEqual(final['beacon_power'],1)
        self.assertGreater(final['boat_world'][0],renderer.frame(0)[1]['boat_world'][0]+100)

    def test_theme_selection_and_list_are_explicit(self):
        with tempfile.TemporaryDirectory() as temporary:
            result=subprocess.run([sys.executable,str(ROOT/'tools/make_video.py'),'--list'],cwd=temporary,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            listed=json.loads(result.stdout);self.assertEqual(listed['default'],'harbor')
            self.assertEqual(len(listed['stories']),3)
            self.assertFalse((Path(temporary)/'outputs').exists())
        robot=HarborRenderer(make_scene(42,'sunset','harbor')).frame(8)[0].tobytes()
        rabbit=GardenRenderer(make_scene(42,'moon','garden')).frame(8)[0].tobytes()
        self.assertNotEqual(robot,rabbit)


class FirstVideoTests(unittest.TestCase):
    def test_seed_is_repeatable_and_distinct_from_showcase(self):
        scene=make_scene(42,'moon')
        first=GardenRenderer(scene)
        picture=first.frame(8)[0].tobytes()
        self.assertEqual(picture,GardenRenderer(scene).frame(8)[0].tobytes())
        self.assertNotEqual(picture,GardenRenderer(make_scene(43,'moon')).frame(8)[0].tobytes())
        self.assertNotEqual(picture,PixelRenderer(load_scene(ROOT/'examples/pixel/scene.json')).frame(8)[0].tobytes())
        for palette in PALETTES:
            other=GardenRenderer(make_scene(42,palette))
            if palette!='moon':self.assertNotEqual(picture,other.frame(8)[0].tobytes())
        self.assertEqual(picture,first.frame(8)[0].tobytes())

    def test_crank_contact_and_progress_are_preserved(self):
        renderer=GardenRenderer(make_scene(42,'moon'))
        previous=0
        for k in range(4*24,12*24+1):
            trace=renderer.frame(k/24)[1]
            self.assertLess(sum(abs(a-b) for a,b in zip(trace['right_hand_world'],trace['crank_world'])),1e-8)
            self.assertGreaterEqual(trace['spring_charge'],previous)
            previous=trace['spring_charge']
            self.assertTrue(all(0<=v<=1 for v in trace['rabbit_normalized_bbox']))
        start=renderer.frame(0)[1];finish=renderer.frame(31)[1]
        self.assertEqual(start['flower_openings'],[0,0,0])
        self.assertEqual(finish['flower_openings'],[1,1,1])
        self.assertEqual(finish['bird_opening'],1)

    def test_entry_writes_to_caller_and_records_scene_with_audio(self):
        with tempfile.TemporaryDirectory() as temporary:
            args=[sys.executable,'-B',str(ROOT/'tools/make_video.py'),'--seed','42','--start','8','--end','8.25']
            result=subprocess.run(args,cwd=temporary,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            folders=list((Path(temporary)/'outputs').iterdir());self.assertEqual(len(folders),1)
            out=folders[0];data=json.loads((out/'run.json').read_text())
            self.assertEqual(data['example'],'robot-lighthouse')
            self.assertEqual(data['expected']['frames'],6)
            self.assertEqual(data['audio_source_start'],8)
            scene=json.loads((out/'scene.json').read_text())
            self.assertEqual(scene['seed'],42)
            self.assertEqual(data['scene_sha256'],sha256(out/'scene.json'))
            self.assertEqual(data['audio_fade_out'],.125)
            self.assertTrue(probe(out/'video.mp4',ffmpeg_path())['has_audio'])
            before=sha256(out/'video.mp4')
            again=subprocess.run(args+['--out',str(out)],cwd=temporary,capture_output=True)
            self.assertNotEqual(again.returncode,0)
            self.assertEqual(before,sha256(out/'video.mp4'))

    def test_bad_seed_fails_without_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'bad'
            result=subprocess.run([sys.executable,str(ROOT/'tools/make_video.py'),'--seed','-1','--out',str(out)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(out.exists())


class ProjectTests(unittest.TestCase):
    def test_existing_project_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'project'
            create('pixel','test-pixel',out)
            marker=out/'preserve.txt';marker.write_text('original')
            before=(out/'status.json').read_bytes()
            with self.assertRaises(FileExistsError):create('pixel','replacement',out)
            self.assertEqual(marker.read_text(),'original')
            self.assertEqual(before,(out/'status.json').read_bytes())
            self.assertEqual(len(list((out/'worksheets').iterdir())),12)

    def test_candidate_route_stays_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'project'
            create('paperbook','candidate',out)
            data=json.loads((out/'status.json').read_text())
            self.assertEqual(data['workflow_status'],'candidate')
            self.assertEqual(data['status'],'PLANNED')
            self.assertEqual(data['adoption'],'PENDING')

    def test_asset_choice_is_preserved_without_generating_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'project'
            create('pixel','reuse-assets',out,asset_mode='reuse')
            data=json.loads((out/'status.json').read_text())
            self.assertEqual(data['asset_strategy'],'reuse')
            self.assertEqual(data['artifacts'],[])
            self.assertEqual(data['status'],'PLANNED')


class PixelTests(unittest.TestCase):
    def setUp(self):self.scene=load_scene(ROOT/'examples/pixel/scene.json')

    def test_invalid_timing_fails_before_output_creation(self):
        bad=copy.deepcopy(self.scene);bad['camera_keys'][1][0]=-1
        with self.assertRaises(ValueError):validate_scene(bad)
        bad=copy.deepcopy(self.scene);bad['fps']=0
        with self.assertRaises(ValueError):validate_scene(bad)
        with tempfile.TemporaryDirectory() as temporary:
            scene=Path(temporary)/'bad.json';scene.write_text(json.dumps(bad))
            out=Path(temporary)/'should-not-exist'
            result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/render_pixel.py'),
                '--scene',str(scene),'--out',str(out)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(out.exists())

    def test_missing_audio_is_reported_before_render(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'should-not-exist'
            result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/render_pixel.py'),
                '--audio',str(Path(temporary)/'missing.wav'),'--out',str(out)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(out.exists())

    def test_subclip_uses_matching_audio_offset(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)/'music-pilot'
            result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/render_pixel.py'),
                '--start','16','--end','16.25','--out',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            data=json.loads((out/'run.json').read_text())
            self.assertEqual(data['audio_source_start'],16)
            self.assertEqual(data['expected']['frames'],6)
            self.assertTrue(data['expected']['audio'])
            self.assertTrue(probe(out/'video.mp4',ffmpeg_path())['has_audio'])

    def test_camera_change_is_isolated_to_its_renderer(self):
        original=PixelRenderer(self.scene)
        before=original.frame(12)[0].tobytes()
        changed=copy.deepcopy(self.scene)
        for key in changed['camera_keys']:key[1]+=10
        validate_scene(changed)
        modified=PixelRenderer(changed)
        self.assertNotEqual(before,modified.frame(12)[0].tobytes())
        self.assertEqual(before,original.frame(12)[0].tobytes())

    def test_all_original_frames_and_drawing_functions_are_preserved(self):
        result=verify(ROOT/'examples/pixel/scene.json',ROOT/'examples/pixel/source-frame-baseline.json')
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['frames_checked'],1056)
        self.assertEqual(result['mismatched_frames'],[])
        self.assertTrue(result['source_drawing_functions_unchanged'])


class MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.ffmpeg=ffmpeg_path()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.directory=Path(self.temp.name)
        self.video=self.directory/'fixture.mp4'
        run([self.ffmpeg,'-v','error','-nostdin','-n','-f','lavfi','-i',
             'color=c=blue:s=64x48:r=8:d=1','-an','-c:v','libx264','-pix_fmt','yuv420p',self.video])

    def tearDown(self):self.temp.cleanup()

    def test_decode_and_expected_frame_mismatch(self):
        self.assertEqual(decode_frames(self.video,self.ffmpeg),8)
        good=inspect(self.video,self.ffmpeg,dict(width=64,height=48,frames=8,fps=8,audio=False))
        self.assertEqual(good['status'],'PASS')
        bad=inspect(self.video,self.ffmpeg,dict(frames=9))
        self.assertEqual(bad['status'],'FAIL')

    def test_mismatched_manifest_is_rejected(self):
        manifest=self.directory/'run.json';report=self.directory/'report.json'
        manifest.write_text(json.dumps(dict(status='RENDERED',video_sha256='0'*64,expected={})))
        result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/check_video.py'),str(self.video),
            '--manifest',str(manifest),'--out',str(report),'--ffmpeg',self.ffmpeg],capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(report.exists())

    def make_audio(self,name,seconds):
        audio=self.directory/name
        with wave.open(str(audio),'wb') as stream:
            stream.setparams((1,2,16000,0,'NONE','not compressed'))
            stream.writeframes(b'\0\0'*round(seconds*16000))
        return audio

    def test_audio_attachment_preserves_picture_and_rejects_short_input(self):
        short=self.make_audio('short.wav',.25)
        out=self.directory/'new.mp4'
        with self.assertRaises(ValueError):attach(self.video,short,out,0,self.ffmpeg)
        self.assertFalse(out.exists())
        audio=self.make_audio('enough.wav',2)
        attach(self.video,audio,out,.2,self.ffmpeg)
        self.assertTrue(probe(out,self.ffmpeg)['has_audio'])
        self.assertEqual(decode_frames(out,self.ffmpeg),8)
        def hashes(path):
            return run([self.ffmpeg,'-v','error','-i',path,'-map','0:v:0','-an','-f','framemd5','-']).stdout
        self.assertEqual(hashes(self.video),hashes(out))
        before=sha256(out)
        with self.assertRaises(FileExistsError):attach(self.video,audio,out,0,self.ffmpeg)
        self.assertEqual(before,sha256(out))


if __name__=='__main__':unittest.main()
