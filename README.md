# Pyramid Learning Journal

## Step 1

### Views/Routes Used:

* **def list_view(request):
    """Function that generates list of journal entries."""
    with open(os.path.join(STATIC, 'templates/public/index.html')) as f:
        return Response(f.read())**

* **def detail_view(request):
    """Function that generates single journal entry."""
    with open(os.path.join(STATIC, 'data/day-11.html')) as f:
        return Response(f.read())**

* **def create_view(request):
    """Function that generates new view."""
    with open(os.path.join(STATIC, 'templates/public/new_entry.html')) as f:
        return Response(f.read())**

* **def update_view(request):
    """Function that updates existing view."""
    with open(os.path.join(STATIC, 'templates/public/edit_entry.html')) as f:
        return Response(f.read())**


##### Pytest 2.6 & 3.6 Coverage Report - 100%, 100%


##[My Blog on Heroku](https://carson-tech-blog-fun-times.herokuapp.com/)

## Step 2

### Views/Routes Used:

* **@view_config(route_name="home", renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    return {
        "title": "Carson's Totally Amazing Journey Through The Land of Journal Entries",
        "journals": JOURNAL_ENTRIES[::-1]
    }**

* **@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    post_id = int(request.matchdict["id"])
    post = list(filter(lambda post: post["id"] == post_id, JOURNAL_ENTRIES))[0]
    return {
        "title": "Details",
        "post": post
    }**

* **@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
def create_view(request):
    """Function that generates single journal entry."""
    return {
        "title": "Create"
        }**

* **@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
def update_view(request):
    """Function that updates existing view."""
    post_id = int(request.matchdict['id'])
    post = list(filter(lambda post: post['id'] == post_id, JOURNAL_ENTRIES))[0]
    return{
        "title": "Update",
        "post": post
    }**

##### Pytest 2.6 & 3.6 Coverage Report - 100%, 100%


## Step 3

### Views/Routes Used:

* **@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
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
    }**

* **@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    post_id = int(request.matchdict["id"])
    post = list(filter(lambda post: post["id"] == post_id, JOURNAL_ENTRIES))[0]
    return {
        "title": "Details",
        "post": post
    }**

* **@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
def create_view(request):
    """Function that generates single journal entry."""
    return {
        "title": "Create"
    }**

* **@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
def update_view(request):
    """Function that updates existing view."""
    post_id = int(request.matchdict["id"])
    post = request.dbsession.query(Entry).get(post_id)
    return {
        "title": "Update",
        "post": post
    }**

##### Pytest 2.6 & 3.6 Coverage Report - 94%, 94%
