from models import TeacherGroup, Teacher, Student, Subject, Group, SRSone, SRStwo, FinalResult

def create_teacher_groups():
    # Получите всех учителей из базы данных
    teachers = Teacher.objects.all()

    for teacher in teachers:
        # Получите предметы, которые преподает учитель
        subjects_taught = teacher.subject.all()

        for subject in subjects_taught:
            # Получите группы, которые связаны с учителем и предметом
            groups = Group.objects.filter(teachergroup__teacher=teacher, teachergroup__subject=subject)

            for group in groups:
                # Получите студентов этой группы
                students = Student.objects.filter(group=group)

                # Создайте запись TeacherGroup для каждого студента
                for student in students:
                    teacher_group = TeacherGroup.objects.create(
                        teacher=teacher,
                        subject=subject,
                        group=group
                    )
                    teacher_group.students.add(student)

if __name__ == "__main__":
    create_teacher_groups()
