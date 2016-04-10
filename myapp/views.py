from uuid import UUID

from myapp.models import Question
from myapp.models import Choice
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.session import check_csrf_token
from websauna.system.core import messages
from websauna.system.http import Request
from websauna.system.core.route import simple_route
from websauna.system.core.route import decode_uuid
from websauna.utils.slug import slug_to_uuid
from websauna.utils.slug import uuid_to_slug



# Configure view named home at path / using a template myapp/home.html
@simple_route("/", route_name="home", renderer="myapp/home.html")
def home(request: Request):
    """Render the site homepage."""
    latest_question_list = request.dbsession.query(Question).order_by(Question.published_at.desc()).all()[:5]
    return locals()


@simple_route("/questions/{question_uuid}/results", route_name="results", renderer="myapp/results.html", custom_predicates=(decode_uuid,))
def results(request: Request, question_uuid: UUID):
    question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
    if not question:
        raise HTTPNotFound()
    choices = question.choices.order_by(Choice.votes.desc())
    return locals()


@simple_route("/questions/{question_uuid}", route_name="detail", renderer="myapp/detail.html", custom_predicates=(decode_uuid,))
def detail(request: Request, question_uuid: UUID):
    question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
    if not question:
        raise HTTPNotFound()

    if request.method == "POST":

        # Check that CSRF token was good
        check_csrf_token(request)

        question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
        if not question:
            raise HTTPNotFound()

        if "choice" in request.POST:
            # Extracts the form choice and turn it to UUID object
            chosen_uuid = slug_to_uuid(request.POST['choice'])
            selected_choice = question.choices.filter_by(uuid=chosen_uuid).first()
            selected_choice.votes += 1
            messages.add(request, msg="Thank you for your vote", kind="success")
            return HTTPFound(request.route_url("results", question_uuid=uuid_to_slug(question.uuid)))
        else:
            error_message = "You did not select any choice."

    return locals()

