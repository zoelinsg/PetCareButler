from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["pet", "name", "category", "amount", "date", "notes"]
        labels = {
            "pet": "寵物（可不選）",
            "name": "項目",
            "category": "類別",
            "amount": "金額",
            "date": "日期",
            "notes": "備註",
        }
        
        widgets = {
            "pet": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "category": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "amount": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": "0", "step": "0.01"}),
            "date": forms.DateInput(attrs={"class": "form-control form-control-sm", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3}),
        }

    def clean_amount(self):
        amt = self.cleaned_data["amount"]
        if amt is None:
            return amt
        if amt < 0:
            raise forms.ValidationError("金額不可為負數")
        return amt


class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}), required=False, label="開始日期")
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}), required=False, label="結束日期")
