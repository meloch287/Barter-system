from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Создать объявление'})

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'title': 'Редактировать объявление'})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

def ad_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')

    ads = Ad.objects.all()
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'condition': condition,
    })

@login_required
def create_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        ad_sender_id = request.POST.get('ad_sender_id')
        comment = request.POST.get('comment')
        ad_sender = get_object_or_404(Ad, id=ad_sender_id, user=request.user)
        if ad_sender == ad_receiver:
            return render(request, 'ads/proposal_form.html', {
                'ad_receiver': ad_receiver,
                'user_ads': Ad.objects.filter(user=request.user),
                'error': 'Нельзя предложить обмен на свое же объявление'
            })
        ExchangeProposal.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment
        )
        return redirect('proposal_list')
    user_ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/proposal_form.html', {'ad_receiver': ad_receiver, 'user_ads': user_ads})

@login_required
def proposal_list(request):
    sent_proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    received_proposals = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    return render(request, 'ads/proposal_list.html', {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
    })

@login_required
def update_proposal_status(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['accepted', 'rejected']:
            proposal.status = status
            proposal.save()
        return redirect('proposal_list')
    return render(request, 'ads/proposal_list.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        # перекидываем GET в post, чтобы логаут происходил
        return self.post(request, *args, **kwargs)