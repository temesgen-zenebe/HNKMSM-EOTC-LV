from django.views.generic import ListView, DetailView,CreateView
from django.views.generic import TemplateView
from .models import BooksLibrary, Gallery, UserManual, PraiseGlory, TestimonyOfSalvation, ArchiveLink
from .forms import BooksLibraryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BooksLibrary
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect


class MultimediaView(TemplateView):
    template_name = 'multimedia/multimediaView.html'

class BooksLibraryListView(ListView):
    model = BooksLibrary
    template_name = 'multimedia/books_library_list.html'
    context_object_name = 'books'
    paginate_by = 10

class BooksLibraryDetailView(DetailView):
    model = BooksLibrary
    template_name = 'multimedia/books_library_detail.html'
    context_object_name = 'book'

class GalleryListView(ListView):
    model = Gallery
    template_name = 'multimedia/gallery_list.html'
    context_object_name = 'media'
    paginate_by = 10

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'multimedia/gallery_detail.html'
    context_object_name = 'media_item'

class UserManualListView(ListView):
    model = UserManual
    template_name = 'multimedia/user_manual_list.html'
    context_object_name = 'manuals'
    paginate_by = 10

class UserManualDetailView(DetailView):
    model = UserManual
    template_name = 'multimedia/user_manual_detail.html'
    context_object_name = 'manual'

class PraiseGloryListView(ListView):
    model = PraiseGlory
    template_name = 'multimedia/praise_glory_list.html'
    context_object_name = 'praises'
    paginate_by = 10

class PraiseGloryDetailView(DetailView):
    model = PraiseGlory
    template_name = 'multimedia/praise_glory_detail.html'
    context_object_name = 'praise'

class TestimonyOfSalvationListView(ListView):
    model = TestimonyOfSalvation
    template_name = 'multimedia/testimony_of_salvation_list.html'
    context_object_name = 'testimonies'
    paginate_by = 10

class TestimonyOfSalvationDetailView(DetailView):
    model = TestimonyOfSalvation
    template_name = 'multimedia/testimony_of_salvation_detail.html'
    context_object_name = 'testimony'

class ArchiveLinkListView(ListView):
    model = ArchiveLink
    template_name = 'multimedia/archive_link_list.html'
    context_object_name = 'archives'
    paginate_by = 10

class ArchiveLinkDetailView(DetailView):
    model = ArchiveLink
    template_name = 'multimedia/archive_link_detail.html'
    context_object_name = 'archive'



class BooksLibraryCreateView(CreateView, LoginRequiredMixin):
    model = BooksLibrary
    form_class = BooksLibraryForm
    template_name = 'multimedia/books_library_form.html'
    success_url = reverse_lazy('multimedia:books_library_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        published_date = form.cleaned_data.get('published_date')
        
        # Check if a book with the same title, author, and published date already exists
        if BooksLibrary.objects.filter(title=title, author=author, published_date=published_date).exists():
            form.add_error(None, "A book with the same title, author, and published date already exists.")
            return self.form_invalid(form)
        
        return super().form_valid(form)

# multimedia/
# books_library_list.html
# books_library_detail.html
# gallery_list.html
# gallery_detail.html
# user_manual_list.html
# user_manual_detail.html
# praise_glory_list.html
# praise_glory_detail.html
# testimony_of_salvation_list.html
# testimony_of_salvation_detail.html
# archive_link_list.html
# archive_link_detail.html