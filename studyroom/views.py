from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Group, Topic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from users.models import Tag, CustomUser
from studysession.models import StudySession

@login_required
def user_dashboard(request):

    tags = Tag.objects.all()
    sessions = request.user.sessions.all()
    user_topics = request.user.interested_topics.all()

    user = request.user
    user_tags = user.tags.all()
    matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()
    groups = Group.objects.filter(members=user)
    context = {
        "sessions": sessions,
        "tags": tags,
        "user_topics": user_topics,
        "user": user,
        "matches": matches,
        'groups': groups
    }
    return render(request, 'studyroom/dashboard.html', context)

@csrf_exempt
def create_topic(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        tags = request.POST.get('tags', '')

        if not name or not description:
            return JsonResponse({'error': 'Name and Description are required.'}, status=400)

        topic, created = Topic.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )

        tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            topic.tags.add(tag)

        topic.interested_users.add(request.user)

        return JsonResponse({
            'name': topic.name,
            'description': topic.description,
            'tags': [tag.name for tag in topic.tags.all()]
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required
def select_topics(request):
    if request.method == "POST":
        selected_tags = request.POST.getlist("tags")
        user = request.user

        user.tags.clear()
        user.tags.add(*selected_tags)

        return JsonResponse({"message": "Topics updated successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def find_matches(request):
    user = request.user
    user_tags = user.tags.all()
    matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()

    return render(request, "studyroom/matches.html", {"matches": matches})

@login_required
def group_detail(request, group_id):
    """
    Renders the group details page.
    """
    group = get_object_or_404(Group, group_id=group_id)
    return render(request, 'group_detail.html', {'group': group})

@login_required
def search_group(request):
    query = request.GET.get('q', '')
    groups = Group.objects.filter(Q(name__icontains=query) | Q(group_id__icontains=query))

    if request.is_ajax():
        html = render_to_string('studyroom/search_results.html', {'groups': groups})
        return JsonResponse({'html': html})
    
    return render(request, 'studyroom/search_group.html')

@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(group_id=group_id)
            group.add_member_to_group(request.user)  # Add the current user to the group
            return JsonResponse({'message': 'You have successfully joined the group!'})
        except Group.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)
