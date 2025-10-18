from django import forms
from .models import Blog, Comment
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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Input your comment here',
                    'rows': 5,
                    'cols': 80,
                }
            )

        }
