from django.db import models
from django.utils.translation import gettext_lazy as _

class Employee(models.Model):
    class Role(models.TextChoices):
        MANAGER = 'Manager', _('Manager')
        EDITOR = 'Editor', _('Editor')
        OTHER = 'Other', _('Other')

    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    role = models.CharField(_("Role"), max_length=20, choices=Role.choices)
    email = models.EmailField(_("Email"), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    address = models.CharField(_("Address"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Author(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    biography = models.TextField(_("Biography"), blank=True)
    email = models.EmailField(_("Email"), unique=True, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    authors = models.ManyToManyField(
        Author,
        through='BookAuthor',
        verbose_name=_("Authors"),
        related_name='books'
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name=_("Book"),
        related_name='book_authors'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
        related_name='book_authors'
    )
    position_on_cover = models.PositiveIntegerField(_("Position on Cover"))
    royalty_percentage = models.DecimalField(
        _("Royalty Percentage"),
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        unique_together = ('book', 'author')
        ordering = ['position_on_cover']
        verbose_name = _("Book Author")
        verbose_name_plural = _("Book Authors")

    def __str__(self):
        return f"{self.author} - {self.book.title} (Order {self.self.position_on_cover})"

class Edition(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='editions',
        verbose_name=_("Book")
    )
    edition_number = models.PositiveIntegerField(_("Edition Number"))
    publication_date = models.DateField(_("Publication Date"))
    number_of_pages = models.PositiveIntegerField(_("Number of Pages"))
    has_illustrations = models.BooleanField(_("Has Illustrations"), default=False)
    editors = models.ManyToManyField(
        'Employee',
        through='EditionEditor',
        related_name='edited_editions',
        verbose_name=_("Editors"),
        limit_choices_to={'role': Employee.Role.EDITOR}
    )

    class Meta:
        unique_together = ('book', 'edition_number')
        verbose_name = _("Edition")
        verbose_name_plural = _("Editions")

    def __str__(self):
        return f"{self.book.title} - Edition {self.edition_number}"

class Contract(models.Model):
    edition = models.OneToOneField(
        Edition,
        on_delete=models.CASCADE,
        verbose_name=_("Edition"),
        related_name='contract'
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Employee.Role.MANAGER},
        verbose_name=_("Manager"),
        related_name='contracts'
    )
    date_signed = models.DateField(_("Date Signed"))

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")

    def __str__(self):
        return f"Contract for {self.edition}"

class EditionEditor(models.Model):
    edition = models.ForeignKey(
        Edition,
        on_delete=models.CASCADE,
        verbose_name=_("Edition"),
        related_name='edition_editors'
    )
    editor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Employee.Role.EDITOR},
        verbose_name=_("Editor"),
        related_name='edition_editors'
    )
    is_responsible_editor = models.BooleanField(_("Responsible Editor"), default=False)

    class Meta:
        unique_together = ('edition', 'editor')
        verbose_name = _("Edition Editor")
        verbose_name_plural = _("Edition Editors")

    def __str__(self):
        role = _('Responsible Editor') if self.is_responsible_editor else _('Editor')
        return f"{self.editor} - {self.edition} ({role})"

class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    address = models.CharField(_("Address"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_("Customer"),
        related_name='orders'
    )
    date_ordered = models.DateField(_("Date Ordered"))
    items = models.ManyToManyField(
        Edition,
        through='OrderItem',
        verbose_name=_("Items"),
        related_name='orders'
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        related_name='order_items'
    )
    edition = models.ForeignKey(
        Edition,
        on_delete=models.CASCADE,
        verbose_name=_("Edition"),
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        unique_together = ('order', 'edition')

    def __str__(self):
        return f"{self.quantity} x {self.edition}"