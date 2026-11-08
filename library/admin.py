# library/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import BookCategory, Book, BookBorrowing

@admin.register(BookCategory)
class BookCategoryAdmin(ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'available_copies', 'total_copies', 'shelf_location']
    list_filter = ['category', 'shelf_location']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BookBorrowing)
class BookBorrowingAdmin(ModelAdmin):
    list_display = ['student', 'book', 'borrowed_date', 'due_date', 'show_return_status']
    list_filter = ['is_returned', 'borrowed_date']
    search_fields = ['student__user__username', 'book__title']

    @display(description="Status", label={
        True: "success",
        False: "warning",
    })
    def show_return_status(self, obj):
        return "Returned" if obj.is_returned else "Active Loan"