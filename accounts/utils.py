from django.contrib.auth import get_user_model
from .models import UserProfile


def profile_for(user):
    return getattr(user, 'profile', None)


def role_for(user):
    if user.is_superuser:
        return UserProfile.Role.ADMIN
    profile = profile_for(user)
    return profile.role if profile else UserProfile.Role.EMPLOYEE


def is_viewer(user):
    return role_for(user) == UserProfile.Role.VIEWER


def visible_users(user):
    User = get_user_model()
    role = role_for(user)
    profile = profile_for(user)
    if role == UserProfile.Role.ADMIN:
        return User.objects.all()
    if not profile:
        return User.objects.filter(pk=user.pk)
    if role == UserProfile.Role.DIRECTOR:
        return User.objects.filter(profile__department=profile.department)
    if role == UserProfile.Role.SECTION_HEAD:
        return User.objects.filter(profile__department=profile.department, profile__section=profile.section)
    return User.objects.filter(pk=user.pk)


def restrict_queryset(queryset, user):
    return queryset.filter(user__in=visible_users(user))
