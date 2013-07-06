import functools

import flask


def templated(template=None):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = flask.request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return flask.render_template(template_name, **ctx)
        return wrapped
    return wrapper
