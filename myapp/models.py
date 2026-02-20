from django.db import models
from django.contrib.auth.models import User



# ================= DJANGO ORM MODELS =================

# ----------------- Student -----------------
class Student(models.Model):
    name = models.CharField(max_length=100)
    regno = models.CharField(max_length=20)
    email = models.EmailField()
    # Add other fields only if they exist in MySQL table

    class Meta:
        db_table = 'student'   # Matches MySQL table
        managed = False        # Django will not create/alter table

    def __str__(self):
        return self.name


# ----------------- Driver -----------------
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    bus_no = models.CharField(max_length=20)

    class Meta:
        db_table = 'driver'
        managed = False

    def __str__(self):
        return self.user.username


# ----------------- Passenger -----------------
class Passenger(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'passenger'
        managed = False

    def __str__(self):
        return self.name


# ----------------- Attendance -----------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20)
    wait_time = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'attendance'
        managed = False

    def __str__(self):
        return f"{self.student.name} - {self.date}"




# ----------------- Student Status -----------------
class StudentStatus(models.Model):
    STATUS_CHOICES = [
        ('come', 'Coming'),
        ('notcome', 'Not Coming'),
        ('wait', 'Waiting'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    wait_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'student_status'
        managed = False

    def __str__(self):
        return f"{self.user.username} - {self.status}"



  


# ----------------- Fee -----------------
class Fee(models.Model):
    student = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])

    class Meta:
        db_table = 'fee'
        managed = False

    def __str__(self):
        return self.student.user.username


# ----------------- Bus Fees -----------------
class BusFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid_on = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'bus_fees'
        managed = False

    def __str__(self):
        return f"{self.student.name} - {self.amount}"
    

    
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username



class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bus_stop = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class StudentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    wait_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_status'
        unique_together = ('user', 'date')

    def __str__(self):
        return self.user.username
    
    
   


class StudentDetail(models.Model):
    register_no = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    bus_stop = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'studentdetail'   # IMPORTANT


class BusDriver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bus_no = models.CharField(max_length=20)
    route = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'bus_drivers'


class BusFees(models.Model):
    register_no = models.CharField(max_length=20)
    amount = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'bus_fees'


class PassengerList(models.Model):
    register_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    bus_stop = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    wait_time = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'passenger_list_real_90'