# library/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookBorrowing
from academics.models import StudentProfile

@login_required
def library_catalog(request):
    """Displays searchable list of physical books and digital e-book repositories."""
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) if query else Book.objects.all()
    
    # If student, retrieve their personal active borrows
    my_borrows = []
    if hasattr(request.user, 'studentprofile'):
        my_borrows = BookBorrowing.objects.filter(student=request.user.studentprofile, is_returned=False)

    return render(request, 'library/catalog.html', {
        'books': books,
        'my_borrows': my_borrows,
        'query': query
    })

@login_required
def download_digital_book(request, book_id):
    """Allows authorized users to download or read digital book PDFs."""
    book = get_object_or_404(Book, id=book_id)
    if book.digital_file:
        return redirect(book.digital_file.url)
    return redirect('library_catalog')