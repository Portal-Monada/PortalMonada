from django.db import models
from django.utils import timezone
import json

# Create your models here.
class Menu(models.Model):

    # enum MenuType
    class MenuType(models.TextChoices):
        LINK = 'link', 'Link'
        DROPDOWN = 'dropdown', 'Dropdown'
        SEPARATOR = 'separator', 'Separator'
        BUTTON = 'button', 'Button'

    # enum TargetType
    class TargetType(models.TextChoices):
        SELF = '_self', 'Same tab'
        BLANK = '_blank', 'New tab'

    # basic fields
    title = models.CharField(max_length=100)
    url = models.SlugField(max_length=255)
    icon = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    # Type and behavior
    menu_type = models.CharField(max_length=100)

    # Self-referencing for submenus
    parent_menu = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='submenus',
        blank=True,
        null=True,
        verbose_name='Parent Menu',
        help_text='Parent menu for submenus'
    )

    target = models.CharField(
        max_length=10,
        choices=TargetType.choices,
        default=TargetType.SELF,
        verbose_name='Target'
    )

    # Status and highlighting
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Whether the item is active/visible'
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name='Featured',
        help_text='For special items (ex: "Promotion")'
    )

    # Access control
    allowed_roles = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Allowed Roles',
        help_text='Roles that can see this menu (ex: ["admin", "user"])'
    )

    required_permissions = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Required Permissions',
        help_text='Specific permissions required'
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        db_table = 'menus'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['parent_menu']),
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        """Custom validations"""
        if self.menu_type == self.MenuType.LINK and not self.url:
            raise ValidationError({
                'url': 'Menu of type Link must have a URL defined.'
            })

        if self.menu_type == self.MenuType.SEPARATOR and self.url:
            raise ValidationError({
                'url': 'Menu of type Separator should not have a URL.'
            })

        if self.parent_menu and self.parent_menu.menu_type != self.MenuType.DROPDOWN:
            raise ValidationError({
                'parent_menu': 'Parent menu must be of type Dropdown.'
            })

        if self.parent_menu == self:
            raise ValidationError({
                'parent_menu': 'A menu cannot be its own parent.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def has_submenus(self):
        """Check if menu has submenus"""
        return self.submenus.filter(is_active=True).exists()

    def get_active_submenus(self):
        """Return active submenus ordered"""
        return self.submenus.filter(is_active=True).order_by('order')

    def user_has_access(self, user):
        """Check if user has access to menu"""
        if not self.allowed_roles:
            return True

        # Adapt this to your role/permission system
        try:
            roles = json.loads(self.allowed_roles) if isinstance(self.allowed_roles, str) else self.allowed_roles
            user_roles = getattr(user, 'roles', [])

            # Role verification logic (adapt to your implementation)
            if hasattr(user, 'is_superuser') and user.is_superuser:
                return True

            return any(role in user_roles for role in roles)

        except (json.JSONDecodeError, TypeError):
                return True

    def is_dropdown(self):
        """Check if it's a dropdown"""
        return self.menu_type == self.MenuType.DROPDOWN

    def is_link(self):
        """Check if it's a link"""
        return self.menu_type == self.MenuType.LINK

    def is_separator(self):
        """Check if it's a separator"""
        return self.menu_type == self.MenuType.SEPARATOR

    def is_button(self):
        """Check if it's a button"""
        return self.menu_type == self.MenuType.BUTTON


class MenuManager(models.Manager):
    def main_menus(self):
        """Return active main menus (without parent)"""
        return self.filter(parent_menu__isnull=True, is_active=True).order_by('order')

    def menus_for_user(self, user):
        """Return menus that user has access to"""
        menus = self.main_menus()
        return [menu for menu in menus if menu.user_has_access(user)]

    def menu_by_title(self, title):
        """Find menu by title"""
        return self.filter(title__iexact=title, is_active=True).first()

# Add manager to model
Menu.objects = MenuManager()