class Query:
    _models = []
    """
    [
      {
        "model": Model,
        "alias": "model name"
        "search: ("Field Name",),
        "return": ("Field Name",),
        "filter": {"field": "value"}
      }
    ]
    """
    _response = {}
    """
    {
      "alias":[
        {
          "field": value,
          "field": value,
        }
      ]
    }
    """
    def __bool__(self):
        for model, results in self._response.items():
            for json in results:
                for field, value in json.items():
                    if value:
                        return True
        return False

    def __init__(self, query_str):
        self.obj = query_str

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, new_model):
        if not isinstance(new_model, dict):
            return
        for key in ["model", "alias", "search", "return"]:
            if key not in new_model:
                return
        self._models.append(new_model)

    @models.deleter
    def models(self):
        pass

    def resolve(self):
        for model in self.models:
            print(f"query-model:{model}")
            self._response[model['alias']] = []
            dictionary = self._response[model['alias']]
            print(0)
            for field in model['search']:
                filter_kwargs = {"{0}__contains".format(field): self.obj}
                filter_kwargs.update(model.get("filter", {}))
                print(f"filter_kwargs:{filter_kwargs}")
                results = model['model'].objects.filter(**filter_kwargs)
                for result in results:
                    json = {}
                    for ret in model['return']:
                        json[ret] = getattr(result, ret)
                    dictionary.append(json)
        return self._response if self else None

