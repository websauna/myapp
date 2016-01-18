"""Place your admin resources in this file."""
from websauna.system.admin.modeladmin import model_admin
from websauna.system.admin.modeladmin import ModelAdmin

from . import models


@model_admin(traverse_id="question")
class QuestionAdmin(ModelAdmin):

    title = "Questions"

    singular_name = "question"
    plural_name = "questions"
    model = models.Question

    class Resource(ModelAdmin.Resource):

        def get_title(self):
            return self.get_object().question_text


@model_admin(traverse_id="choice")
class ChoiceAdmin(ModelAdmin):

    title = "Choices"

    singular_name = "choice"
    plural_name = "choices"
    model = models.Choice

    class Resource(ModelAdmin.Resource):

        def get_title(self):
            return self.get_object().choice_text

