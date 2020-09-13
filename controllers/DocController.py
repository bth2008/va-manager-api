from models import Documents


class DocController:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def all_docs():
        return [{"id": d.id, "name": d.name, "lang": d.lang} for d in Documents.query.all()]

    @staticmethod
    def one_doc(doc_id):
        doc = Documents.query.get(doc_id)
        return doc.as_dict()

    @staticmethod
    def add_doc(user, data):
        return Documents().add_doc(user, data)

    def del_doc(self, user, doc_id):
        if self.config['airline']['ceo_vid'] == user.vid:
            doc = Documents.query.get(doc_id)
            return doc.del_doc() if doc else {"success": False,
                                              "message": "No document found"}
        return {"success": False, "message": "Only CEO can do that"}
