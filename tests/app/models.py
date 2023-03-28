from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtailmodelchooser import Chooser, register_model_chooser
from wagtailmodelchooser.blocks import ModelChooserBlock


@register_model_chooser(icon="user")
class Author(models.Model, index.Indexed):
    name = models.CharField(max_length=255)

    search_fields = [
        index.SearchField("name"),
    ]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(Page):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel("author"),
    ]


@register_model_chooser
class BookChooser(Chooser):
    model = Book
    icon = "form"
    qs_hook_name = "remove_bad_books"

    def get_queryset(self, request):
        return Book.objects.exclude(title__startswith="BAD")


class ContentPage(Page):
    body = StreamField(
        [
            ("text", RichTextBlock()),
            ("author", ModelChooserBlock(Author)),
            ("book", ModelChooserBlock("app.Book")),
        ]
    )

    favourite_book = models.ForeignKey(
        Book, blank=True, null=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("favourite_book"),
    ]
