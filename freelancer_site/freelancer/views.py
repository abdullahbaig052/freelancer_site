from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from freelancer.models import Project, AppUser, Bids
from freelancer.forms import *


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homeview')

        else:
            form = SignUpForm()
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homeview')
        else:
            form = LoginForm()
        return render(request, self.template_name, {'form' : form})


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'home.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        if request.user.appuser.user_type == "hire":
            project_details = Project.objects.filter(user_id=request.user.id)
            context['project_details'] = project_details
        else:
            project_details = Project.objects.all()
            userbids = Bids.objects.filter(user_id = request.user.id)
            context['project_details'] = project_details
            context['userbids'] = userbids
            context['bids_project_ids'] =Bids.objects.values_list('project_id', flat=True)\
                .filter(user_id=request.user.id)

            context['status_hired'] =Bids.objects.values_list('project_id', flat=True)\
                .filter(project_status="Hired")

        return render(request, self.template_name, context)


class LogoutView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        logout(request)
        return redirect("indexview")


class EditView(TemplateView):
    template_name = "user_edit.html"

    def get(self, request):
        user_details = AppUser.objects.get(id=request.user.id)
        form = UserProfileEditForm(instance=user_details)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('homeview')
        else:
            form = UserProfileEditForm(instance=request.user)
        return render(request, self.template_name, {
            'form': form
        })


class PostProjectView(TemplateView):
    template_name = 'postproject.html'

    def get(self, request):
        form = PostProjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user.id
            project.save()
            return redirect("homeview")
        else:
            form = PostProjectForm()
        return render(request, self.template_name, {'form': form})


class DeleteProjectView(TemplateView):
    template_name = "home.html"

    def get(self, request, id):
        instance = Project.objects.get(id=id)
        instance.delete()
        return redirect("homeview")


class EditProjectView(TemplateView):
    template_name = 'editproject.html'

    def get(self, request, id):
        project_details = Project.objects.get(id=id)
        form = PostProjectForm(instance=project_details)
        return render(request, self.template_name, {'form': form})

    def post(self, request, id):
        form = PostProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(id=id)
            project.name = form.cleaned_data["name"]
            project.description = form.cleaned_data["description"]
            project.budget = form.cleaned_data["budget"]
            project.save()
            return redirect("homeview")
        else:
            form = PostProjectForm()
        return render(request, self.template_name, {'form': form})


class UserBidView(TemplateView):
    template_name = "userbids.html"

    def get(self, request, id):
        form = UserBidsForm()
        return render(request, self.template_name, {'form' :form})

    def post(self, request, id):
        form = UserBidsForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user_id = request.user.id
            bid.project_id = id
            bid.save()
            return redirect("homeview")
        else:
            form = UserBidsForm()
        return render(request, self.template_name, {'form': form})


class BidsProjectView(TemplateView):
    template_name = "bids.html"

    def get(self, request, id):
        bids = Bids.objects.filter(project_id=id)
        form = StatusForm(request.GET)
        return render(request, self.template_name, { 'bids':bids, 'form':form})

    def post(self, request, id):
        form = StatusForm(request.POST)
        bid = Bids.objects.get(id=id)
        if form.data.get('status') == "Approve":
            bid.status = form.data.get('status')
            bid.project_status = "Hired"
            bid.save()
        return redirect("homeview")


class UserProfileView(TemplateView):
    template_name = "profile.html"

    def get(self, request, id):
        users = AppUser.objects.filter(id=id)
        context = {
            'username': users[0].username,
            'fname': users[0].first_name,
            'lname': users[0].last_name,
            'user_type': users[0].user_type,

        }
        return render(request, self.template_name, context)


class ProjectDetailView(TemplateView):
    template_name = "project_detail.html"

    def get(self, request, id):
        project_details = Project.objects.filter(id=id)
        return render(request, self.template_name,{'project_details' :project_details[0]})
