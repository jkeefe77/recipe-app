from django.db import models


# Create your models here.

genre_choices = (
    ("cl", "Classic"),
    ("ro", "Romantic"),
    ("co", "Comedy"),
    ("fa", "Fantasy"),
    ("ho", "Horror"),
    ("ed", "Educational"),
)

book_type_choices = (
    ("hc", "Hard cover"),
    ("eb", "E-Book"),
    ("ab", "Audiobook"),
)


class Book(models.Model):
    name = models.CharField(max_length=120)
    author_name = models.CharField(max_length=120)
    price = models.FloatField(help_text="in US dollars $")
    genre = models.CharField(max_length=12, choices=genre_choices, default="cl")
    book_type = models.CharField(max_length=12, choices=book_type_choices, default="hc")
    pic = models.ImageField(upload_to="books", default="no_picture.jpg")

    def __str__(self):
        return str(self.name)
