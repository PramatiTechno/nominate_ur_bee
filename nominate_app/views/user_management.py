from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from nominate_app.models import *
from django.contrib.auth.models import User, Group
from nominate_app.forms import AddUserForm
from django.core.mail import send_mail
from nominate_app.utils import group_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from IPython import embed


@group_required('Admin', raise_exception=True)
def index(request):
	groups = Group.objects.all()
	group = groups[0]
	group_list = []
	for _group in groups:
		group_list.append({
			'id': _group.id,
			'name': _group.name
		})
	group_list.append({
		'id': 0,
		'name': 'Invited'
	})

	selected_group = group_list[0]
	user_list = []
	if 'group' in request.GET:
		group_id = request.GET['group']
		if group_id == '0':
			selected_group = {
				'id': 0,
				'name': 'Invited'
			}
			for invite in UserInvite.objects.all():
				user_list.append({
					'first_name': '',#invite.first_name,
					'last_name': '',#invite.last_name,
					'email': invite.email,
					'baselocation': '',#invite.baselocation,
					'designation': '',#invite.designation,
				})
			return render(request, 'nominate_app/user_management/index.html', {'users': user_list, 'groups':group_list, 'c_group': selected_group})

		else:
			group = groups.get(id=group_id)
			selected_group = {
				'id': group.id,
				'name': group.name
			}

	users = User.objects.filter(groups=selected_group['id'])
	for user in users:
		if user.groups.order_by('-group')[0] == group:  # to get the users if the group is his/her highest
			user_list.append({
				'first_name': user.first_name,
				'last_name': user.last_name,
				'email': user.email,
				'baselocation': user.userprofile.baselocation,
				'designation': user.userprofile.designation,
			})

	return render(request, 'nominate_app/user_management/index.html', {'users': user_list, 'groups':group_list, 'c_group': selected_group})


@group_required('Admin', raise_exception=True)
def new(request):
	invite_form = AddUserForm()
	return render(request, 'nominate_app/user_management/new.html', {'invite_form': invite_form})


@group_required('Admin', raise_exception=True)
def create(request):
	email = request.POST['email']
	group_id = request.POST['group']
	group = Group.objects.get(id=group_id)
	invite = UserInvite(email=email, group=group)
	invite.save()
	message_value_html_template = render_to_string('nominate_app/emails/invitation.html',{'user_group':group.name,'url':os.environ['SERVER_NAME']})
	plain_message_value = strip_tags(message_value_html_template)
	send_mail(subject='Welcome To Nominate Your Bee !!!!', from_email='pramati@gmail.com', \
		recipient_list=[str(email)], message=plain_message_value, fail_silently=False)
	return redirect('/users?group=0')

