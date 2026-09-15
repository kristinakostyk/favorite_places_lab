from django import forms


class PlaceForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Назва",
    )

    description = forms.CharField(
        widget=forms.Textarea,
        label="Опис",
    )

    place_type = forms.CharField(
        max_length=50,
        label="Тип місця",
    )

    location = forms.CharField(
        max_length=100,
        required=False,
        label="Локація",
    )

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label="Рейтинг",
    )