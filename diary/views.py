from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from .forms import InquiryForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class InquiryView(FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ：{}'.format(title)
        message_body = '送信者名:{0}\nメールアドレス:{1}\nタイトル:{2}\nメッセージ:{3}'.format(name, email, title, message)

        try:
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER]

            message = EmailMessage(subject=subject, body=message_body, from_email=from_email, to=to_list)
            message.send()

            messages.success(self.request, 'お問い合わせは正常に送信されました。')
        except Exception as e:
            messages.error(self.request, 'メール送信に失敗しました: {}'.format(e))

        return super().form_valid(form)

class diaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries
