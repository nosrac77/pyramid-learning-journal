"""Functions that give application secure login access."""
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated, Allow
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import SignedCookieSessionFactory
import os


def includeme(config):
    """Security config."""
    session_secret = os.environ.get("SESSION_SECRET")
    session_factory = SignedCookieSessionFactory(session_secret)
    auth_secret = os.environ.get("AUTH_SECRET")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg="sha512"
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_session_factory(session_factory)
    config.set_default_crsf_options(require_csrf=True)
    config.set_default_permission("view")
    config.set_root_factory(MyRoot)


def check_credentials(username, password):
    """Check that user input for username and password are correct."""
    stored_username = os.environ.get("AUTH_USERNAME", "")
    stored_password = os.environ.get("AUTH_PASSWORD", "")
    is_authenticated = False
    if stored_password and stored_username:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password, stored_password)
            except ValueError:
                pass
    return is_authenticated


class MyRoot(object):
    """Create instance of MyRoot class, which defines ACL access."""
    def __init__(self, request):
        """Creates instance of MyRoot class."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "secret")
    ]
