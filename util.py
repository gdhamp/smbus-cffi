def get_validator(tp, name):
    def f(x):
        if not isinstance(x, tp):
            raise TypeError("Expected %s" % name) 
    return f


validators = {}
for tp, name in [(int, 'integer'), (float, 'float'),
                  (str, 'string'), (dict, 'dict'), (list, 'list')]:
  validators[tp] = get_validator(tp, name)


def validate(**schema):
    def wrapper(fn):
        code = fn.func_code
        nargs = code.co_argcount
        varnames = code.co_varnames
        defaults = fn.func_defaults if fn.func_defaults else []
        def validator(*args):
            largs = len(args)
            if largs != nargs and largs + len(defaults) != nargs:
                raise TypeError("%s() takes exactly %d arguments (%d given)" %
                                (fn.__name__, nargs, len(args)))
            for i, value in enumerate(args):
                name = varnames[i]
                if name not in schema:
                    continue
                typ = schema[name]
                validators[typ](value)
            if largs < nargs:
                for i in range(largs, nargs):
                    value = defaults[largs - i]
                    name = varnames[i]
                    if name not in schema:
                        continue
                    typ = schema[name]
                    validators[typ](value)
            return fn(*args)
        return validator
    return wrapper
