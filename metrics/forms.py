from django import forms

class QualityMetricsForm(forms.Form):
    url = forms.URLField(label='URL', required=True)

class PerformanceMetricsForm(forms.Form):
    url_quality = forms.URLField(label='URL', required=True)
