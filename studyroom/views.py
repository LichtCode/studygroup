from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Group, Topic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from users.models import Tag

@login_required
def search_group(request):
    query = request.GET.get('q', '')
    groups = Group.objects.filter(Q(name__icontains=query) | Q(group_id__icontains=query))

    if request.is_ajax():
        html = render_to_string('studyroom/search_results.html', {'groups': groups})
        return JsonResponse({'html': html})
    
    return render(request, 'studyroom/search_group.html')

@login_required
def user_profile(request):

    tags = Tag.objects.all()  # Fetch all tags for the dropdown
    user_topics = request.user.interested_topics.all()  # Fetch topics the user is interested in
    return render(request, 'studyroom/create_topic.html', {'tags': tags, 'user': request.user})


@csrf_exempt
def create_topic(request):
    if request.method == "POST":
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        tags = request.POST.get('tags', '')
        user = request.POST.get('user') 

        if not name or not description:
            return JsonResponse({'error': 'Name and Description are required.'}, status=400)

        topic = Topic.objects.create(name=name, description=description, tags=tags)
        topic, created = Topic.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if not created:
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                topic.tags.add(tag)
        topic.interested_users.add(user)

        return JsonResponse({'name': topic.name, 'description': topic.description})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(group_id=group_id)
            group.members.add(request.user)  # Add the current user to the group
            return JsonResponse({'message': 'You have successfully joined the group!'})
        except Group.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request.'}, status=400)
