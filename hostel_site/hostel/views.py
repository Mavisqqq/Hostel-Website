from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView
from hostel_site.forms import *
from hostel.models import *
from hostel.token import account_activation_token
from hostel_site.forms import UserRegisterForm, UserForgotPasswordForm, UserSetNewPasswordForm, UserLoginForm


def index(request):
    news_sorted = News.objects.all().order_by('-created_at')
    context = {
        'news_sorted': news_sorted,
    }
    return render(request, 'hostel/index.html', context)


def about_us(request):
    return render(request, 'hostel/about_us.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации аккаунта'
            message = render_to_string('hostel/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, "Ссылка для активации аккаунта была отправлена на ваш email")
            return redirect('Home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'hostel/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Регистрация завершена успешно!")
        return redirect('Home')
    else:
        messages.error(request, 'Ошибка регистрации')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Home')
    else:
        form = UserLoginForm()
    return render(request, 'hostel/login.html', {"form": form})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    #Представление по сбросу пароля по почте
    form_class = UserForgotPasswordForm
    template_name = 'hostel/password_change_request.html'
    success_url = reverse_lazy('Home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    email_template_name = 'hostel/password_change_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    #Представление установки нового пароля
    form_class = UserSetNewPasswordForm
    template_name = 'hostel/password_changing.html'
    success_url = reverse_lazy('Home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


def user_logout(request):
    logout(request)
    return redirect('Home')


@login_required(login_url='/login/', redirect_field_name="login")
def blockAuthenticated(request, slug):
    block = get_object_or_404(Block, slug=slug)
    if request.user in block.user.all():
        block_title = block.title
        context = {
            'block_title': block_title,
        }
        return render(request, 'hostel/blockAuthenticated.html', context)
    else:
        raise Http404


def leave_block(request, slug):
    block = get_object_or_404(Block, slug=slug)
    block.user.remove(request.user)
    return redirect('Home')


class BlockChatView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Block
    template_name = 'hostel/block_chat.html'

    def get(self, request, *args, **kwargs):
        block = self.get_object()
        if request.user in block.user.all():
            block_messages = block.blockmessages_set.all()
            paginator = Paginator(block_messages, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context = {
                "page_obj": page_obj,
            }
            return render(request, 'hostel/block_chat.html', context=context)
        else:
            raise Http404

    def post(self, request, slug):
        block = get_object_or_404(Block, slug=slug)
        if request.POST['text'] != '':
            message = BlockMessages(date_added=datetime.Now, user=request.user, text=request.POST['text'], block=block)
            message.save()
        return render(request, 'hostel/block_chat.html')


@login_required(login_url='/login/', redirect_field_name="login")
def get_block_messages(request, slug):
    block = get_object_or_404(Block, slug=slug)
    if request.user in block.user.all():
        block_messages = block.blockmessages_set.all()
        paginator = Paginator(block_messages, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
        }
        return render(request, 'hostel/get_block_messages_template.html', context)
    else:
        raise Http404


@login_required(login_url='/login/', redirect_field_name="login")
def blockDuty(request, slug):
    block = get_object_or_404(Block, slug=slug)
    if request.user in block.user.all():
        duties = block.duty_set.all()
        paginator = Paginator(duties, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'hostel/block_duty.html', context)
    else:
        raise Http404


@login_required(login_url='/login/', redirect_field_name="login")
def addDuty(request, slug):
    block = get_object_or_404(Block, slug=slug)
    if request.user in block.user.all():
        if request.method == 'POST':
            form = DutyForm(request.POST)
            if form.is_valid():
                images = request.FILES.getlist('images')
                form = form.save(commit=False)
                form.sending_user = request.user
                form.block = block
                form.save()
                for image in images:
                    ImageDuty.objects.create(duty=form, image=image)
                return redirect('block_duty', str(slug))
            else:
                messages.error(request, 'Ошибка')
        else:
            form = DutyForm()
        return render(request, 'hostel/add_duty.html', {'form': form})
    else:
        raise Http404


class BlockUnauthenticated(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    template_name = 'hostel/blockUnauthenticated.html'
    context_object_name = 'block_number'

    def get_queryset(self):
        return Block.objects.filter(title__icontains=self.request.GET.get('s', default=""))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def addUserToBlock(request):
    block_num = request.GET.get("s")
    blocks = Block.objects.all()
    k = 0
    for block in blocks:
        if request.user in block.user.all():
            messages.error(request, 'Вы уже присоединились к другому блоку')
            return render(request, 'hostel/blockUnauthenticated.html')
    for block in blocks:
        if block.title == block_num:
            block.user.add(request.user)
            k += 1
            return redirect('blockAuthenticated', str(block_num))
    if k == 0:
        messages.error(request, 'Такого блока не существует. Введите номер ещё раз.')
        return render(request, 'hostel/blockUnauthenticated.html')


def ads(request):
    ads_list = Ads.objects.all()
    paginator = Paginator(ads_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, 'hostel/ads.html', context=context)


class ViewAds(DetailView):
    model = Ads
    template_name = 'hostel/view_ad.html'

    def get(self, request, *args, **kwargs):
        ads = self.get_object()
        ads_comments = ads.commentads_set.all()
        paginator = Paginator(ads_comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        ads.views += 1
        ads.save()
        ads_item = Ads.objects.filter(pk=self.kwargs['pk'])
        return render(request, 'hostel/view_ad.html', {"ads_item": ads_item, "page_obj": page_obj})

    def post(self, request, pk):
        ads = get_object_or_404(Ads, pk=pk)
        if request.POST['text'] != '':
            comment = CommentAds(date_added=datetime.Now, user=request.user, text=request.POST['text'], ads=ads)
            comment.save()
        return render(request, 'hostel/view_ad.html')


@login_required(login_url='/login/', redirect_field_name="login")
def get_ads_comments(request, pk):
    ads = get_object_or_404(Ads, pk=pk)
    ads_comments = ads.commentads_set.all()
    paginator = Paginator(ads_comments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'hostel/get_ads_comments_template.html', context)


@login_required(login_url='/login/', redirect_field_name="login")
def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            images = request.FILES.getlist('images')
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            for image in images:
                ImageAd.objects.create(ad=form, image=image)
            return redirect('ads')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = AdForm()
    return render(request, 'hostel/add_ad.html', {'form': form})


class GeneralChatView(DetailView):
    template_name = 'hostel/general_chat.html'

    def get(self, request, *args, **kwargs):
        chat_items = GeneralChatMessages.objects.all()
        paginator = Paginator(chat_items, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
        }
        return render(request, 'hostel/general_chat.html', context=context)

    def post(self, request):
        if request.POST['text'] != '':
            message = GeneralChatMessages(date_added=datetime.Now, user=request.user, text=request.POST['text'])
            message.save()
        return render(request, 'hostel/general_chat.html')


@login_required(login_url='/login/', redirect_field_name="login")
def get_general_chat_messages(request):
    general_chat_messages = GeneralChatMessages.objects.all()
    paginator = Paginator(general_chat_messages, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'hostel/get_general_chat_messages_template.html', context)


def news(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, 'hostel/news.html', context=context)


class ViewNews(DetailView):
    model = News
    template_name = 'hostel/view_news.html'

    def get(self, request, *args, **kwargs):
        news = self.get_object()
        news_comments = news.commentnews_set.all()
        paginator = Paginator(news_comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        news.views += 1
        news.save()
        news_item = News.objects.filter(pk=self.kwargs['pk'])
        return render(request, 'hostel/view_news.html', {"news_item": news_item, "page_obj": page_obj})

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        if request.POST['text'] != '':
            comment = CommentNews(date_added=datetime.Now, user=request.user, text=request.POST['text'], news=news)
            comment.save()
        return render(request, 'hostel/view_news.html')


@login_required(login_url='/login/', redirect_field_name="login")
def get_news_comments(request, pk):
    news = get_object_or_404(News, pk=pk)
    news_comments = news.commentnews_set.all()
    paginator = Paginator(news_comments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'hostel/get_news_comments_template.html', context)


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        news = News.objects.get(pk=pk)
        news.views -= 1
        news.save()

        is_dislike = False
        for dislike in news.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            news.dislikes.remove(request.user)

        is_like = False
        for like in news.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            news.likes.add(request.user)
        if is_like:
            news.likes.remove(request.user)
        return HttpResponseRedirect(reverse('view_news', args=[int(pk)]))


class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        news = News.objects.get(pk=pk)
        news.views -= 1
        news.save()

        is_like = False
        for like in news.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            news.likes.remove(request.user)

        is_dislike = False
        for dislike in news.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            news.dislikes.add(request.user)
        if is_dislike:
            news.dislikes.remove(request.user)
        return HttpResponseRedirect(reverse('view_news', args=[int(pk)]))


@login_required(login_url='/login/', redirect_field_name="login")
def get_news_footer(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    context = {
        'news_item': news_item,
    }
    return render(request, 'hostel/get_news_footer_template.html', context)


def add_news(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                images = request.FILES.getlist('images')
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                for image in images:
                    ImageNews.objects.create(news=form, image=image)
                return redirect('news')
            else:
                messages.error(request, 'Ошибка')
        else:
            form = NewsForm()
        return render(request, 'hostel/add_news.html', {'form': form})
    else:
        raise Http404
