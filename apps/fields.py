import os
import shutil
from PIL import Image
from PIL import ImageOps
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

    def resize_image(self, instance=None, **kwargs):
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            shutil.copyfile(filename, '%s/%d-0.jpg' % (os.path.dirname(filename), instance._get_pk_val()))
            for i, size in enumerate(self.sizes):
                img = Image.open(filename)
                img = ImageOps.fit(img, size, method=Image.ANTIALIAS)
                new_filename = '%s/%d-%d.jpg' % (os.path.dirname(filename), instance._get_pk_val(), i + 1)
                img.save(new_filename, "JPEG", quality=100)

    def _set_thumbnail(self, instance=None, **kwargs):
        if getattr(instance, self.name):
            for i, size in enumerate(self.sizes):
                k = i + 1
                setattr(getattr(instance, self.name), 'image%d' % k, '%s%d-%d.jpg'\
                % (self.upload_to, instance._get_pk_val(), k))
