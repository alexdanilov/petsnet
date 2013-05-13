import os.path
import shutil
from PIL import Image, ImageEnhance
from PIL import ImageOps
from django.conf import settings
from django.db.models.fields.files import ImageField
from django.db.models import signals


def get_upload_to(instance, filename):
    return '%d-0.jpg' % instance._get_pk_val()


class StdImageField(ImageField):
    def __init__(self, verbose_name=None, name=None, width_field=None,
        height_field=None, sizes=None, **kwargs):

        self.sizes = sizes
        super(StdImageField, self).__init__(verbose_name, name, width_field,
            height_field, **kwargs)

    def contribute_to_class(self, cls, name):
        """Call methods for generating all operations on specified signals"""
        super(StdImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self.resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnail, sender=cls)

    def reduce_opacity(self, img, opacity):
        """Returns an image with reduced opacity."""

        assert opacity >= 0 and opacity <= 1
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        else:
            img = img.copy()
        alpha = img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        img.putalpha(alpha)

        return img

    def set_watermark(self, img, padding=10, opacity=1):
        mark = Image.open(os.path.join(settings.ROOT_PATH, 'apps', 'watermark.png'))

        #img_w_p = img.size[0] - padding
        #if img_w_p < mark.size[0]:
        #    ratio = float(img_w_p) / mark.size[0]
        #    w = int(mark.size[0] * ratio)
        #    h = int(mark.size[1] * ratio)
        #    mark = mark.resize((w, h))

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        if opacity < 1:
            mark = self.reduce_opacity(mark, opacity)

        # create a transparent layer the size of the image and draw the watermark in that layer.
        layer = Image.new('RGBA', img.size, (0,0,0,0))
        position = (padding, img.size[1] - mark.size[1] - padding)
        layer.paste(mark, position)
        return Image.composite(layer, img, layer)

    def resize_image(self, instance=None, **kwargs):
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                shutil.copyfile(filename, '%s/%d-0.jpg' % (os.path.dirname(filename), instance._get_pk_val()))
                for i, size in enumerate(self.sizes):
                    img = Image.open(filename)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.thumbnail(size, Image.ANTIALIAS)

                    # set watermark to last image size
                    #if i == 3:
                    #    img = self.set_watermark(img, 20, 1)

                    new_filename = '%s/%d-%d.jpg' % (os.path.dirname(filename), instance._get_pk_val(), i + 1)
                    img.save(new_filename, "JPEG", quality=100)
                
                #remove source file
                os.remove(filename)

    def _set_thumbnail(self, instance=None, **kwargs):
        if instance._get_pk_val() and getattr(instance, self.name):
            for i, size in enumerate(self.sizes):
                k = i + 1
                setattr(getattr(instance, self.name), 'image%d' % k, '%s%d-%d.jpg'\
                % (self.upload_to, instance._get_pk_val(), k))