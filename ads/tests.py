from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='Books',
            condition='new'
        )

    def test_ad_creation(self):
        ad = Ad.objects.get(id=self.ad.id)
        self.assertEqual(ad.title, 'Test Ad')
        self.assertEqual(ad.user.username, 'testuser')

    def test_ad_search(self):
        ads = Ad.objects.filter(title__icontains='Test')
        self.assertEqual(ads.count(), 1)

class ProposalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.ad1 = Ad.objects.create(user=self.user1, title='Ad 1', description='Desc', category='Books', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad 2', description='Desc', category='Electronics', condition='used')

    def test_proposal_creation(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Interested!')
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender.title, 'Ad 1')