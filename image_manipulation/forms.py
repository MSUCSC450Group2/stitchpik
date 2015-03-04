from django import forms
from .models import Image

# Inherrit main Image model
class ManipulateImageForm(forms.Form):
    GUAGE_SIZES = ( ('0', '1" 25.0mm',), ('1', '7/8" 22.0mm',), ('2', '3/4" 19.0mm',),
        ('3', '5/8" 16.0mm',), ('4', '9/16" 14.0mm',), ('5', '1/2" 12.7mm',), ('6', '7/16" 11.0mm',),
        ('7', '3/8" 9-10mm',), ('8', '1/3" 8.25mm',), ('9', '1/4" 6-6.5mm',),
        ('10', '3/16" 5.0mm',), ('11', '5/32" 4.0mm',), ('12', '1/8" 3.2mm',),
        ('13', '3/32" 2.4mm',), ('14', '5/64" 2.0mm',), ('15', '1/16" 1.6mm',),
        ('16', '3/64" 1.2mm',), ('17', '5/128" 1.0mm',), ('19', '1/32" 0.88mm',)
    )

    KNIT_TYPES = (
        ('0', 'Knitting',), ('1', 'Crochetting',), ('2', 'Cross-Stitching',)
    )

    # 
    numberOfColors = forms.IntegerField(max_value=32, min_value=2, label='Number of Colors', initial='8')

    # 
    guageSize = forms.ChoiceField(choices=GUAGE_SIZES, label="Guage Size", initial='8')

    # in inches
    canvasLength = forms.DecimalField(label="Canvas Length (in)")

    # in inches
    canvasWidth = forms.DecimalField(label="Canvas Width (in)")

    knitType = forms.ChoiceField(widget=forms.RadioSelect, choices=KNIT_TYPES, label="Knit Type", initial="0")
    
    
