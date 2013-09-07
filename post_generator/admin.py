from django.contrib import admin
from post_generator.models.language import Language
from post_generator.models.dictionaryitem import DictionaryItem
from post_generator.models.post import Post
from post_generator.models.tab import Tab
from post_generator.models.textblock import TextBlock
from post_generator.models.header import Header
from post_generator.models.ingredient import Ingredient
from post_generator.models.direction import Direction
from post_generator.models.image import Image
from post_generator.models.video import Video

admin.site.register(Language)
admin.site.register(DictionaryItem)
admin.site.register(Post)
admin.site.register(Tab)
admin.site.register(TextBlock)
admin.site.register(Header)
admin.site.register(Ingredient)
admin.site.register(Direction)
admin.site.register(Image)
admin.site.register(Video)