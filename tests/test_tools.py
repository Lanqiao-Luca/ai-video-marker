"""Behavioral checks for preservation, configuration and actual media operations."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
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
