# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'gringotts.api.v1.root.RootController',
    'modules': ['gringotts.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/v1/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

# Wether or not to include exception tracebacks
# in the returned server-side errors.
wsme = {
    'debug': True
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf