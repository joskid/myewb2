from django.db import models
from django.db.models.signals import post_save

from django.utils.translation import ugettext_lazy as _

from profiles.models import MemberProfile
from networks.models import Network
from avatar.templatetags.avatar_tags import avatar_url
from conference.models import ConferenceRegistration

# Create your models here.

class ConferenceInterest(models.Model):
    """
    A topic of interest for members of conference.
    """
    name = models.CharField(_("Interest Name"), max_length=255)
    description = models.TextField(_("Interest Description"))

    def __unicode__(self):
        return self.name


class ConferenceProfile(models.Model):
    """
    An additional set of information tied to a MyEWB user specifically
    for the conference community website.
    """
    member_profile = models.ForeignKey(MemberProfile, unique=True, verbose_name=_('member profile this profile is linked to.'))
    registered = models.BooleanField(_('registered for conference 2011'), default=False)
    # additional personal information
    what_now = models.TextField(_("What you are doing now."), default="Edit me! What are you doing? Where are you living?")
    # additional information we want for conference.
    interests = models.ManyToManyField(ConferenceInterest, related_name='interested_users', verbose_name=_('List of interests.'), blank=True)
    conference_question = models.TextField(_("One question you want to answer at conference."), default="Add your question here!")
    conference_goals = models.TextField(_("Your goals for conference."), default="My goals for conference are...")
    active = models.BooleanField(default=False)

    @property
    def avatar_url(self):
        return avatar_url(self.member_profile.user, 160)

    @property
    def username(self):
        return self.member_profile.user.username
    @property
    def cohorts(self):
        return self.member_profile.cohort_set.all()

CHAPTER_CHOICES = []
chapterlist = Network.objects.filter(chapter_info__isnull=False, is_active=True).order_by('name')
for chapter in chapterlist:
    CHAPTER_CHOICES.append((chapter.slug, chapter.chapter_info.chapter_name))

CHAPTER_CHOICES = (
    ('carleton', 'Carleton',),
    ('concordia', 'Concordia',),
    ('dal', 'Dalhousie',),
    ('uoguelph', 'Guelph',),
    ('laval', 'Laval',),
    ('mcmaster', 'McMaster',),
    ('mcgill', 'McGill ',),
    ('mun', 'MUN',),
    ('polymtl', 'Polytechnique',),
    ('queensu', 'Queen\'s',),
    ('uregina', 'U of R',),
    ('ryerson', 'Ryerson',),
    ('sfu', 'SFU',),
    ('usherbrooke', 'Sherbrooke',),
    ('ubc', 'UBC',),
    ('unb', 'UNB',),
    ('ualberta', 'U of A',),
    ('ucalgary', 'U of C',),
    ('umanitoba', 'U of M',),
    ('utoronto', 'U of T',),
    ('uoit', 'UoIT',),
    ('uottawa', 'U of O',),
    ('usask', 'U of S',),
    ('uvic', 'UVic',),
    ('uwaterloo', 'Waterloo',),
    ('uwo', 'Western',),
    ('uwindsor', 'Windsor',),
    ('vancouver', 'Vancouver',),
    ('calgary', 'Calgary',),
    ('edmonton', 'Edmonton',),
    ('saskatoon', 'Saskatoon',),
    ('winnipeg', 'Winnipeg',),
    ('grandriver', 'Grand River',),
    ('toronto', 'Toronto',),
    ('ottawa', 'Ottawa',),
    ('montreal', 'Montreal',),
    )
DICT_CHAPTER_CHOICES = dict(CHAPTER_CHOICES)
ROLE_CHOICES = (
        ('m', 'Member',),
        ('e', 'Executive',),
        ('p', 'President',),
        ('j', 'JF/Op 21',),
        ('f', 'ProF',),
        ('s', 'APS/OVS',),
        )

class Cohort(models.Model):
    """
    A definition of a Cohort of people we are looking at.
    """
    chapter = models.CharField(max_length=20, choices=CHAPTER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='m')
    year = models.PositiveIntegerField(default=2005)
    members = models.ManyToManyField(MemberProfile)

    def __unicode__(self):
        if self.role in ['m', 'e', 'p']:
            return '%s of %s in %d/%d' % (self.get_role_display(), DICT_CHAPTER_CHOICES[self.chapter], self.year, self.year + 1)
        else:
            return '%s %d' % (self.get_role_display(), self.year)
    @property
    def display(self):
        return str(self)

    @property
    def relevant_properties(self):
        if self.role in ['m', 'e', 'p']:
            return ['chapter', 'role', 'year']
        else:
            return ['role', 'year']



CANADA_ROLE_CHOICES = (
        ('m', 'Member',),
        ('e', 'Executive',),
        ('p', 'President',),
        )
class CanadaCohort(models.Model):
    """
    A definition of a Cohort of people that we are looking at.
    """
    chapter = models.CharField(max_length=40,choices=CHAPTER_CHOICES)
    role = models.CharField(max_length=1, choices=CANADA_ROLE_CHOICES)
    year = models.PositiveIntegerField()
    members = models.ManyToManyField(MemberProfile)

AFRICA_ROLE_CHOICES = (
        ('j', 'JF/Op 21',),
        ('p', 'ProF',),
        ('s', 'APS/OVS',),
        )
AFRICA_COUNTRY_CHOICES = (
        ('bf', 'Burkina Faso',),
        ('gh', 'Ghana',),
        ('mw', 'Malawi',),
        ('zm', 'Zambia',),
        ('ml', 'Mali',),
        ('ph', 'Philippines',),
        ('tz', 'Tanzania',),
        ('cm', 'Cameroon',),
        ('kh', 'Cambodia',),
        )
class AfricaCohort(models.Model):
    """
    A definition of a Cohort in terms of Africa.
    """
    country = models.CharField(_('Country'), max_length=2, choices=AFRICA_COUNTRY_CHOICES) # Ghana, Burkina, etc.
    role = models.CharField(_('Role'), max_length=1, choices=AFRICA_ROLE_CHOICES) # APS/OVS, JF/OP21, ProF
    year = models.PositiveIntegerField()
    members = models.ManyToManyField(MemberProfile)

class ConferenceInvitation(models.Model):
    """
    Keep track of invitations that are sent and clicked on.
    """
    sender = models.ForeignKey(MemberProfile, related_name='sent_conference_invitations')
    receiver = models.ForeignKey(MemberProfile, related_name='received_conference_invitations')
    code = models.CharField(max_length=12)
    activated = models.BooleanField()

def update_registered_status(sender, **kwargs):
    try:
        cp = ConferenceProfile.objects.get(member_profile__user=instance.user)
        if instance.user.conference_registrations.filter(cancelled=False).count() > 0:
            if not cp.registered:
                cp.registered = True
                cp.save()
        else:
            if cp.registered:
                cp.registered = False
                cp.save()
    except:
        pass
post_save.connect(update_registered_status, sender=ConferenceRegistration)
