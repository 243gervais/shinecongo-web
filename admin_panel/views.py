from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, FileResponse
from django.conf import settings
import os

from applications.models import JobApplication
from careers.models import JobRole
from contact.models import ContactMessage


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_authenticated and user.is_staff


def admin_login(request):
    """Custom login view for admin panel"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    next_url = request.POST.get('next', 'admin_panel:dashboard')
                    if next_url == 'admin_panel:dashboard' or next_url.startswith('/admin-panel'):
                        return redirect('admin_panel:dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Vous n\'avez pas les permissions nécessaires pour accéder à cette page.')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez vérifier vos identifiants.')
    else:
        form = AuthenticationForm()
    
    next_url = request.GET.get('next', '')
    return render(request, 'admin_panel/login.html', {
        'form': form,
        'next': next_url
    })


@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    """Admin dashboard with statistics"""
    
    # Statistics
    total_applications = JobApplication.objects.count()
    new_applications = JobApplication.objects.filter(reviewed=False).count()
    total_jobs = JobRole.objects.count()
    active_jobs = JobRole.objects.filter(is_active=True).count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(read=False).count()
    
    # Recent activity
    recent_applications = JobApplication.objects.all()[:5]
    recent_messages = ContactMessage.objects.all()[:5]
    
    # Chart data (last 7 days)
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=x) for x in range(6, -1, -1)]
    
    applications_by_day = []
    messages_by_day = []
    
    for day in last_7_days:
        app_count = JobApplication.objects.filter(
            applied_at__date=day
        ).count()
        msg_count = ContactMessage.objects.filter(
            created_at__date=day
        ).count()
        applications_by_day.append(app_count)
        messages_by_day.append(msg_count)
    
    context = {
        'total_applications': total_applications,
        'new_applications': new_applications,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'recent_applications': recent_applications,
        'recent_messages': recent_messages,
        'applications_by_day': applications_by_day,
        'messages_by_day': messages_by_day,
        'days': [d.strftime('%d/%m') for d in last_7_days],
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def applications_list(request):
    """List all job applications"""
    applications = JobApplication.objects.all()
    
    # Filters
    search = request.GET.get('search', '')
    reviewed = request.GET.get('reviewed', '')
    
    if search:
        applications = applications.filter(
            Q(full_name__icontains=search) |
            Q(physical_address__icontains=search) |
            Q(phone__icontains=search)
        )
    
    if reviewed == 'yes':
        applications = applications.filter(reviewed=True)
    elif reviewed == 'no':
        applications = applications.filter(reviewed=False)
    
    context = {
        'applications': applications,
        'search': search,
        'reviewed': reviewed,
    }
    
    return render(request, 'admin_panel/applications_list.html', context)


@login_required
@user_passes_test(is_staff_user)
def application_detail(request, pk):
    """View application details"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    if request.method == 'POST':
        reviewed = request.POST.get('reviewed') == 'on'
        notes = request.POST.get('notes', '')
        
        application.reviewed = reviewed
        application.notes = notes
        application.save()
        
        messages.success(request, 'Candidature mise à jour avec succès!')
        return redirect('admin_panel:application_detail', pk=pk)
    
    return render(request, 'admin_panel/application_detail.html', {
        'application': application
    })


@login_required
@user_passes_test(is_staff_user)
def download_cv(request, pk):
    """Download CV file"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    if application.cv_file:
        try:
            # Try to get file path (works for local storage)
            if hasattr(application.cv_file, 'path'):
                file_path = application.cv_file.path
                if os.path.exists(file_path):
                    return FileResponse(
                        open(file_path, 'rb'),
                        as_attachment=True,
                        filename=os.path.basename(file_path)
                    )
            # For S3 storage, redirect to the file URL
            if application.cv_file.url:
                return redirect(application.cv_file.url)
        except Exception as e:
            pass
    
    messages.error(request, 'Fichier CV non trouvé.')
    return redirect('admin_panel:application_detail', pk=pk)


@login_required
@user_passes_test(is_staff_user)
def jobs_list(request):
    """List all job roles"""
    jobs = JobRole.objects.all()
    
    search = request.GET.get('search', '')
    active = request.GET.get('active', '')
    
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    if active == 'yes':
        jobs = jobs.filter(is_active=True)
    elif active == 'no':
        jobs = jobs.filter(is_active=False)
    
    return render(request, 'admin_panel/jobs_list.html', {
        'jobs': jobs,
        'search': search,
        'active': active,
    })


@login_required
@user_passes_test(is_staff_user)
def job_create(request):
    """Create a new job role"""
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        responsibilities = request.POST.get('responsibilities')
        requirements = request.POST.get('requirements')
        benefits = request.POST.get('benefits', '')
        employment_type = request.POST.get('employment_type')
        location = request.POST.get('location', 'Kinshasa, RDC')
        is_active = request.POST.get('is_active') == 'on'
        
        job = JobRole.objects.create(
            title=title,
            slug=slug,
            description=description,
            responsibilities=responsibilities,
            requirements=requirements,
            benefits=benefits,
            employment_type=employment_type,
            location=location,
            is_active=is_active
        )
        
        messages.success(request, f'Poste "{title}" créé avec succès!')
        return redirect('admin_panel:job_detail', pk=job.pk)
    
    return render(request, 'admin_panel/job_form.html', {
        'action': 'create'
    })


@login_required
@user_passes_test(is_staff_user)
def job_detail(request, pk):
    """View and edit job role"""
    job = get_object_or_404(JobRole, pk=pk)
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.slug = request.POST.get('slug')
        job.description = request.POST.get('description')
        job.responsibilities = request.POST.get('responsibilities')
        job.requirements = request.POST.get('requirements')
        job.benefits = request.POST.get('benefits', '')
        job.employment_type = request.POST.get('employment_type')
        job.location = request.POST.get('location', 'Kinshasa, RDC')
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()
        
        messages.success(request, 'Poste mis à jour avec succès!')
        return redirect('admin_panel:job_detail', pk=pk)
    
    return render(request, 'admin_panel/job_form.html', {
        'job': job,
        'action': 'edit'
    })


@login_required
@user_passes_test(is_staff_user)
def job_delete(request, pk):
    """Delete a job role"""
    job = get_object_or_404(JobRole, pk=pk)
    
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f'Poste "{title}" supprimé avec succès!')
        return redirect('admin_panel:jobs_list')
    
    return render(request, 'admin_panel/job_delete.html', {
        'job': job
    })


@login_required
@user_passes_test(is_staff_user)
def messages_list(request):
    """List all contact messages"""
    contact_messages = ContactMessage.objects.all()
    
    search = request.GET.get('search', '')
    read = request.GET.get('read', '')
    
    if search:
        contact_messages = contact_messages.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search)
        )
    
    if read == 'yes':
        contact_messages = contact_messages.filter(read=True)
    elif read == 'no':
        contact_messages = contact_messages.filter(read=False)
    
    return render(request, 'admin_panel/messages_list.html', {
        'messages': contact_messages,
        'search': search,
        'read': read,
    })


@login_required
@user_passes_test(is_staff_user)
def message_detail(request, pk):
    """View message details"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    # Mark as read when viewing
    if not message.read:
        message.read = True
        message.save()
    
    if request.method == 'POST':
        replied = request.POST.get('replied') == 'on'
        notes = request.POST.get('notes', '')
        
        message.replied = replied
        message.notes = notes
        message.save()
        
        messages.success(request, 'Message mis à jour avec succès!')
        return redirect('admin_panel:message_detail', pk=pk)
    
    return render(request, 'admin_panel/message_detail.html', {
        'message': message
    })


@login_required
def admin_logout(request):
    """Logout view for admin panel"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('core:home')

