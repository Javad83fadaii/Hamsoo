"""فرم‌های سایت."""

from django import forms

from .models import AdvocacySubmission


class AdvocacySubmissionForm(forms.ModelForm):
    """فرم ثبت مطالبه در صفحه مطالبه‌گری."""

    class Meta:
        model = AdvocacySubmission
        fields = ('institution', 'subject', 'description', 'contact')
        labels = {
            'institution': 'نام یا عنوان نهاد مربوطه',
            'subject': 'موضوع مطالبه',
            'description': 'شرح دقیق مسئله',
            'contact': 'شماره تماس یا ایمیل (اختیاری جهت پیگیری)',
        }
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'مثال: معاونت دانشجویی / سازمان آب منطقه',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'عنوان خلاصه مطالبه',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-field',
                'rows': 4,
                'placeholder': 'توضیحات، اسناد یا مستندات را شرح دهید...',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': '۰۹...',
            }),
        }
