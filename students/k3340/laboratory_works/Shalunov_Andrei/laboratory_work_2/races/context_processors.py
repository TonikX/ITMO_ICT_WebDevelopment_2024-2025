def has_racer_profile(request):
    return {
        'has_racer_profile': hasattr(request.user, 'racer') if request.user.is_authenticated else False
    }