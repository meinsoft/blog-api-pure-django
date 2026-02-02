from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.db.models import Q
from accounts.models import Category,Post,Comment
from accounts.decorators import api_login_required
from accounts.utils import parse_json_body,error_response



class CategoryListCreateView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def get(self,request):
		qs = Category.objects.all()
		data = {
		    "success": True,
		    "categories":[i.to_dict() for i in qs]
		}
		return JsonResponse(data)


	def post(self,request):
		data,error = parse_json_body(request)
		if(error):
			return error_response("VALIDATION_ERROR",error,status=404)

		if(not request.user.is_staff):
			return error_response("STUFF ERROR","YOU ARE NOT STUFF",status=400)

		name = data.get('name')
		description = data.get('description')

		slug = slugify(name, allow_unicode=True)
		if(Category.objects.filter(slug=slug).exists()):
			return error_response('VALIDATION_ERROR', 'Category already exists', status=400)

		category = Category.objects.create(name=name,description=description)

		return JsonResponse({
	        "success": True,
	        "message": "Category created",
	        "category": category.to_dict()
	    }, status=201)

class CategoryDetailView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get(self,request,slug):

		try:
			category = Category.objects.get(slug=slug)
		except Category.DoesNotExist:
			return error_response('NOT_FOUND', 'Category not found', status=404)

		return JsonResponse({
			"success": True,
			"category":category.to_dict()
		})

	def put(self,request,slug):

		if(not request.user.is_staff):
			return error_response("STUFF ERROR","YOU ARE NOT STUFF",status=400)

		data,error = parse_json_body(request)

		if(error):
			return error_response("VALIDATION_ERROR",error,status=404)


		try:
			category = Category.objects.get(slug=slug)
		except Category.DoesNotExist:
			return error_response('NOT_FOUND', 'Category not found', status=404)

		category.name = data.get('name',category.name)
		category.description = data.get('description',category.description)

		category.save()

		return JsonResponse({
			"success": True,
			"category":category.to_dict()
		})


	def delete(self,request,slug):
		if(not request.user.is_staff):
			return error_response("STUFF ERROR","YOU ARE NOT STUFF",status=400)

		try:
			category = Category.objects.get(slug=slug)
		except Category.DoesNotExist:
			return error_response('NOT_FOUND', 'Category not found', status=404)

		category.delete()


		return JsonResponse({
			"success": True,
			"category":category.to_dict()
		})

class PostListCreateView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)


	def get(self,request):
		posts = Post.objects.filter(status='published')

		q = request.GET.get('q')
		
		if(q):
		    posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

		category = request.GET.get('category')
		
		if(category):
		    posts = posts.filter(category__slug=category)

		author = request.GET.get('author')
		
		if(author):
		    posts = posts.filter(author__username=author)

		ordering = request.GET.get('ordering')
		if(ordering in ['created_at', '-created_at', 'title', '-title']):
		    posts = posts.order_by(ordering)

		end = int(request.GET.get('limit',10))
		start = int(request.GET.get('offset', 0))
		posts = posts[start:start+end]



		return JsonResponse({
			"success": True,
			"posts":[i.to_dict() for i in posts]
		})

	@method_decorator(api_login_required)
	def post(self,request):
		data,error = parse_json_body(request)
		if(error):
			return error_response("VALIDATION_ERROR",error,status=404)

		title = data.get('title')
		category_id = data.get('category_id')
		content = data.get('content')
		excerpt = data.get('excerpt')
		status = data.get('status')

		post = Post.objects.create(
		    title=title,
		    author=request.user,
		    category_id=category_id,
		    content=content,
		    excerpt=excerpt,
		    status=status
		)
		
		return JsonResponse({
	        "success": True,
	        "message": "Post created",
	        "post": post.to_dict()
	    }, status=201)

class PostDetailView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def get(self,request,slug):

		try:
			post = Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			return error_response('NOT_FOUND', 'Post not found', status=404) 

		return JsonResponse({
			"success": True,
			"post":post.to_dict(include_content=True)
		})

	def put(self,request,slug):
		data,error = parse_json_body(request)

		if(error):
			return error_response("VALIDATION_ERROR",error,status=404)

		try:
			post = Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			return error_response('NOT_FOUND', 'Post not found', status=404) 

		if(request.user!=post.author):
			return error_response('USER DOES NOT EQUAL', 'Not found', status=404) 

		post.title=data.get('title',post.title)
		post.content=data.get('content',post.content)

		post.save()

		return JsonResponse({
			"success": True,
			"category":post.to_dict()
		})

	def delete(self,request,slug):

		try:
			post = Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			return error_response('NOT_FOUND', 'Post not found', status=404)

		if(request.user!=post.author):
			return error_response("STUFF ERROR","YOU ARE NOT STUFF",status=400)

		data = post.to_dict()
		post.delete()
		return JsonResponse({
			"success": True, 
			"post": data
		})


class MyPostsView(View):

	@method_decorator(api_login_required)
	def get(self,request):
		posts = Post.objects.filter(author=request.user)

		return JsonResponse({
			"success": True,
			'posts':[i.to_dict() for i in posts]

		})


class CommentListCreateView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def get(self,request,slug):
		try:
			post = Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			return error_response('VALIDATION_ERROR', 'POST DOES NOT EXIST', status=400)

		comments = post.comments.all()

		return JsonResponse({
			"success": True,
			'comments':[i.to_dict() for i in comments]
		})

	@method_decorator(api_login_required)
	def post(self,request,slug):
		data,error = parse_json_body(request)
		if(error):
			return error_response("VALIDATION_ERROR",error,status=404)

		content = data.get('content')

		try:
			post=Post.objects.get(slug=slug)
		except Post.DoesNotExist:
			return error_response('NOT_FOUND', 'Post not found', status=404)

		comment = Comment.objects.create(post=post,author=request.user,content=content)

		return JsonResponse({
		    "success": True,
		    "message": "Comment created",
		    "comment": comment.to_dict()
		}, status=201)

class CommentDeleteView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	@method_decorator(api_login_required)
	def delete(self,request,id):
		try:
			comment = Comment.objects.get(id=id)
		except Comment.DoesNotExist:
			return error_response('NOT_FOUND', 'Comment not found', status=404)

		if(comment.author!=request.user):
			return error_response('FORBIDDEN', 'Not your comment', status=403)


		data = comment.to_dict()
		comment.delete()

		return JsonResponse({
	        "success": True,
	        "message": "Comment deleted",
	        "comment": data
	    })