from django import forms
from .models import DailyRecord


class DailyRecordForm(forms.ModelForm):
    supplements_choices = forms.MultipleChoiceField(
        choices=DailyRecord.SUPPLEMENT_CHOICES,
        required=False,
        label="營養品(可複選)",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = DailyRecord
        fields = [
            "pet",
            "recorded_at",         
            "weight_kg",
            "water_ml",
            "food_g",
            "supplements_choices",
            "mood",
            "poop_and_pee_count",   
            "poop_status",
            "exercise_min",
            "medications",
            "note",
        ]
        widgets = {
            "recorded_at": forms.DateInput(attrs={"type": "date"}), 
            "note": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.supplements:
            self.fields["supplements_choices"].initial = [
                s for s in self.instance.supplements.split(",") if s
            ]

        for name, field in self.fields.items():
            input_type = getattr(field.widget, "input_type", "")
            if input_type in ("checkbox", "radio"):
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()

        for name in ("pet", "mood", "poop_status"):
            if name in self.fields:
                self.fields[name].widget.attrs["class"] = "form-select"

    def save(self, commit=True):
        obj = super().save(commit=False)
        selected = self.cleaned_data.get("supplements_choices") or []
        obj.supplements = ",".join(selected)

        if commit:
            obj.save()
        return obj
