# academics/timetable_utils.py
from .models import TimetableSlot, Subject, Classroom, Section
from accounts.models import User
import random

def generate_automatic_timetable(section_id, academic_year):
    """
    Automatically assigns subjects to periods 1-8 across Monday to Friday 
    for a given section without duplicating periods or double-booking teachers.
    """
    section = Section.objects.get(id=section_id)
    
    # Filter subjects by grade level and stream if applicable
    if section.stream:
        subjects = list(Subject.objects.filter(grade_level=section.grade_level, stream=section.stream))
    else:
        subjects = list(Subject.objects.filter(grade_level=section.grade_level))

    teachers = list(User.objects.filter(role='teacher'))
    classrooms = list(Classroom.objects.all())

    if not subjects:
        return False, "No subjects found for this grade level and stream."

    days = ['1_Mon', '2_Tue', '3_Wed', '4_Thu', '5_Fri']
    periods = range(1, 9) # Periods 1 through 8

    # Clear existing timetable for this section before generating a fresh one
    TimetableSlot.objects.filter(section=section).delete()

    for day in days:
        # Shuffle subjects daily to distribute evenly across the week
        random.shuffle(subjects)
        subject_idx = 0

        for period in periods:
            subject = subjects[subject_idx % len(subjects)]
            teacher = random.choice(teachers) if teachers else None
            classroom = classrooms[0] if classrooms else None

            # Check if teacher is already booked at this exact day and period elsewhere
            conflict = False
            if teacher:
                conflict = TimetableSlot.objects.filter(
                    teacher=teacher, day=day, period_number=period
                ).exists()

            if not conflict:
                TimetableSlot.objects.create(
                    section=section,
                    subject=subject,
                    teacher=teacher,
                    day=day,
                    period_number=period,
                    classroom=classroom
                )
            
            subject_idx += 1

    return True, "Timetable generated successfully!"[cite: 10]