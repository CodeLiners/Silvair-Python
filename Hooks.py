print("Loading hooklib...")
hooks = {}
def callHook(name, args):
    if name in hooks:
        for hook in hooks[name]:
            hook(args)

def regHook(name, callback):
    if not name in hooks:
        hooks[name] = []
    hooks[name].append(callback)