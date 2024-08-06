from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, UpdatePostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def CommentView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@login_required
def DeleteCommentView(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('article_detail', pk=comment.post.pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('article_detail', pk=post_pk)

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    
def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' ')).order_by('-post_date')
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})

def CategoryListView(request):
    category_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_list':category_list})
        
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context
        
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    
class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'update_post.html'
    
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')