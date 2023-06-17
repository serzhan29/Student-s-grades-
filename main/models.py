from django.db import models
from decimal import Decimal


class Fakulty(models.Model):
    """ Факультет """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"


class Course(models.Model):
    """ Курс студента """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курс"


class Group(models.Model):
    """ Гурппа студента """
    name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Fakulty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Subject(models.Model):
    """Прдметы"""
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    code = models.CharField(max_length=40, unique=True, default='')
    fakulty = models.ForeignKey(Fakulty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Student(models.Model):
    """ Информация об студенте """
    GENDER_CHOISE = (
        ('M', 'Мужской'),
        ('W', 'Женский'),
    )

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField()
    iin = models.CharField(max_length=12)
    gender = models.CharField(max_length=1, choices=GENDER_CHOISE)
    url = models.SlugField(max_length=100, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    def calculate_gpa(self):
        final_results = FinalResult.objects.filter(student=self)
        total_exam_grade = sum(result.exam_grade for result in final_results)
        total_credits = sum(result.subject.credits for result in final_results)

        gpa = round((total_exam_grade / len(final_results)) / total_credits, 2)
        gpa += 0.40

        self.gpa = gpa
        self.save()

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class SRSone(models.Model):
    """Оценка за АКБ 1"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    week1 = models.IntegerField()
    week2 = models.IntegerField()
    week3 = models.IntegerField()
    week4 = models.IntegerField()
    week5 = models.IntegerField()
    week6 = models.IntegerField()
    week7 = models.IntegerField()
    SRS_1 = models.IntegerField(default=0)
    result = models.FloatField(null=True, blank=True)

    def calculate_and_save_result(self):
        total_grade = self.week1 + self.week2 + \
                      self.week3 + self.week4 + \
                      self.week5 + self.week6 + \
                      self.week7

        average_grade = total_grade / 7

        result = (average_grade + self.SRS_1) / 2
        rounded_result = round(result, 0)  # Округление результата до двух десятичных знаков
        self.result = rounded_result # Сохраняет округленный результат в поле result
        self.save()  # Сохраняет объект в базе данных

    def __str__(self):
        return f"{self.student} | {self.subject.name} = {self.result}"

    class Meta:
        verbose_name = "СРС - 1"
        verbose_name_plural = "СРС - 1"


class SRStwo(models.Model):
    """Оценка за АКБ 2"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    week8 = models.IntegerField()
    week9 = models.IntegerField()
    week10 = models.IntegerField()
    week11 = models.IntegerField()
    week12 = models.IntegerField()
    week13 = models.IntegerField()
    week14 = models.IntegerField()
    week15 = models.IntegerField()
    SRS_2 = models.IntegerField(default=0)
    result2 = models.FloatField(null=True, blank=True)

    def calculate_and_save_result(self):
        total_grade = self.week8 + self.week9 + \
                      self.week10 + self.week11 + \
                      self.week12 + self.week13 + \
                      self.week14 + self.week15

        average_grade = total_grade / 8

        result2 = (average_grade + self.SRS_2) / 2
        rounded_result2 = round(result2, 0)  # Округление результата до двух десятичных знаков
        self.result2 = rounded_result2  # Сохраняет округленный результат в поле result2
        self.save()  # Сохраняет объект в базе данных

    def __str__(self):
        return f"{self.student} | {self.subject.name} = {self.result2}"

    class Meta:
        verbose_name = "СРС - 2"
        verbose_name_plural = "СРС - 2"


class FinalResult(models.Model):
    """Итоговый результат"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    SRS_1 = models.ForeignKey(SRSone, on_delete=models.CASCADE)
    SRS_2 = models.ForeignKey(SRStwo, on_delete=models.CASCADE)
    exam_grade = models.IntegerField()
    final_result2 = models.FloatField(blank=True, null=True)

    def calculate_final_result(self):
        SRS_sum = (self.SRS_1.result + self.SRS_2.SRS_2) / 2
        SRS_weighted = SRS_sum * 0.4
        exam_weighted = self.exam_grade * 0.6

        final_result = SRS_weighted + exam_weighted
        rounded_result = round(final_result, 0)  # Округление результата
        self.final_result2 = Decimal(rounded_result)  # Сохраняет округленный результат в поле final_result2
        self.save()

    def __str__(self):
        return f"{self.final_result2} | {self.subject.name}"

    class Meta:
        verbose_name = "Оценка за экзамен"
        verbose_name_plural = "Оценка за экзамены"



