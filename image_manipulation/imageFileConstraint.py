from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class RestrictedImageField(forms.ImageField):
  """
  content_types : ['application/pdf', 'image/jpeg']
  max_upload_size : size in bytes of max acceptable size

  ex:
  class ExForm(forms.Form):
    db_image = RestrictedImageField(content_types = ['image/png'], max_upload_size='2621440')
  """
  
  def getPillowSupportedImageTypes():
    return ["image/jpeg", "image/png", "image/gif", "image/tif", "image/x-tiff", "image/bmp"]

  def getBytesFromMegaBytes(mb):
    return 1024 * 1024 * mb


  def __init__(self, *args, **kwargs):
    self.contentTypes = kwargs.pop("content_types")
    self.maxUploadSize = kwargs.pop("max_upload_size")

    super(RestrictedImageField, self).__init__(*args, **kwargs)

  def clean(self, data, initial=None):
    file = super(RestrictedImageField, self).clean(data, initial)

    try:
      contentType = file.content_type
      if contentType in self.contentTypes:
        if file._size > self.maxUploadSize:
          raise ValidationError(_('Please keep file size under %s. The file\'s size was %s') % (filesizeformat(self.maxUploadSize), filesizeformat(file._size)) )
      else:
        raise ValidationError(_('That file type is not supported.') )
    except AttributeError:
        pass

    return data
