class Page:
    def __init__(self, _id, path, order, is_parent, content):
        self.id = _id
        self.path = path.lstrip("/")
        self.title = path.split("/")[-1]
        self.order = order
        self.is_parent = is_parent
        self.content = content
