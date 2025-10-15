from django import forms
from .models import Blog
from froala_editor.widgets import FroalaEditor


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ("author", "publish_date", "slug", )

        widgets = {
            'body': FroalaEditor(options={
                # 'toolbarInline': True,
                'heightMin': 200,
                'heightMax': 400,
                'placeholderText': 'Write your content here...',
            }),
        }
