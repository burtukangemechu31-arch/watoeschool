# exams/views.py
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, Question, ExamSubmission, MarkAssessment
from academics.models import StudentProfile
from accounts.models import User

@login_required
def exams_dashboard(request):
    submissions = ExamSubmission.objects.all().order_by('-submitted_at')[:50]
    assessments = MarkAssessment.objects.all().order_by('-id')[:50]
    active_exams = Exam.objects.filter(is_active=True)

    context = {
        'submissions': submissions,
        'assessments': assessments,
        'active_exams': active_exams,
    }
    return render(request, 'exams/dashboard.html', context)


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)
    student = get_object_or_404(StudentProfile, user=request.user)
    
    submission, created = ExamSubmission.objects.get_or_create(student=student, exam=exam)
    if getattr(submission, 'is_completed', False):
        return redirect('exam_result', submission_id=submission.id)

    # Shuffle questions to ensure academic integrity and prevent cheating
    questions = exam.questions.all().order_by('?')

    if request.method == 'POST':
        score = 0
        total_weight = 0

        for question in questions:
            total_weight += question.marks
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += question.marks

        if hasattr(submission, 'score_obtained'):
            submission.score_obtained = score
        if hasattr(submission, 'is_completed'):
            submission.is_completed = True
        submission.save()
        return redirect('exam_result', submission_id=submission.id)

    return render(request, 'exams/take_exam.html', {
        'exam': exam,
        'questions': questions,
        'duration_minutes': getattr(exam, 'duration_minutes', 60)
    })


@login_required
def exam_result(request, submission_id):
    submission = get_object_or_404(ExamSubmission, id=submission_id)
    questions = submission.exam.questions.all()
    return render(request, 'exams/exam_result.html', {
        'submission': submission, 
        'exam': submission.exam,
        'questions': questions
    })


# --- BULK UPLOAD & TEMPLATE DOWNLOAD UTILITIES ---

@login_required
def download_question_template(request):
    """Generates and downloads a CSV template for bulk uploading exam questions."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="question_upload_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['text', 'marks', 'correct_option', 'option_a', 'option_b', 'option_c', 'option_d'])
    writer.writerow(['What is the chemical symbol for Gold?', '5', 'A', 'Au', 'Ag', 'Fe', 'Cu'])
    return response


@login_required
def bulk_upload_questions(request, exam_id):
    """Processes bulk uploaded CSV questions for a specific exam."""
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        count = 0
        for row in reader:
            Question.objects.create(
                exam=exam,
                text=row.get('text'),
                marks=int(row.get('marks', 1)),
                correct_option=row.get('correct_option', 'A').strip().upper(),
                option_a=row.get('option_a'),
                option_b=row.get('option_b'),
                option_c=row.get('option_c'),
                option_d=row.get('option_d'),
            )
            count += 1
            
        messages.success(request, f"Successfully imported {count} questions into {exam.title}!")
        return redirect('exams_dashboard')
    
    return render(request, 'exams/bulk_upload_questions.html', {'exam': exam})


@login_required
def download_result_template(request):
    """Generates and downloads a CSV template for bulk uploading student scores."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_results_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['username', 'exam_id', 'score_obtained', 'is_completed'])
    writer.writerow(['student_bezawit', '1', '85', 'True'])
    return response


@login_required
def bulk_upload_results(request):
    """Processes bulk uploaded CSV student results."""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        count = 0
        for row in reader:
            try:
                user = User.objects.get(username=row.get('username'))
                exam = Exam.objects.get(id=int(row.get('exam_id')))
                
                # Check for StudentProfile or fallback to user
                student_profile = StudentProfile.objects.filter(user=user).first()
                if student_profile:
                    submission, created = ExamSubmission.objects.get_or_create(student=student_profile, exam=exam)
                else:
                    submission, created = ExamSubmission.objects.get_or_create(student=user, exam=exam)
                    
                submission.score_obtained = float(row.get('score_obtained', 0))
                submission.is_completed = str(row.get('is_completed', 'True')).lower() == 'true'
                submission.save()
                count += 1
            except Exception:
                continue
                
        messages.success(request, f"Successfully uploaded {count} student result records!")
        return redirect('exams_dashboard')
        
    return render(request, 'exams/bulk_upload_results.html')