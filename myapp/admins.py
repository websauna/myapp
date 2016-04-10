"""Admin resource registrations for your app."""

from websauna.system.admin.modeladmin import model_admin
from websauna.system.admin.modeladmin import ModelAdmin

# Import our models
from . import models


@model_admin(traverse_id="question")
class QuestionAdmin(ModelAdmin):
    """Admin resource for question model.

    This class declares a resource for question model admin root folder with listing and add views.
    """

    #: Label as shown in admin
    title = "Questions"

    #: Used in admin listings etc. user visible messages
    #: TODO: This mechanism will be phased out in the future versions with gettext or similar replacement for languages that have plulars one, two, many
    singular_name = "question"
    plural_name = "questions"

    #: Which models this model admin controls
    model = models.Question

    class Resource(ModelAdmin.Resource):
        """Declare resource for each individual question.

        View, edit and delete views are registered against this resource.
        """

        def get_title(self):
            """What we show as the item title in question listing."""
            return self.get_object().question_text


@model_admin(traverse_id="choice")
class ChoiceAdmin(ModelAdmin):
    """Admin resource for choice model."""

    title = "Choices"

    singular_name = "choice"
    plural_name = "choices"
    model = models.Choice

    class Resource(ModelAdmin.Resource):

        def get_title(self):
            return self.get_object().choice_text

