from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView

from .models import Student, SRSone, SRStwo, FinalResult


class StudentListView(ListView):
    template_name = 'main/grades_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.only('name', 'surname', 'gpa', 'url').order_by('surname', 'name')



class StudentDetailView(View):
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









