from pymongo.collection import Collection
from datetime import datetime
from pymongo.errors import WriteError


class BaseModel(Collection):
    def __init__(self, database, db, create=False, codec_options=None,
                 read_preference=None, write_concern=None, read_concern=None,
                 session=None, **kwargs):
        self.db = db
        super(BaseModel, self).__init__(database, self.__collection_name__, create=create,
                                        codec_options=codec_options,
                                        read_preference=read_preference, write_concern=write_concern,
                                        read_concern=read_concern,
                                        session=session, **kwargs)

    def _check_require_fields(self, spec):
        for k, v in self.require_fields.items():
            if k not in spec:
                raise WriteError("{0} isn't exists ".format(k))
            if not isinstance(spec.get(k), v):
                raise WriteError("{0} is required {1} not {2}".format(k, v, type(spec.get(k))))

    def _add_default_fields(self, spec):
        for k, v in self.default_fields.items():
            if k not in spec:
                spec.update({k: v() if callable(v) else v})

    def create(self, spec):
        self._check_require_fields(spec)
        self._add_default_fields(spec)
        return self.insert_one(spec).inserted_id

    def update_set(self, spec, doc):
        if 'updated_at' not in doc:
            doc['updated_at'] = datetime.utcnow()
        docs = {"$set": doc}
        return self.update_one(spec, docs).matched_count

    def get_from_oid(self, oid):
        return self.find_one({"_id": oid})

    @staticmethod
    def build_object_set_result(cursor, page, limit):
        count = cursor.count()
        records = list(record for record in cursor)
        meta = {
            'result_count': count,
            'has_more': False
        }
        if count > limit * page:
            meta['has_more'] = True

        return {'data': {'records': records, '_meta': meta}}

    def find_objects(self, spec, option, **kwargs):
        """
        :param spec:
        :param option:
        :return:
        """
        page = option.pop('page', 1)
        if not option.get('limit'):
            option['limit'] = 30
        limit = option['limit']
        if kwargs.get('fields'):
            fields = {v: 1 for v in kwargs['fields']}
            cursor = self.find(spec, fields=fields, **option)
        else:
            cursor = self.find(spec, **option)
        data = self.build_object_set_result(cursor, page, limit)
        return {
            '_meta': data['data'].get("_meta"),
            'results': data['data'].get("records")
        }

    def get_dict_with_id(self, spec):
        return {i.get('_id'): i for i in self.find(spec)}
