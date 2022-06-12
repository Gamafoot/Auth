from flask import session, redirect

#============================================================================
#========================== Custom decorators ===============================
#============================================================================
def isLogged(func):
    def wrapper(*args, **kwargs):
        if 'logged' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    wrapper.__name__ = func.__name__
    return wrapper


def tryex(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                print(f"\n---------------------\n!:::Error:::!\n\nMethod: {func.__name__}()\n\n-->{ex}\n---------------------\n")
                return False
        wrapper.__name__ = func.__name__
        return wrapper

#============================================================================
#=========================== Custom functions ===============================
#============================================================================