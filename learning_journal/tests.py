"""Functions that test server functions."""
import pytest
from pyramid import testing
# import transaction
from learning_journal.models import (
    Entry,
    # get_tm_session
)
from learning_journal.models.meta import Base


@pytest.fixture
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://postgres:Skrillexfan7@localhost:5432/test_db'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def testapp():
    """Create an instance of our app for testing."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        """ This function returns a Pyramid WSGI application.
        """
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_list_view_returns_html(dummy_request):
    """Function to test if list_view returns proper list of dictionaries."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_create_view_returns_title(dummy_request):
    """Update view response has file content."""
    from learning_journal.views.default import create_view
    request = dummy_request
    response = create_view(request)
    assert response['title'] == 'Create'


def test_update_view_returns_title(dummy_request):
    """Update view response has file content."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    request = dummy_request
    response = update_view(request)
    assert response['title'] == 'Update'


def test_response_is_instance_of_dict(dummy_request):
    """Function that tests database gets populated with model object."""
    from learning_journal.views.default import list_view
    new_entry = Entry(
        title='Learning Journal Fun Times',
        body='Today I learned all of the things',
        creation_date='November 2nd, 2017 7:47pm'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_model_gets_added_to_test_database(db_session):
    assert len(db_session.query(Entry).all()) == 0
    model = Entry(
        title='Learning Journal Fun Times',
        body='Today I learned all of the things',
        creation_date='November 2nd, 2017 7:47pm'
    )
    db_session.add(model)
    assert len(db_session.query(Entry).all()) == 1


def test_list_view_returns_correct_size_of_test_database(dummy_request):
    """Home view response matches database count."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry)
    assert len(response['entries']) == query.count()


def test_list_view_returns_empty_when_test_database_is_empty(dummy_request):
    """List view returns nothing when there is no data."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response['entries']) == 0


def test_detail_view_return_Entry_instance_and_values(dummy_request):
    """Update view response has file content."""
    from learning_journal.views.default import detail_view
    new_entry = Entry(
        title='Test',
        creation_date='01/23/45',
        body='Test should pass!'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.matchdict['id'] = 1
    request = dummy_request
    response = detail_view(request)
    assert str(response['post']) == '<Entry: {}>.format(self.title)'
    assert response['post'].title == 'Test'
    assert response['post'].creation_date == '01/23/45'
    assert response['post'].body == 'Test should pass!'


def test_detail_view_return_Entry_instance_and_vals_of_correct_model_id(dummy_request):
    """Update view response has file content."""
    from learning_journal.views.default import detail_view
    first_entry = Entry(
        title='Test',
        creation_date='01/23/45',
        body='Test should pass!'
    )
    second_entry = Entry(
        title='Test 2',
        creation_date='99/99/99',
        body='This entry is different!'
    )
    entries = [first_entry, second_entry]
    dummy_request.dbsession.add_all(entries)
    dummy_request.matchdict['id'] = 2
    request = dummy_request
    response = detail_view(request)
    assert len(dummy_request.dbsession.query(Entry).all()) == 2
    assert str(response['post']) == '<Entry: {}>.format(self.title)'
    assert response['post'].title == 'Test 2'
    assert response['post'].creation_date == '99/99/99'
    assert response['post'].body == 'This entry is different!'


def test_list_view_return_Entry_instance_and_only_two_values(dummy_request):
    """Update view response has file content."""
    from learning_journal.views.default import list_view
    new_entry = Entry(
        title='Test',
        creation_date='01/23/45'
    )
    dummy_request.dbsession.add(new_entry)
    request = dummy_request
    response = list_view(request)
    assert 'body' not in response['entries']
    assert str(response['entries']) == '[<Entry: {}>.format(self.title)]'
    assert response['entries'][0].title == 'Test'
    assert response['entries'][0].creation_date == '01/23/45'
