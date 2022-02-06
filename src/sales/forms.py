from django import forms

class SalesSearchForm(forms.Form):
    CHART_TYPE = (
        ('#1', 'Bar Chart'),
        ('#2', 'Pie Chart'),
        ('#3', 'Line Chart'),
    )

    RESULT_TYPE = (
        ('#1', 'transaction'),
        ('#2', 'sales date'),
    )

    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_TYPE)
    result_by = forms.ChoiceField(choices=RESULT_TYPE)

    