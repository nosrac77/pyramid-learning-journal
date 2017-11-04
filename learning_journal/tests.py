"""Functions that test server functions."""
import pytest


@pytest.fixture
def dummy_request():
    from pyramid import testing
    return testing.DummyRequest()


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


def test_layout_root_has_text_in_footer(testapp):
    """Test that the contents of the root page contains <footer>."""
    response = testapp.get('/', status=200)
    html = response.html
    print(html.find("footer"))
    assert 'Carson Newton' in html.find("footer").text


def test_root_content_contains_h4(testapp):
    """Test that the contents of the root page contains as many <footer>."""
    from learning_journal.data.journal_entries import JOURNAL_ENTRIES
    response = testapp.get('/', status=200)
    html = response.html
    assert len(JOURNAL_ENTRIES) == len(html.findAll("h4"))


def test_reponse_to_detail_view_returns_proper_h4_title(testapp):
    """Test that the contents of the root page contains as many <footer>."""
    response = testapp.get('/journal/1', status=200)
    print(response)
    assert response.html.find('h4').text == 'Learning Journal Day 1'


def test_list_view_returns_html(dummy_request):
    """Function to test if list_view returns proper list of dictionaries."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_proper_amount_of_content(dummy_request):
    """Home view response has file content."""
    from learning_journal.data.journal_entries import JOURNAL_ENTRIES
    from learning_journal.views.default import list_view
    request = dummy_request
    response = list_view(request)
    assert len(response['journals']) == len(JOURNAL_ENTRIES)


def test_create_view_returns_title(dummy_request):
    """Create view response has file content."""
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
