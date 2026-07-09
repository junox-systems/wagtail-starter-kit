import uuid
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtailseo.models import SeoMixin
from wagtailcache.cache import WagtailCacheMixin


class BasePage(WagtailCacheMixin, SeoMixin, Page):
    """
    Abstract base page model that defines common fields and
    functionality that should be shared across all page types.
    Inherits from SeoMixin to provide SEO functionality via wagtail-seo.
    """

    cache_control = "public, max-age=300, stale-while-revalidate=60"

    # Add a UUID field to provide a stable identifier for all page types
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Make this an abstract model
    class Meta:
        abstract = True

    # SEO settings specific to this project
    # We're using the SeoMixin from wagtail-seo which provides:
    # - seo_title (inherits from Wagtail Page)
    # - search_description (inherits from Wagtail Page)
    # - canonical_url
    # - og_image
    # Plus structured data, social meta tags, etc.

    # Add any additional fields that are common to all pages but not covered by SeoMixin
    # For example, you might want a custom field for page-specific structured data
    custom_structured_data = models.TextField(
        blank=True,
        null=True,
        help_text="Additional structured data for this page in JSON-LD format.",
    )

    # Content panels - these will be shown in the content tab
    base_content_panels = Page.content_panels + []

    # Promote panels - these will be shown in the promote tab
    base_promote_panels = [
        FieldPanel("custom_structured_data"),
    ]

    # Settings panels - these will be shown in the settings tab
    base_settings_panels = (
        Page.settings_panels
        + [
            # Add any settings panels that are common to all pages
        ]
    )

    # Combine all panels
    content_panels = base_content_panels
    promote_panels = SeoMixin.seo_meta_panels + base_promote_panels
    settings_panels = base_settings_panels
