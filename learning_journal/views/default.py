"""Module that contains callable server functions."""
from pyramid.view import view_config
from learning_journal.models.mymodel import Entry


@view_config(route_name="home", renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    entries = request.dbsession.query(Entry).all()
    return {
        'title': 'All Entries',
        'entries': entries
    }


@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    from pyramid.httpexceptions import HTTPNotFound
    post_id = int(request.matchdict["id"])
    post = request.dbsession.query(Entry).get(post_id)
    if post is None:
        raise HTTPNotFound
    return {
        "title": "Details",
        "post": post
    }


@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
def update_view(request):
    """Function that generates single journal entry."""
    from pyramid.httpexceptions import HTTPFound
    post_id = int(request.matchdict["id"])
    if request.method == 'GET':
        post = request.dbsession.query(Entry).get(post_id)
        return {
           "title": "Update",
           "post": post
        }

    if request.method == 'POST' and request.POST:
        request.dbsession.query(Entry).filter_by(id=post_id).update(
            {
                "title": request.POST['title'],
                "body": request.POST['body'],
                "creation_date": request.POST['creation_date']
            }
        )
        request.dbsession.flush()
        return HTTPFound(request.route_url('details', id=post_id))


@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
def create_view(request):
    """Function that updates existing view."""
    from pyramid.httpexceptions import HTTPFound
    if request.method == 'GET':
        return {
            "title": "Create"
        }

    if request.method == 'POST' and request.POST:
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
            creation_date=request.POST['creation_date']
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))
