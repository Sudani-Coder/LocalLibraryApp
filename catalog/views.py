import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from catalog.models import *
from catalog.forms import *

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = "a")
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_instances_onloan = BookInstance.objects.filter(status__exact="o").count()
    num_instances_maintenance = BookInstance.objects.filter(status__exact="m").count()
    num_instances_reserved = BookInstance.objects.filter(status__exact="r").count()

    # The "all()" is implied by default.
    num_authors = Author.objects.count()

    num_genre = Genre.objects.count()
    num_language = Language.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    template = "catalog/index.html"
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_instances_onloan": num_instances_onloan,
        "num_instances_maintenance": num_instances_maintenance,
        "num_instances_reserved": num_instances_reserved,
        "num_authors": num_authors,
        "num_genre": num_genre,
        "num_language": num_language,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, template, context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = "o").order_by("due_back")

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan to current librarians."""
    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed_librarians.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding)
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("catalog:all-borrowed"))
    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    fields = "__all__"
    initial = {"date_of_death": "05/01/2018"}

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Author
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy("catalog:authors")

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = "__all__"

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = "__all__"

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy("catalog:books")

def about(request):
    template = "catalog/about.html"
    return render(request, template)
