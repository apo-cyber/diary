from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import InquiryForm, DiaryCreateForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Diary
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)

# Create your views here.
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        diary = get_object_or_404(Diary, pk=self.kwargs['pk'])
        return self.request.user == diary.user


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

class DiaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary
    context_object_name='diary_list' # テンプレート内で使用する変数名を変更する場合 # デフォルトはobject_list
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin, OnlyYouMixin ,DetailView):
    template_name = 'diary_detail.html'
    model = Diary
    # pk_url_kwarg = 'id' # URLパラメータ名を変更する場合
    # slug_field = 'title' # URLパラメータ名を変更する場合 # pathは'detail/<str:title>/'のようにする
    # slug_url_kwarg = 'title' # URLパラメータ名を変更する場合
    # context_object_name = 'diary' # テンプレート内で使用する変数名を変更する場合

class DiaryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'diary_create.html'
    model = Diary
    form_class=DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'diary_update.html'
    model = Diary
    form_class=DiaryCreateForm

    def get_success_url(self):
        diary_pk = self.kwargs['pk']
        url = reverse_lazy('diary:diary_detail', kwargs={'pk': diary_pk})
        return url

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の更新に失敗しました。')
        return super().form_invalid(form)

# class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
#     model = Diary
#     template_name = 'diary_delete.html'
#     success_url = reverse_lazy('diary:diary_list')

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, "日記を削除しました。")
#         return super().delete(request, *args, **kwargs)

class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    template_name = 'diary_delete.html'
    model = Diary
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '日記を削除しました。')
        return response
