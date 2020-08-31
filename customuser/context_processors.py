def check_profile(request):
    if request.user.is_authenticated:
        user = request.user
        allMessages = user.message_set.all()
        msgCount = allMessages.filter(is_viewed = False).count






    return locals()

