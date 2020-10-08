from django import forms


class NewComment(forms.Form):
    new_comment_title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'class': 'form-control'}))
    new_comment_body = forms.CharField(label='Comment', widget=forms.Textarea(
        attrs={'width': '60%', 'col': '50', 'rows': '100', 'class': 'form-control'}))
