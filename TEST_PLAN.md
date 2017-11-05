# Plans for testing Carson's Learning Journal

###### In this file I outline my thought process surrounding how to test my view functions and model objects. Below my functions are lists of ways I envision testing them, as well as what I'll be testing for.

## Tests for detail_view function

**@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
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

Since I know this function returns exactly what it's always returned, I can test for some of the same things:

* Returns dictionary with a title of "Details"
* Returns dictionary with a key of 'post', which is a model object containing "title", "creation_date", "body".
* Raises an HTTPNotFound if the database session query returns None
* Returns an instance of an Entry class model object
* Returns the correct model object given an id within the database that matches, which would have correct "title", "body", and "creation_date" values.


## Tests for list_view function

**@view_config(route_name="home", renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    entries = request.dbsession.query(Entry).all()
    return {
        'title': 'All Entries',
        'entries': entries
    }**

Since I know this function returns exactly what it's always returned, I can test for some of the same things:

* Returns dictionary with a title of "All Entries"
* Returns dictionary with a key of 'post', which is a list of model objects only containing "title", "creation_date", as "body" should not be included in the list of journal entries displayed to the user.
* Returns instances of Entry class model objects
* Returns the correct number of model objects from within the database (as many as there are entries in the 'entries' table), which would have correct "title" and "creation_date" values.


## Tests for update_view function

**@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
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
        return HTTPFound(request.route_url('details', id=post_id))**

Since this function is a new addition, I'll have to test for some new things as well as common things all view functions share:

**If method is GET**

* Returns dictionary with a title of "Update"
* Returns dictionary with a key of 'post', which is a model object containing "title", "creation_date", and "body".
* Returns an instance of an Entry class model object
* Returns the correct number model object from within the database, which would have correct "title", "creation_date", and "body" values.

**If method is POST**

* Updates existing model object at the correct id with new values
* Does not update existing model object if any values are null values
* Does not alter the overall length of model objects in the database


## Tests for create_view function

**@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
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
        return HTTPFound(request.route_url('home'))**

Since this function has some new functionality, I'll have to test for some new things as well as common things all view functions share:

**If method is GET**

* Returns dictionary with a title of "Create"

**If method is POST**

* Creates a new model object that gets added to the database
* Does not create model object if any values are null values
* Alters the overall length of model objects in the database since a new addition has been made


#### Misc. Thoughts on Testing

* For the **detail_view** function - I didn't know how to test for raising HTTPNotFound if the id didn't match any existing database model object. I tried using a with pytest.raises assertion, as well as a try/except, to no avail.
* For the **create_view** and **update_view** functions - I didn't know how to test for the HTTPFound redirect. I saw multiple descriptions of how to do it in the class notes and tried to emulate them. Examples belows.

**def test_new_expense_redirects_to_home(testapp, empty_db):
    """When redirection is followed, result is home page."""
    new_entry = {
        "title": 'New Entry',
        "creation_date": '99/99/99',
        "body": 'This is new!'
    }
    response = testapp.post('/create', new_entry)
    home_path = testapp.app.routes_mapper.get_route('home').path
    assert response.location == 'https://carson-tech-blog-fun-times.herokuapp.com/' + home_path**


**def test_new_entry_redirection_lands_on_home(testapp, empty_db):
    """When redirection is followed, result is home page."""
    new_entry = {
        "title": 'New Entry',
        "creation_date": '99/99/99',
        "body": 'This is new!'
    }
    response = testapp.post('https://carson-tech-blog-fun-times.herokuapp.com/create', new_entry)
    next_response = response.follow()
    home_response = testapp.get('/')
    assert next_response.text == home_response.text**

After testing them multiple ways, I decided to remove the empty_db fixture and remove the tests altogether.
