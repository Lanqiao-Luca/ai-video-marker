"""Validate the rooftop example and isolate its preserved drawing implementation."""
import copy
import importlib.util
import json
import math
from pathlib import Path

DRAWING=Path(__file__).with_name('pixel_drawing.py')


def number(value):
    return type(value) in (int,float) and math.isfinite(value)


def validate_scene(scene):
    if scene.get('schema_version')!=1 or scene.get('id')!='rooftop-sunshine':
        raise ValueError('Expected the rooftop-sunshine scene schema.')
    if scene.get('logical_size')!=[360,640]:
        raise ValueError('The preserved rooftop drawing uses a fixed 360x640 world.')
    size=scene.get('output_size')
    if (not isinstance(size,list) or len(size)!=2 or
            any(type(v) is not int or not 64<=v<=4096 or v%2 for v in size) or size[0]*640!=size[1]*360):
        raise ValueError('Output needs even portrait dimensions with the original 9:16 aspect.')
    fps=scene.get('fps');duration=scene.get('duration')
    if type(fps) is not int or not 1<=fps<=60:
        raise ValueError('fps must be an integer in [1, 60].')
    if duration!=44:
        raise ValueError('This reproduction preserves the original 44-second story timing.')
    if scene.get('audio') is not None:
        raise ValueError('Drawing configuration stays audio-independent; use render_pixel.py --audio or --silent.')
    for name,length in [('rabbit_path',3),('camera_keys',4)]:
        keys=scene.get(name)
        if not isinstance(keys,list) or len(keys)<2:
            raise ValueError('Missing path: '+name)
        previous=-1
        for key in keys:
            if (not isinstance(key,list) or len(key)!=length or not all(number(v) for v in key) or
                    not 0<=key[0]<=duration or key[0]<=previous):
                raise ValueError('Path times must be finite, sorted and within the story: '+name)
            previous=key[0]
            if not 0<=key[1]<=360 or not 0<=key[2]<=640:
                raise ValueError('Path point lies outside the shared world: '+name)
            if name=='camera_keys' and not 0<key[3]<=360:
                raise ValueError('Camera width must be in (0, 360].')
        if keys[0][0]!=0 or keys[-1][0]!=duration:
            raise ValueError('Path must cover the complete story: '+name)
    objects=scene.get('objects',{})
    required={'wheel','basin','gear','flower','clothesline','umbrella','cloud'}
    if set(objects)!=required:raise ValueError('Missing rooftop objects.')
    for name,value in objects.items():
        if name=='clothesline':
            span=value.get('span')
            if not isinstance(span,list) or len(span)!=4 or not all(number(v) for v in span):
                raise ValueError('Invalid clothesline span.')
            points=[span[:2],span[2:]]
        else:
            point=value.get('placed_center' if name=='umbrella' else 'center')
            points=[point]
        for point in points:
            if (not isinstance(point,list) or len(point)!=2 or not all(number(v) for v in point) or
                    not 0<=point[0]<=360 or not 0<=point[1]<=640):
                raise ValueError('Invalid object location: '+name)
    radius=objects['wheel'].get('radius')
    if not number(radius) or not 4<=radius<=64:raise ValueError('Invalid waterwheel radius.')
    return scene


def load_scene(path):
    return validate_scene(json.loads(Path(path).read_text(encoding='utf-8')))


class PixelRenderer:
    """Each instance owns its world; configuring another instance cannot change it."""
    def __init__(self,scene):
        self.scene=copy.deepcopy(validate_scene(scene))
        spec=importlib.util.spec_from_file_location('_rooftop_drawing_instance',DRAWING)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.initialize(self.scene)
        self._drawing=module

    def frame(self,second):
        if not number(second) or not 0<=second<self.scene['duration']:
            raise ValueError('Frame time must be within the story.')
        return self._drawing.frame(second)
