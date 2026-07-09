from django.db import models
from django.core.exceptions import ValidationError
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from apps.core.models import BasePage
from apps.blocks.models import ContentStreamBlock


class FlexPage(BasePage):
    """
    A flexible page model that can be used for the homepage or other standard pages.
    It uses a StreamField for maximum content flexibility.
    """

    # Main content area as a StreamField for flexible content
    body = StreamField(
        ContentStreamBlock(),
        use_json_field=True,
        blank=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = BasePage.promote_panels
    settings_panels = BasePage.settings_panels

    # Allow only one instance at the root level
    parent_page_types = ["wagtailcore.Page", "pages.FlexPage"]

    # Specify the template for this page
    template = "pages/flex_page.html"

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"


@register_snippet
class Tag(models.Model):
    """
    A tag for organizing and filtering showcase entities.
    Tags can be assigned to any BaseEntityPage to categorize content.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]


class BaseEntityPage(FlexPage):
    """
    Abstract base page for all showcase entities with common fields.
    Entities can be tagged with a Tag for organization and filtering.
    This model provides common functionality for all showcase entity types.
    """

    tag = models.ForeignKey(
        "pages.Tag",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    URL_TYPE_CHOICES = [
        ("seo", "SEO-friendly Slug"),
        ("uuid", "UUID-based"),
    ]
    url_type_preference = models.CharField(
        max_length=10,
        choices=URL_TYPE_CHOICES,
        default="seo",
        help_text="Choose whether to display SEO-friendly URLs or UUID-based URLs",
    )

    # Add tag to content panels
    content_panels = FlexPage.content_panels + [
        FieldPanel("tag"),
        FieldPanel("url_type_preference"),
    ]

    template = "pages/entity_base.html"

    class Meta:
        abstract = True

    def get_url_parts(self, request=None, current_site=None):
        """
        Override URL generation to support both SEO-friendly and UUID-based URLs.
        """
        url_parts = super().get_url_parts(request, current_site)
        if url_parts is None:
            return None

        if self.url_type_preference == "uuid" and self.uuid:
            # Replace the slug part with the UUID
            site_id, root_url, page_path = url_parts
            # Split the path and replace the last part (slug) with UUID
            path_parts = page_path.rstrip("/").split("/")
            if path_parts:
                path_parts[-1] = str(self.uuid)
                page_path = "/".join(path_parts) + "/"
            return (site_id, root_url, page_path)

        return url_parts

    def get_uuid_url(self):
        """
        Get the UUID-based URL for this page.
        """
        if self.uuid:
            # Get the parent URL and append the UUID
            if self.get_parent():
                parent_url = self.get_parent().specific.get_url()
                return f"{parent_url}uuid/{self.uuid}/"
            return f"/uuid/{self.uuid}/"
        return "#"


class ProjectPage(BaseEntityPage):
    """
    A project page that may or may not have child pages.
    """

    has_page = models.BooleanField(
        default=False, help_text="Check this box if this project has its own page"
    )

    content_panels = BaseEntityPage.content_panels + [
        FieldPanel("has_page"),
    ]

    parent_page_types = ["pages.ProjectShowcasePage"]
    subpage_types = ["pages.FlexPage"]  # Only if has_page is True
    template = "pages/project_page.html"

    def clean(self):
        # If has_page is False, ensure no child pages exist
        if not self.has_page and self.get_children().exists():
            raise ValidationError("Cannot have child pages when 'has_page' is False.")

    def save(self, *args, **kwargs):
        # Update subpage_types based on has_page value
        if self.has_page:
            self.subpage_types = ["pages.FlexPage"]
        else:
            self.subpage_types = []
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Project Page"
        verbose_name_plural = "Project Pages"


class ServicePage(BaseEntityPage):
    """
    A service page that always has child pages.
    """

    content_panels = (
        BaseEntityPage.content_panels
        + [
            # Services typically don't have links in list view, but you can add them here if needed
        ]
    )

    parent_page_types = ["pages.ServiceShowcasePage"]
    subpage_types = ["pages.FlexPage"]
    template = "pages/service_page.html"

    def save(self, *args, **kwargs):
        # Services always have pages, so we don't need to modify subpage_types
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Service Page"
        verbose_name_plural = "Service Pages"


class PortfolioItemPage(BaseEntityPage):
    """
    A portfolio item page that always has child pages and includes an image.
    """

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    content_panels = BaseEntityPage.content_panels + [
        FieldPanel("image"),
    ]

    parent_page_types = ["pages.PortfolioShowcasePage"]
    subpage_types = ["pages.FlexPage"]
    template = "pages/portfolio_item_page.html"

    class Meta:
        verbose_name = "Portfolio Item Page"
        verbose_name_plural = "Portfolio Item Pages"


class AbstractShowcasePage(BasePage):
    """
    Abstract base page for showcasing different types of entities.
    Editors can create sections and explicitly assign items to each section.
    """

    # Introduction text for the page
    introduction = models.TextField(
        blank=True, help_text="Optional introduction text for the showcase page"
    )

    class Meta:
        abstract = True
        verbose_name = "Abstract Showcase Page"
        verbose_name_plural = "Abstract Showcase Pages"


class ProjectShowcasePage(AbstractShowcasePage):
    """
    A page that showcases projects.
    """

    content_panels = AbstractShowcasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel(
            "project_sections",
            label="Sections",
            help_text="Add and order sections to display on this page",
        ),
    ]

    template = "pages/project_showcase_page.html"
    parent_page_types = ["wagtailcore.Page", "pages.FlexPage"]
    subpage_types = ["pages.ProjectPage"]

    class Meta:
        verbose_name = "Project Showcase Page"
        verbose_name_plural = "Project Showcase Pages"


class ServiceShowcasePage(AbstractShowcasePage):
    """
    A page that showcases services.
    """

    content_panels = AbstractShowcasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel(
            "service_sections",
            label="Sections",
            help_text="Add and order sections to display on this page",
        ),
    ]

    template = "pages/service_showcase_page.html"
    parent_page_types = ["wagtailcore.Page", "pages.FlexPage"]
    subpage_types = ["pages.ServicePage"]

    class Meta:
        verbose_name = "Service Showcase Page"
        verbose_name_plural = "Service Showcase Pages"


class PortfolioShowcasePage(AbstractShowcasePage):
    """
    A page that showcases portfolio items.
    """

    content_panels = AbstractShowcasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel(
            "portfolio_sections",
            label="Sections",
            help_text="Add and order sections to display on this page",
        ),
    ]

    template = "pages/portfolio_showcase_page.html"
    parent_page_types = ["wagtailcore.Page", "pages.FlexPage"]
    subpage_types = ["pages.PortfolioItemPage"]

    class Meta:
        verbose_name = "Portfolio Showcase Page"
        verbose_name_plural = "Portfolio Showcase Pages"


class ResourceShowcasePage(AbstractShowcasePage):
    """
    A page that showcases resources.
    """

    content_panels = AbstractShowcasePage.content_panels + [
        FieldPanel("introduction"),
        InlinePanel(
            "resource_sections",
            label="Sections",
            help_text="Add and order sections to display on this page",
        ),
    ]

    template = "pages/resource_showcase_page.html"
    parent_page_types = ["wagtailcore.Page", "pages.FlexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Resource Showcase Page"
        verbose_name_plural = "Resource Showcase Pages"


class AbstractShowcaseSection(ClusterableModel, Orderable):
    """
    Abstract base model for showcase sections. Editors explicitly assign items to each section.
    """

    # Section heading
    heading = models.CharField(max_length=200, help_text="Heading for this section")

    # Custom description for the section
    description = models.TextField(
        blank=True, help_text="Optional description for this section"
    )

    panels = [
        FieldPanel("heading"),
        FieldPanel("description"),
        InlinePanel("items", label="Items", help_text="Add items to this section"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.showcase_page.title} -> {self.heading}"

    def get_items(self):
        """
        Get items explicitly assigned to this section.
        """
        return self.items.all()


class ProjectShowcaseSection(AbstractShowcaseSection):
    """
    A section on the project showcase page.
    """

    showcase_page = ParentalKey(
        "pages.ProjectShowcasePage",
        on_delete=models.CASCADE,
        related_name="project_sections",
    )


class ServiceShowcaseSection(AbstractShowcaseSection):
    """
    A section on the service showcase page.
    """

    showcase_page = ParentalKey(
        "pages.ServiceShowcasePage",
        on_delete=models.CASCADE,
        related_name="service_sections",
    )


class PortfolioShowcaseSection(AbstractShowcaseSection):
    """
    A section on the portfolio showcase page.
    """

    showcase_page = ParentalKey(
        "pages.PortfolioShowcasePage",
        on_delete=models.CASCADE,
        related_name="portfolio_sections",
    )


class ResourceShowcaseSection(AbstractShowcaseSection):
    """
    A section on the resource showcase page.
    """

    showcase_page = ParentalKey(
        "pages.ResourceShowcasePage",
        on_delete=models.CASCADE,
        related_name="resource_sections",
    )


class AbstractShowcaseItem(ClusterableModel, Orderable):
    """
    Abstract base model for showcase items. Each item has its own title, description, and links,
    and can optionally be attached to a page.
    """

    # Item fields
    title = models.CharField(
        max_length=200, help_text="Title for this item", default="Untitled"
    )
    description = models.TextField(blank=True, help_text="Description for this item")

    # Optional page reference
    page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optional page to link to",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("page"),
        InlinePanel("links", label="Links", help_text="Links for this item"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.section.heading} -> {self.title}"

    def get_links(self):
        """
        Get links for this item.
        """
        return self.links.all()


class ProjectShowcaseItem(AbstractShowcaseItem):
    """
    An item in a project showcase section.
    """

    section = ParentalKey(
        "pages.ProjectShowcaseSection", on_delete=models.CASCADE, related_name="items"
    )


class ServiceShowcaseItem(AbstractShowcaseItem):
    """
    An item in a service showcase section.
    """

    section = ParentalKey(
        "pages.ServiceShowcaseSection", on_delete=models.CASCADE, related_name="items"
    )


class PortfolioShowcaseItem(AbstractShowcaseItem):
    """
    An item in a portfolio showcase section. Includes an image field.
    """

    # Image field specific to portfolio items
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    section = ParentalKey(
        "pages.PortfolioShowcaseSection", on_delete=models.CASCADE, related_name="items"
    )

    panels = AbstractShowcaseItem.panels + [
        FieldPanel("image"),
    ]


class ResourceShowcaseItem(AbstractShowcaseItem):
    """
    An item in a resource showcase section. Resources don't have pages to link to.
    """

    section = ParentalKey(
        "pages.ResourceShowcaseSection", on_delete=models.CASCADE, related_name="items"
    )

    # Override the page field to make it non-editable for resources
    page = None

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("links", label="Links", help_text="Links for this item"),
    ]


class AbstractShowcaseItemLink(Orderable):
    """
    Abstract base model for showcase item links.
    """

    LINK_TARGET_CHOICES = [
        ("_self", "Same Window"),
        ("_blank", "New Window"),
    ]

    title = models.CharField(max_length=200)
    url = models.URLField()
    target = models.CharField(
        max_length=10, choices=LINK_TARGET_CHOICES, default="_self"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("target"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.item.title} -> {self.title}"


class ProjectShowcaseItemLink(AbstractShowcaseItemLink):
    """
    Links for a project showcase item.
    """

    item = ParentalKey(
        "pages.ProjectShowcaseItem", on_delete=models.CASCADE, related_name="links"
    )


class ServiceShowcaseItemLink(AbstractShowcaseItemLink):
    """
    Links for a service showcase item.
    """

    item = ParentalKey(
        "pages.ServiceShowcaseItem", on_delete=models.CASCADE, related_name="links"
    )


class PortfolioShowcaseItemLink(AbstractShowcaseItemLink):
    """
    Links for a portfolio showcase item.
    """

    item = ParentalKey(
        "pages.PortfolioShowcaseItem", on_delete=models.CASCADE, related_name="links"
    )


class ResourceShowcaseItemLink(AbstractShowcaseItemLink):
    """
    Links for a resource showcase item.
    """

    item = ParentalKey(
        "pages.ResourceShowcaseItem", on_delete=models.CASCADE, related_name="links"
    )
