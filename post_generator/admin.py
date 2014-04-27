from django.contrib import admin
from post_generator.models import Language, DictionaryItem, Post, TextBlock, Image, Video, IngredientBlock, DirectionBlock, Ingredient, Direction, ConversionType, Conversion, ConversionIngredient

class VideoInline(admin.TabularInline):
    model = Video

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class TextBlockInline(admin.TabularInline):
    model = TextBlock

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3

class IngredientBlockInline(admin.TabularInline):
    model = IngredientBlock
    inlines = [ IngredientInline, ]

class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 3

class DirectionBlockInline(admin.TabularInline):
    model = DirectionBlock
    inlines = [ DirectionInline, ]

class ConversionTypeInline(admin.TabularInline):
    model = ConversionType

class ConversionInline(admin.TabularInline):
    model = Conversion

class ConversionIngredientInline(admin.TabularInline):
    model = ConversionIngredient

class PostAdmin(admin.ModelAdmin):
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

admin.site.register(Language)
admin.site.register(DictionaryItem)
admin.site.register(Post)
admin.site.register(TextBlock)
admin.site.register(IngredientBlock)
admin.site.register(Ingredient)
admin.site.register(DirectionBlock)
admin.site.register(Direction)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(ConversionType)
admin.site.register(Conversion)
admin.site.register(ConversionIngredient)
