from .template_view_with_context import TemplateViewWithContext


class StyleGuideView(TemplateViewWithContext):
    template_name = "pages/style_guide.html"
    page_title = "Style Guide"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{"url": "/style-guide", "text": "Style guide"}, {"text": "Example breadcrumbs"}]
        context["feedback_survey_type"] = "support"
        context["menu_items"] = [
            {"label": "Colours", "href": "#colours"},
            {
                "label": "Components",
                "href": "#components",
                "children": [
                    {"label": "Character count", "href": "#character-count"},
                    {"label": "Checkboxes", "href": "#checkboxes"},
                    {"label": "Details box", "href": "#details-box"},
                    {"label": "Important information box", "href": "#important-information-box"},
                    {"label": "Judgment header", "href": "#judgment-header"},
                    {"label": "Notification banners", "href": "#notification-banners"},
                    {"label": "Radios", "href": "#radios"},
                    {"label": "Summary card", "href": "#summary-card"},
                    {"label": "Text input", "href": "#text-input"},
                ],
            },
            {
                "label": "Spacing",
                "href": "#spacing",
            },
            {
                "label": "Typography",
                "href": "#typography",
                "children": [
                    {"label": "Font family", "href": "#font-family"},
                    {"label": "Font sizes", "href": "#font-sizes"},
                    {"label": "Font weights", "href": "#font-weights"},
                    {"label": "Headings", "href": "#headings"},
                    {"label": "Line heights", "href": "#line-heights"},
                ],
            },
        ]
        return context