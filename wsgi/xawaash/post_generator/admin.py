import reversion

from django.contrib import admin
from post_generator.models import Language, DictionaryItem, Post, TextBlock, Image, Video, IngredientBlock, DirectionBlock, Ingredient, Direction, ConversionType, Conversion, ConversionIngredient

# Post Model Admin
class VideoInline(admin.TabularInline):
    model = Video
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class TextBlockInline(admin.TabularInline):
    model = TextBlock
    extra = 0

class IngredientBlockInline(admin.TabularInline):
    model = IngredientBlock
    extra = 0

class DirectionBlockInline(admin.TabularInline):
    model = DirectionBlock
    extra = 0

class PostAdmin(reversion.VersionAdmin):
    fieldsets = [
        (None,  {'fields': []}),
    ]
    inlines = [
        VideoInline,
        ImageInline,
        TextBlockInline,
        IngredientBlockInline,
        DirectionBlockInline,
    ]
    list_display = ('title','link')
    list_filter = ['pub_date']

# Image Model Admin
class ImageAdmin(reversion.VersionAdmin):
    list_display = ('post', 'link', 'width', 'height',
                    'english', 'somali', 'french', 'arabic',
                    'wordpress_image_id')

# Video Model Admin
class VideoAdmin(reversion.VersionAdmin):
    list_display = ('post', 'link', 'width', 'height')

# TextBlock Model Admin
class TextBlockAdmin(reversion.VersionAdmin):
    list_display = ('post', 'english', 'header')

# Direction Model Admin
class DirectionAdmin(reversion.VersionAdmin):
    list_display = ('direction_block', 'english')

# Ingredient Model Admin
class IngredientAdmin(reversion.VersionAdmin):
    list_display = ('ingredient_block', 'name',
                    'quantity', 'quantity_units',
                    'intl', 'intl_units',
                    'english')
    
# DictionaryItem Model Admin
class DictionaryItemAdmin(reversion.VersionAdmin):
    list_display = ('english', 'somali', 'french', 'french_feminine',
                    'arabic', 'image', 'link')

# DirectionBlock Admin
class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 0

class DirectionBlockAdmin(reversion.VersionAdmin):
    list_display = ('post', 'header')
    inlines = [DirectionInline, ]

# IngredientBlock Admin
class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0

class IngredientBlockAdmin(reversion.VersionAdmin):
    list_display = ('post', 'header')
    inlines = [IngredientInline, ]

# General Reversion Admin
class ReversionAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Language)
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ReversionAdmin)
admin.site.register(Video, ReversionAdmin)
admin.site.register(TextBlock, ReversionAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(DictionaryItem, DictionaryItemAdmin)
admin.site.register(IngredientBlock, IngredientBlockAdmin)
admin.site.register(DirectionBlock, DirectionBlockAdmin)
admin.site.register(Conversion, ReversionAdmin)
admin.site.register(ConversionType, ReversionAdmin)
admin.site.register(ConversionIngredient, ReversionAdmin)
