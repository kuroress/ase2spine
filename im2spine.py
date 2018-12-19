import sys
import json

import imageio
from PIL import Image
import glob
import os


class SpineImage:
    def __init__(self, file_name):
        self.file_name = file_name

    def tagname(self):
        return self.basename().split("-", 1)[0]

    def layername(self):
        return self.basename().split("-", 1)[1]

    def basename(self):
        return os.path.splitext(os.path.basename(self.file_name))[0]

    def to_slot(self):
        return {
            "name": self.basename(),
            "bone": "root",
            "attachment": self.basename()
        }

    def to_skin(self):
        im = imageio.imread(self.file_name)
        x1, y1, x2, y2 = Image.fromarray(im[:, :, :3]).getbbox()
        xc, yc = (x1+x2)/2, (y1+y2)/2
        return {
            self.basename(): {
                "x": xc,
                "y": -yc,
                "width": x2 - x1,
                "height": y2 - y1
            }
        }

    def trim(self):
        im = imageio.imread(self.file_name)
        bbox = Image.fromarray(im[:, :, :3]).getbbox()
        Image.open(self.file_name).crop(bbox).save(self.file_name)


class SpineSkeleton:
    VERSION = "3.7.76-beta"

    def __init__(self, im_dir):
        self.im_dir = im_dir

    def images(self):
        images = [SpineImage(im_path) for im_path
                  in glob.glob(os.path.join(self.im_dir, '*.png'))]
        images = {im.layername(): im for im in images}
        images = [images[l] for l in self.layers()]
        return list(reversed(images))

    def layers(self):
        with open(os.path.join(self.im_dir, 'layers.txt'), 'r') as f:
            return f.read().splitlines()

    def to_json(self):
        images = self.images()
        return {
            "skeleton": {
                "spine": SpineSkeleton.VERSION
            },
            "bones": [
                {
                    "name": "root"
                }
            ],
            "slots": [
                im.to_slot() for im in images
            ],
            "skins": {
                "default": {
                    im.basename(): im.to_skin() for im in images
                }
            }
        }

    def trim_images(self):
        for im in self.images():
            im.trim()


if __name__ == '__main__':
    im_dir = sys.argv[1]
    json_name = f"{im_dir}/{os.path.basename(im_dir)}.json"
    sk = SpineSkeleton(im_dir)
    with open(json_name, 'w') as f:
        json.dump(sk.to_json(), f)
    sk.trim_images()
