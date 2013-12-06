import pecan

from oslo.config import cfg

from gringotts import db
from gringotts.api import config
from gringotts.api import hooks
from gringotts.api import middleware

from gringotts.openstack.common import log as logger

CONF = cfg.CONF
LOG = logger.getLogger(__name__)


def get_pecan_config():
    # Set up the pecan configuration
    filename = config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(config, extra_hooks=None):

    app_hooks = [hooks.ConfigHook(),
                 hooks.DBHook(db.get_connection(CONF))]

    if extra_hooks:
        app_hooks.extend(extra_hooks)

    if not config:
        config = get_pecan_config()

    app = pecan.make_app(
        config.app.root,
        static_root=config.app.static_root,
        template_path=config.app.template_path,
        debug=CONF.debug,
        force_canonical=getattr(config.app, 'force_canonical', True),
        hooks=app_hooks,
        wrap_app=middleware.FaultWrapperMiddleware,
    )
    pecan.conf.update({'wsme': {'debug': CONF.debug}})

    return app


class VersionSelectorApplication(object):
    def __init__(self):
        pc = get_pecan_config()
        self.v1 = setup_app(config=pc)

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)
