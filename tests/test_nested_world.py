"""Optional nested-compositor geometry and live-layer behavior checks."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
try:
 import numpy as np
 import cv2
except ModuleNotFoundError as exc:
 if exc.name not in {'numpy','cv2'}:raise
 np=None
if np is not None:
 from tools.nested_world_reveal import NestedWorldReveal


@unittest.skipIf(np is None,'Optional painting dependencies are not installed')
class NestedWorldTests(unittest.TestCase):
 def setUp(self):
  self.images=[np.full((64,64,3),c,np.uint8) for c in ([255,0,0],[0,255,0],[0,0,255])]
  self.events=[{'start':0,'end':1,'quad':[[16,16],[48,16],[48,48],[16,48]]},
               {'start':2,'end':3,'quad':[[8,8],[56,8],[56,56],[8,56]]}]

 def test_entire_inner_world_survives_second_exit_and_inputs_are_unchanged(self):
  originals=[a.copy() for a in self.images]
  r=NestedWorldReveal(self.images,self.events)
  np.testing.assert_allclose(r.frame(0),self.images[0]/255.)
  end=r.frame(3)
  np.testing.assert_allclose(end[0,0],[0,0,1])
  np.testing.assert_allclose(end[10,10],[0,1,0])
  np.testing.assert_allclose(end[32,32],[1,0,0])
  self.assertEqual(end.dtype,np.float32)
  for old,now in zip(originals,self.images):np.testing.assert_array_equal(old,now)

 def test_second_exit_starts_from_same_composite_and_provider_called_once_per_layer(self):
  r=NestedWorldReveal(self.images,self.events)
  np.testing.assert_allclose(r.frame(1),r.frame(2),atol=1e-6)
  calls=[]
  def live(i,t):calls.append(i);return self.images[i]
  np.testing.assert_allclose(r.frame(3,live),r.frame(3))
  self.assertEqual(calls,[2,1,0])

 def test_white_layers_have_no_dark_double_alpha_seams(self):
  images=[np.ones((64,64,3),np.float32) for _ in self.images]
  r=NestedWorldReveal(images,self.events)
  for t in [0,.31,.71,1,2,2.37,2.87,3]:np.testing.assert_allclose(r.frame(t),1,atol=1e-6)

 def test_bad_inputs_and_overlapping_events_are_rejected(self):
  with self.assertRaises(ValueError):NestedWorldReveal(self.images[:1],[])
  with self.assertRaises(ValueError):NestedWorldReveal([self.images[0],self.images[1][:32]],self.events[:1])
  bad=[dict(e) for e in self.events];bad[1]['start']=.5
  with self.assertRaises(ValueError):NestedWorldReveal(self.images,bad)
  r=NestedWorldReveal(self.images,self.events)
  for t in [-1,float('nan'),float('inf')]:
   with self.assertRaises(ValueError):r.frame(t)
  with self.assertRaises(ValueError):r.frame(3,lambda i,t:np.zeros((32,32,3),np.uint8))


if __name__=='__main__':unittest.main()
