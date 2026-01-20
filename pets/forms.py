from django import forms
from .models import Pets

class PetsForm(forms.ModelForm):
    class Meta:
        model = Pets
        fields = [
            "name",
            "species",
            "gender",
            "breed",
            "pet_chip",
            "birth_date",
            "features",
            "remark",
            "avatar",
            "is_neutered",
            "is_deceased",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "features": forms.Textarea(attrs={"rows": 3}),
            "remark": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not (self.instance and self.instance.pk):
            self.fields["is_deceased"].widget = forms.HiddenInput()
            self.fields["is_deceased"].initial = False

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.FileInput):
                widget.attrs["class"] = "form-control"
            else:
                widget.attrs["class"] = "form-control"
