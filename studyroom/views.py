from django.shortcuts import render, get_object_or_404, redirect
import datetime
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
    sessions = request.user.sessions.all()
    user_topics = request.user.interested_topics.all()
    tags = Tag.objects.all()
    user = request.user
    user_tags = user.tags.all()
    matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()
    topic_matches = Topic.objects.filter(tags__in=user_tags).exclude(interested_users=request.user).distinct()
    groups = user.study_groups.all()
    user_chatrooms = request.user.chatrooms.all()

    context = {
        "sessions": sessions[:5],
        "user_tags": user_tags,
        "user_topics": user_topics[:5],
        "user": user,
        "matches": matches[:5],
        'groups': groups[:5],
        'suggested_topics': topic_matches[:5],
        "tags": tags,
        "user_chatrooms": user_chatrooms[:5] 
    }
    return render(request, 'studyroom/dashboard.html', context)

def landing_page(request):
    # #general
    # user = request.user
    # user_topics = request.user.interested_topics.all() # dashboard topics
    # user_tags = user.tags.all() # dashboard topic
    # tags = Tag.objects.all() # groups topic
    # # dashboard
    
    # matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()
    # groups = user.study_groups.all()

    # #Groups
    # user_groups = request.user.study_groups.all()

    # #topic
    # topics = Topic.objects.all()
    # topic_matches = Topic.objects.filter(tags__in=user_tags).distinct()

    # #notification
    # user_notifications = request.user.notifications.filter(is_read=False)

    # #sessions
    # sessions = request.user.sessions.all()

    # context = {
    #     "user_groups": user_groups,
    #     "sessions": sessions,
    #     "user_tags": user_tags,
    #     "user_topics": user_topics,
    #     "user": user,
    #     "matches": matches,
    #     'groups': groups,
    #     "tags": tags,
    #     "topics": topics,
    #     "suggested_topics": topic_matches,
    #     "notifications": user_notifications,
    # }
    return render(request, 'studyroom/landing-page.html')

@login_required
def topics_list(request):
    user_topics = request.user.interested_topics.all()
    topics = Topic.objects.all().exclude(interested_users=request.user).distinct()
    topics = topics.order_by('-created_at')
    tags = Tag.objects.all()
    user_tags = request.user.tags.all()
    topic_matches = Topic.objects.filter(tags__in=user_tags).exclude(interested_users=request.user).distinct()

    context = {
        "user_topics": user_topics[:5],
        "tags": tags,
        "topics": topics[:5],
        "suggested_topics": topic_matches[:5],
    }
    return render(request, 'studyroom/topics.html', context)


@csrf_exempt
def create_topic(request):
    print("Create topic got CLICKED")
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
            'tags': [tag.name for tag in topic.tags.all()],
            'topic_id': topic.id
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required
def select_topics(request):
    if request.method == "POST":
        selected_tags = request.POST.getlist("tags[]")

        # Process the selected tags (e.g., save to the database)
        print("Selected Tags:", selected_tags)
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
        group_id = request.POST.get('topic_id')
        try:
            group = Group.objects.get(id=group_id)
            group.add_member_to_group(request.user)  # Add the current user to the group
            return JsonResponse({
                'message': 'You have successfully joined the group!',
                'name': group.name,
                'members': group.members.count(),
                'group_id': group.id})
        except Group.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)

@login_required
def add_topic(request):
    print("_______ADD TOPIC________")
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        try:
            topic = Topic.objects.get(id=topic_id)
            print("How are you", topic)
            topic.interested_users.add(request.user)
            return JsonResponse({
                'message': 'You have successfully added the topic!',
                'name': topic.name,
                'description': topic.description,
                'members': topic.interested_users.count(),
                'topic_id': topic.id})
        except Topic.DoesNotExist:
            return JsonResponse({'message': 'topic not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)

@login_required
def remove_topic(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.interested_users.remove(request.user)
            return JsonResponse({
                'message': 'You have successfully remove the topic!',
                'name': topic.name,
                'description': topic.description,
                'members': topic.interested_users.count(),
                'topic_id': topic.id})
        except Topic.DoesNotExist:
            return JsonResponse({'message': 'topic not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)
