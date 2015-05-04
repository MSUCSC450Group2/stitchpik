from django import forms
from .models import Image
from .imageFileConstraint import RestrictedImageField

class ImageUploadForm(forms.Form):
    imgFile = RestrictedImageField(content_types=RestrictedImageField.getPillowSupportedImageTypes(), max_upload_size=RestrictedImageField.getBytesFromMegaBytes(1))


class ManipulateImageForm(forms.Form):
  KNIT_TYPES = (
      ('0', 'Knitting',), ('1', 'Crochetting',), ('2', 'Cross-Stitching',)
  )
  DO_KMEANS = (
      ('0', 'Pick for me'), ('1', 'Let me decide')
  )

  numberOfColors = forms.IntegerField(max_value=32, min_value=2, 
                                        label='Number of Colors', initial='8')
  gaugeSize = forms.DecimalField(label="Guage Size", initial='10', decimal_places=2)
  canvasLength = forms.DecimalField(label="Canvas Length (in)", initial='12', decimal_places=2, min_value=0.01)
  canvasWidth = forms.DecimalField(label="Canvas Width (in)", initial='12', decimal_places=2, min_value=0.01)
  knitType = forms.ChoiceField(widget=forms.RadioSelect, choices=KNIT_TYPES, 
                                 label="Knit Type", initial="0")
  colorSelect = forms.ChoiceField(widget=forms.RadioSelect, choices=DO_KMEANS, label="Select Colors", initial="0", required=False)
  colorList = forms.CharField(label="Color List", required=False)
    
