from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.contrib.auth import login, logout, authenticate
from .models import Student, SRSone, SRStwo, FinalResult, Teacher, Subject, Group, TeacherGroup
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class MainListView(LoginRequiredMixin, ListView):
    """Студенты и учителя"""
    template_name = 'main/index.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        # Получите текущего пользователя
        user = self.request.user

    # Проверьте, является ли пользователь учителем или студентом
        if user.is_authenticated and user.groups.filter(name='Teacher').exists():
            # Если пользователь - учитель, получите его данные
            return Teacher.objects.filter(user=user)
        elif user.is_authenticated and user.groups.filter(name='Students').exists():
            # Если пользователь - студент, получите его данные
            return Student.objects.filter(user=user)
        else:
            # Если пользователь не является учителем или студентом, верните ошибку 404
            raise Http404("Пользователь не найден или у него нет прав")


class TeacherProfileView(LoginRequiredMixin, View):
    """Профиль учителя"""

    def get(self, request, slug):
        teacher = get_object_or_404(Teacher, url=slug)

        # Проверяем, является ли текущий пользователь тем самым учителем
        if teacher.user == request.user:
            return render(request, "main/profile.html", {
                "teacher": teacher,
            })
        else:
            raise Http404("Доступ запрещен")


class StudentProfileView(LoginRequiredMixin, View):
    """Профиль студента"""

    def get(self, request, slug):
        student = get_object_or_404(Student, url=slug)

        # Проверяем, является ли текущий пользователь тем самым студентом
        if student.user == request.user:
            return render(request, "main/profile_students.html", {
                "student": student,
            })
        else:
            # Если текущий пользователь не является тем самым студентом, вы можете вернуть ошибку 403 (доступ запрещен)
            raise Http404("Доступ запрещен")


class StudentListView(ListView):
    """Все студенты"""
    template_name = 'main/grades_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.only('name', 'surname', 'gpa', 'url').order_by('surname', 'name')


class StudentDetailView(View):
    """Оценки студента"""
    def get(self, request, slug):
        student = get_object_or_404(Student, url=slug)
        srs_ones = SRSone.objects.filter(student=student)
        srs_twos = SRStwo.objects.filter(student=student)
        final_results = FinalResult.objects.filter(student=student)

        return render(request, "main/table2.html", {"student": student,
                                                    "srs_ones": srs_ones,
                                                    "srs_twos": srs_twos,
                                                    "final_results": final_results})

    def post(self, request, slug):
        student = get_object_or_404(Student, url=slug)

        final_result_id = request.POST.get('final_result_id')
        if final_result_id:
            final_result = get_object_or_404(FinalResult, id=final_result_id)
            final_result.calculate_final_result()

        srs_ones = SRSone.objects.filter(student=student)
        srs_twos = SRStwo.objects.filter(student=student) 

        srs_one_id = request.POST.get('srs_one_id')
        if srs_one_id:
            srs_one = get_object_or_404(SRSone, id=srs_one_id)
            srs_one.calculate_and_save_result()

        srs_two_id = request.POST.get('srs_two_id')
        if srs_two_id:
            srs_two = get_object_or_404(SRStwo, id=srs_two_id)
            srs_two.calculate_and_save_result()

        final_results = FinalResult.objects.filter(student=student)

        student.calculate_gpa()  # Вычислить и сохранить GPA для студента

        return render(request, "main/table2.html", {"student": student,
                                                    "srs_ones": srs_ones,
                                                    "srs_twos": srs_twos,
                                                    "final_results": final_results,
                                                    })


class StudentGradesView(LoginRequiredMixin, View):
    """Оценки студента"""

    def get(self, request, slug):
        student = get_object_or_404(Student, url=slug)
        srs_ones = SRSone.objects.filter(student=student)
        srs_twos = SRStwo.objects.filter(student=student)
        final_results = FinalResult.objects.filter(student=student)

        return render(request, "main/grades_student.html", {"student": student,
                                                            "srs_ones": srs_ones,
                                                            "srs_twos": srs_twos,
                                                            "final_results": final_results})


class TeacherGroupView(LoginRequiredMixin, View):
    def get(self, request, slug):
        teacher = Teacher.objects.get(url=slug)
        groups = teacher.group.all()
        group_students = {}

        for group in groups:
            students = group.student_set.all().order_by('surname', 'name')
            group_students[group] = students

        return render(request, "main/group_teacher.html", {
                                                            "teacher": teacher,
                                                            "groups": group_students,
                                                            "student": students, })


def teacher_subject_grades(request, teacher_url, group_link):
    user = request.user

    try:
        teacher = Teacher.objects.get(url=teacher_url)
    except Teacher.DoesNotExist:
        return render(request, 'main/teacher_not_found.html', context={'teacher_url': teacher_url})

    if user.groups.filter(name='Teacher').exists() and teacher == user.teacher:
        subjects_taught = teacher.subject.filter(srsone__student__group__link=group_link)
        if not subjects_taught.exists():
            return render(request, 'main/no_subjects_taught.html', context={'teacher': teacher, 'group_link': group_link})

        students_in_group = Student.objects.filter(group__link=group_link).order_by('surname', 'name')
        student_grades = SRSone.objects.filter(student__in=students_in_group, subject__in=subjects_taught).order_by(
            'student__surname', 'student__name', 'week1', 'week2', 'week3', 'week4', 'week5', 'week6', 'week7', 'week71',
            'result')

        student_grades_2 = SRStwo.objects.filter(student__in=students_in_group, subject__in=subjects_taught).order_by(
            'student__surname', 'student__name', 'week8', 'week9', 'week10', 'week11', 'week12', 'week13', 'week14',
            'week15', 'week16', 'result2' )

        zipped_data = zip(students_in_group, student_grades)
        zipped_data_2 = zip(students_in_group, student_grades_2)

        context = {
            'teacher': teacher,
            'group_link': group_link,
            'subjects_taught': subjects_taught,
            'srs_two_grades': student_grades_2,
            'zipped_data': zipped_data,
            'zipped_data_2': zipped_data_2,
            'teacher_url': teacher_url,  # Добавьте teacher_url в контекст
        }

        return render(request, 'main/grades_template.html', context)
    else:
        return render(request, 'main/no_permission.html', status=403)


def update_grade(request, teacher_url, group_link):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        student_id = request.POST.get('student_id')  # Идентификатор студента
        week = request.POST.get('week')  # Номер недели
        srs_type = request.POST.get('srs_type')  # Тип SRS (1 или 2)
        new_grade = request.POST.get('new_grade')  # Новая оценка

        try:
            # Определяем тип SRS и получаем объект оценок студента
            if srs_type == '1':
                student_grade = SRSone.objects.filter(student_id=student_id).first()
            elif srs_type == '2':
                student_grade = SRStwo.objects.filter(student_id=student_id).first()
            else:
                return JsonResponse({'success': False, 'error': 'Недопустимый тип SRS'})

            # Если объект оценок студента существует, обновляем оценку
            if student_grade:
                setattr(student_grade, f'week{week}', new_grade)
                student_grade.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Оценка не найдена'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})




def calculate_and_save_result(request, teacher_url, group_link):
    user = request.user

    # Получите учителя
    teacher = get_object_or_404(Teacher, url=teacher_url)

    # Проверьте, имеет ли пользователь право на выполнение этой операции
    if user.groups.filter(name='Teacher').exists() and teacher == user.teacher:
        if request.method == 'POST':
            # Получите идентификатор SRStwo из POST-запроса
            srstwo_id = request.POST.get('srstwo_id')
            if srstwo_id:
                srstwo = get_object_or_404(SRStwo, id=srstwo_id)
                srstwo.calculate_and_save_result()

    # Перенаправьте на страницу с оценками
    return redirect('teacher_subject_grades', teacher_url=teacher_url, group_link=group_link)

def calculate_and_save_result_srsone(request, teacher_url, group_link):
    user = request.user

    # Получите учителя
    teacher = get_object_or_404(Teacher, url=teacher_url)

    # Проверьте, имеет ли пользователь право на выполнение этой операции
    if user.groups.filter(name='Teacher').exists() and teacher == user.teacher:
        if request.method == 'POST':
            # Получите идентификатор SRSone из POST-запроса
            srsone_id = request.POST.get('srsone_id')
            if srsone_id:
                srsone = get_object_or_404(SRSone, id=srsone_id)
                srsone.calculate_and_save_result()

    # Перенаправьте на страницу с оценками
    return redirect('teacher_subject_grades', teacher_url=teacher_url, group_link=group_link)


