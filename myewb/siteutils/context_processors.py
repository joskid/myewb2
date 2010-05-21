import settings
from group_topics.models import GroupTopic

def myewb_settings(request):
    gt = GroupTopic.objects.all().order_by('-last_reply')[:1]
    
    grandfathered = False
    if request.user.is_authenticated():
        grandfathered = request.user.get_profile().grandfathered
        request.user.get_profile().grandfathered = False
        request.user.get_profile().messages_as_emails = True
        request.user.get_profile().save()
    
    return {'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
            'LATEST_POST': gt[0].last_reply,
            'grandfathered': grandfathered}
    