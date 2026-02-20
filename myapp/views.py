from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import StudentProfile
from . models import (
    Driver, Student, StudentStatus,StudentStatus,
    UserProfile, Fee, Passenger
)
from django.http import JsonResponse

from .models import StudentDetail
from .forms import UserRegisterForm, StudentForm, DriverForm


from .models import StudentDetail, StudentStatus, BusDriver
# ================= HOME =================
def home(request):
    return render(request, 'home.html')


# ================= LOGIN/LOGOUT =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:  # Only admin users
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, "Invalid Admin Credentials")
    return render(request, 'admin_login.html')

# ================= ADMIN DASHBOARD =================
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('admin_login')

    students = UserProfile.objects.filter(role='student')
    drivers = UserProfile.objects.filter(role='driver')
    fees = Fee.objects.all()

    context = {
        "students": students,
        "drivers": drivers,
        "fees": fees,
        "total_students": students.count(),
        "total_drivers": drivers.count(),
        "total_buses": drivers.count(),  # change later if you add Bus model
    }

    return render(request, "admin_dashboard.html", context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  

# ================= STUDENT login & DASHBOARD =================

def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='Student').exists():
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid Student Credentials")

    return render(request, 'student_login.html')

@login_required
def student_dashboard(request):
    # Auto create profile if not exists
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={"bus_stop": "Anna Nagar"}  # default bus stop
    )

    # Get last status (if any)
    status = StudentStatus.objects.filter(user=request.user).last()

    return render(request, "student_dashboard.html", {
        "profile": profile,
        "status": status
    })

# ---------------------------
# Submit student status
# ---------------------------
@login_required
def submit_student_status(request):
    if request.method == "POST":
        status_text = request.POST.get("status")
        wait_time = request.POST.get("wait_time")

        StudentStatus.objects.create(
            user=request.user,
            status=status_text,
            wait_time=wait_time if wait_time else None
        )

    return redirect("student_dashboard")



@login_required
def student_status(request):

    if not request.user.groups.filter(name='Student').exists():
        return redirect('student_login')

    today = timezone.now().date()

    status_obj = StudentStatus.objects.filter(
        user=request.user,
        date=today
    ).first()

    context = {
        "status": status_obj.status if status_obj else None,
        "student": request.user
    }

    return render(request, "student_status.html", context)

@login_required
def student_status_page(request):
    status = StudentStatus.objects.filter(user=request.user).last()
    profile = StudentProfile.objects.filter(user=request.user).first()

    return render(request, "student_status.html", {
        "status": status,
        "profile": profile
    })
        

@login_required
def submit_status(request):
    if request.method == "POST":
        status = request.POST.get("status")
        wait_time = request.POST.get("wait_time")

        StudentStatus.objects.create(
            user=request.user,
            status=status,
            wait_time=wait_time
        )

        return redirect('student_dashboard')  # redirect after submit

    return redirect('student_status')
    

# ================= DRIVER DASHBOARD =================

def driver_login(request): 
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password") 
        user = authenticate(request, username=username, password=password) 
        if user is not None and user.groups.filter(name='Driver').exists():
            login(request, user)
            return redirect('driver_dashboard')
        else:
            messages.error(request, "Invalid Driver Credentials") 
            return render(request, 'driver_login.html')


@login_required
def driver_dashboard(request):
    if not request.user.groups.filter(name='Driver').exists():
        return redirect('home')
    today = timezone.now().date()
    statuses = StudentStatus.objects.filter(date=today)
    context = {
        "total": statuses.count(),
        "coming": statuses.filter(status='come').count(),
        "waiting": statuses.filter(status='wait').count(),
        "notcoming": statuses.filter(status='notcome').count(),
    }
    return render(request, "driver_dashboard.html", context)

@login_required
def passenger_list(request):

    if not request.user.groups.filter(name='Driver').exists():
        return redirect('home')

    today = timezone.now().date()

    students = StudentStatus.objects.filter(
        date=today
    ).select_related('user')

    return render(request, "passenger_list.html", {"students": students})

def feedback_view(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        message = request.POST.get("message")

        # Do NOT save to DB, just show success popup
        return render(request, "feedback.html", {"submitted": True})

    return render(request, "feedback.html")


# ================= ABOUT PAGE =================
def about(request):
    return render(request, 'about.html')
  

def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, "driver_list.html", {"drivers": drivers})

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password check
        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        # Email already exists check
        if User.objects.filter(username=email).exists():
            return render(request, "signup.html", {"error": "Email already registered"})

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # Assign group
        group_name = role.capitalize()  # student → Student
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        messages.success(request, "Signup Successful!")

        return redirect("signup")

    return render(request, "signup.html")

def login_page(request):
    return render(request, "login.html")




def student_login(request):
    if request.method == "POST":
        register_no = request.POST.get("register_no")

        try:
            student = StudentDetail.objects.get(register_no=register_no)
            request.session['student'] = student.register_no
            return redirect('student_dashboard')
        except StudentDetail.DoesNotExist:
            return render(request, 'student_login.html', {'error': 'Invalid Register Number'})

    return render(request, 'student_login.html')


@login_required
def create_student_profile(request):
    # check if profile already exists
    if not StudentProfile.objects.filter(user=request.user).exists():
        StudentProfile.objects.create(
            user=request.user,
            bus_stop="Anna Nagar"
        )
    return redirect("student_dashboard")