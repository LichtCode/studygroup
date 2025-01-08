from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Group, Topic
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from users.models import Tag, CustomUser
from studysession.models import StudySession

@login_required
def user_dashboard(request):    
    sessions = request.user.sessions.all()
    user_topics = request.user.interested_topics.all()

    user = request.user
    user_tags = user.tags.all()
    matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()
    groups = user.study_groups.all()
    for match in matches:
        print(match.username, match.id)
    context = {
        "sessions": sessions,
        "user_tags": user_tags,
        "user_topics": user_topics,
        "user": user,
        "matches": matches,
        'groups': groups
    }
    return render(request, 'studyroom/dashboard.html', context)


@login_required
def topics_list(request):
    user_topics = request.user.interested_topics.all()
    tags = Tag.objects.all()

    context = {
        "user_topics": user_topics,
        "tags": tags,
    }
    return render(request, 'studyroom/topics.html', context)


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
def groups_list(request):
    user_groups = request.user.study_groups.all()
    tags = Tag.objects.all()

    context = {
        "user_groups": user_groups,
        "tags": tags,
    }
    return render(request, 'studyroom/groups.html', context)

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        tags_input = request.POST.get('tags', '')

        print(name, description, tags_input)

        if not name:
            return JsonResponse({'error': 'Group name is required.'}, status=400)

        # Check if group with the same name exists
        if Group.objects.filter(name=name).exists():
            return JsonResponse({'error': 'A group with this name already exists.'}, status=400)

        try:

            # Create group
            group = Group.objects.create(
                name=name,
                description=description,
                owner=request.user
            )
            group.add_member_to_group(request.user)
            # Add tags if provided
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    group.tags.add(tag)

            return JsonResponse({
                'message': 'Group created successfully!',
                'name': group.name,
                'description': group.description,
                'group_id': group.id
            }, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)

@login_required
def group_detail(request, group_id):
    """
    Renders the group details page.
    """
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'studyroom/group_detail.html', {'group': group})

@login_required
def search_group(request):
    query = request.GET.get('q', '')
    groups = Group.objects.filter(Q(name__icontains=query) | Q(group_id__icontains=query))

    if request.method == 'GET':
        html = render_to_string('studyroom/search_results.html', {'groups': groups})
        return JsonResponse({'html': html})

@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(group_id=group_id)
            group.add_member_to_group(request.user)  # Add the current user to the group
            return JsonResponse({
                'message': 'You have successfully joined the group!',
                'name': group.name,
                'members': group.members.count(),
                'group_id': group.id})
        except Group.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)
