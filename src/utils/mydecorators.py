import functools
import inspect

# https://stackoverflow.com/questions/11731136/class-method-decorator-with-self-arguments
# https://realpython.com/primer-on-python-decorators/

def _error_decorator(do_raise=True, res=-1):                
        def decorator(function):                
                def wrapper(mainclass, *args, **kwargs):
                        try:                                
                                result = function(mainclass, *args, **kwargs)
                                return result
                        except Exception as e:
                                mainclass.log.errlg(e, function.__name__)
                                #print (f"{function.__name__} erreur {e}")
                                if do_raise:raise
                                return res
                return wrapper
        return decorator

def _error_return_int_decorator(function):                
        def wrapper(mainclass, *args, **kwargs):
                try:
                        #print (f"fonction={function.__name__}")
                        result = function(mainclass, *args, **kwargs)
                        return result
                except Exception as e:
                        mainclass.log.errlg(e)
                        #print (f"{function.__name__} erreur {e}")
                        return -1                                
        return wrapper
                
def _trace_decorator(function):
        def wrapper(mainclass, *args, **kwargs):
                mainclass.trace(inspect.stack()[1])
                result = function(mainclass, *args, **kwargs)
                return result
        return wrapper
