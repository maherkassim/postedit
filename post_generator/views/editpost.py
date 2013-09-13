from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from post_generator.models.post import Post
from post_generator.models.language import Language
from post_generator.models.dictionaryitem import DictionaryItem

def NewPost(request):
	languages = Language.objects.all()
	lang_list = []
	for lang in languages:
		lang_list.append(lang.full_name)
	
	title_obj = DictionaryItem.objects.get(english="New Post")
	print_obj = DictionaryItem.objects.get(english="Print Recipe")
	print_img_obj = DictionaryItem.objects.get(english="Print Recipe with Photos")
	print_dict = {}
	print_img_dict = {}
	
	for obj in [print_obj, print_img_obj]:
		for lang in lang_list:
			if obj.id == print_obj.id:
				print_dict[lang] = obj.__dict__[lang]
			else:
				print_img_dict[lang] = obj.__dict__[lang]
	
	post_obj = Post(link="http://xawaash.com/?p=", title=title_obj, pub_date=timezone.now())
	post_obj.save()
	
	context = {
		'post':             post_obj,
		'tab_sides':        ['left', 'right'],
		'lang_list':        lang_list,
		'print_def':        print_dict,
		'print_img_def':    print_img_dict,
	}
	return render(request, 'post_generator/new.html', context)

def EditPost(request, post_id):
	model = Post
	template_name = 'post_generator/edit.html'
	
def UpdatePost(request, post_id):
	post_obj = get_object_or_404(Post, pk=post_id)
	return HttpResponseRedirect(reverse('post_generator:detail', args=(post_obj.id,)))

