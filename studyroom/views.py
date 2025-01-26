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
    """
    Render the user dashboard with various user-specific information.

    **Context**
        sessions: a list of the user's most recent StudySession objects
        user_topics: a list of the user's most recent interested topics
        tags: a list of all available Tag objects
        user: the current user object
        user_tags: a list of tags associated with the user
        matches: a list of CustomUser objects with matching tags, excluding the current user
        topic_matches: a list of Topic objects that share tags with the user but are not yet of interest
        groups: a list of the user's study groups
        user_chatrooms: a list of chatrooms the user is a part of

    **Template**
        studyroom/dashboard.html
    """

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
    """
    Landing page for the study buddy app.

    Args:
        request: The current request object.

    Returns:
        A rendered HTML page.
    """
    return render(request, 'studyroom/landing-page.html')

@login_required
def topics_list(request):
    """
    Shows a list of all topics that the user is not currently interested in.

    The page will display the user's current topics of interest, a list of all topics, and a list of suggested topics based on the user's tags.

    Args:
        request: The HTTP request object

    Returns:
        A rendered HTML page with the topic list
    """
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
    """
    Creates a new topic with the given name, description, and tags.

    If the request is a POST, it validates the form and if valid, creates a new topic and redirects to the topic page.

    Args:
        request: The HTTP request object

    Returns:
        A JSON response indicating the result of the request
    """
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
    """
    Updates the topics of interest for the current user.

    If the request is a POST, it expects a list of tag IDs to be passed
    in the request body. It clears the current topics of interest for the
    user and adds the selected topics.

    Returns a JSON response with a success message if the request is valid,
    or an error message if the request method is invalid.
    """
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
    """
    Renders a page displaying all the users that share at least one tag with the current user.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: A rendered HTML page with the list of matching users.
    """
    
    user = request.user
    user_tags = user.tags.all()
    matches = CustomUser.objects.filter(tags__in=user_tags).exclude(id=user.id).distinct()

    return render(request, "studyroom/matches.html", {"matches": matches})

@login_required
def groups_list(request):
    """
    Renders a page displaying all the groups the user is a member of, along with all the tags available for creating a new group.

    Args:
        request: The HTTP request object

    Returns:
        A rendered HTML page displaying the user's groups and available tags
    """
    user_groups = request.user.study_groups.all()
    tags = Tag.objects.all()

    context = {
        "user_groups": user_groups,
        "tags": tags,
    }
    return render(request, 'studyroom/groups.html', context)

@login_required
def create_group(request):
    """
    Creates a new group with the given name, description, and tags.

    If the request is a POST, it validates the form and if valid, creates a new group and redirects to the group page.

    Args:
        request: The HTTP request object

    Returns:
        A JSON response indicating the result of the request
    """
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
    """
    Searches for groups by name or ID.

    Args:
        request: The request object.

    Returns:
        A JSON response containing the HTML of the search results.
    """
    query = request.GET.get('q', '')
    groups = Group.objects.filter(Q(name__icontains=query) | Q(group_id__icontains=query))

    if request.method == 'GET':
        html = render_to_string('studyroom/search_results.html', {'groups': groups})
        return JsonResponse({'html': html})

@login_required
def join_group(request):
    """
    Joins a group for the current user.

    If the request is a POST, and the group_id parameter is provided, the current user will be added to the group.

    Args:
        request: The request object.

    Returns:
        A JSON response indicating the result of the request.
    """
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

@login_required
def add_topic(request):
    """
    Adds a topic to the topics of interest for the current user.

    If the request is a POST, and the topic_id parameter is provided, the topic will be added to the topics of interest for the current user.

    Args:
        request: The request object.

    Returns:
        A JsonResponse indicating the result of the request.
    """

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        try:
            topic = Topic.objects.get(id=topic_id)
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
    """
    Remove a topic from the user's interested topics.

    This view will remove a topic from the user's interested topics when the user clicks the 'remove' button on their topics page.
    The view will return a JSON response, which will then be used to update the user's topic list on the page.

    :param request: The HTTP request object
    :return: A JSON response indicating the result of the removal
    """
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
