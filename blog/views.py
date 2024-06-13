from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import DetailView
from .models import BlogCategory, Blog

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(visibility='public').order_by('-published_at')

# class BlogDetailView(DetailView):
#     model = Blog
#     template_name = 'blog/blog_detail.html'
#     context_object_name = 'blog'

#     def get_object(self):
#         obj = super().get_object()
#         obj.viewerCount += 1
#         obj.save()
#         return obj
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         blog = self.get_object()
        
#         # Finding related blogs based on the same category
#         if blog.categories.exists():
#             related_blogs = Blog.objects.filter(categories__in=blog.categories.all()).exclude(id=blog.id).distinct()[:6]
#         else:
#             # If no categories, just get the latest 6 blogs excluding the current one
#             related_blogs = Blog.objects.all().exclude(id=blog.id)[:6]

#         context['related_blogs'] = related_blogs
#         return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Increment the viewer count
        if obj.visibility == 'public':
            obj.viewerCount += 1
            obj.save(update_fields=['viewerCount'])  # Save only the updated field for efficiency

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # blog = self.get_object()
        # Finding related blogs based on the same the latest 6
        related_blogs = Blog.objects.all()[:5]

        context['related_blogs'] = related_blogs
        return context



