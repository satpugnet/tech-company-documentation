from mongo.mongo_client import DB


class DbDocument:
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    COLLECTION = DB['document']  # Reference to the mongo collection

    class FileReference:
        """
        A FileReference is part of a Document, and references lines of code in repositories
        """

        def __init__(self, ref_id, repo, path, start_line, end_line, is_deleted):
            self.ref_id = ref_id
            self.repo = repo
            self.path = path
            self.start_line = start_line
            self.end_line = end_line
            self.is_deleted = is_deleted

        def to_json(self):
            return {
                'ref_id': self.ref_id,
                'repo': self.repo,
                'path': self.path,
                'start_line': self.start_line,
                'end_line': self.end_line,
                'is_deleted': self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return DbDocument.FileReference(
                file_ref['ref_id'],
                file_ref['repo'],
                file_ref['path'],
                int(file_ref['start_line']),
                int(file_ref['end_line']),
                file_ref['is_deleted']
            )

    def __init__(self, org_user_account, name, content, references):
        self.org_user_account = org_user_account
        self.name = name
        self.content = content
        self.references = references

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __update(query, new_values):
        return DbDocument.COLLECTION.update_one(query, new_values)

    @staticmethod
    def update_lines_ref(org_user_account, ref_id, new_start_line, new_end_line):
        query = {
            "org_user_account": org_user_account,
            "refs.ref_id": ref_id
        }
        new_values = {
            "$set": {
                "refs.$.start_line": new_start_line,
                "refs.$.end_line": new_end_line
            }
        }

        return DbDocument.__update(query, new_values)

    @staticmethod
    def update_path_ref(org_user_account, ref_id, path):
        query = {
            "org_user_account": org_user_account,
            "refs.ref_id": ref_id
        }
        new_values = {
            "$set": {
                "refs.$.path": path
            }
        }

        return DbDocument.__update(query, new_values)

    @staticmethod
    def update_is_deleted_ref(org_user_account, ref_id, is_deleted):
        query = {
            "org_user_account": org_user_account,
            "refs.ref_id": ref_id
        }
        new_values = {
            "$set": {
                "refs.$.is_deleted": is_deleted
            }
        }

        return DbDocument.__update(query, new_values)

    @staticmethod
    def find(org_user_account, name):
        doc = DbDocument.COLLECTION.find_one({
            'org_user_account': org_user_account,
            'name': name
        })

        if not doc:
            return None

        return DbDocument.from_json(doc)

    @staticmethod
    def get_all(org_user_account):
        docs = DbDocument.COLLECTION.find({
            'org_user_account': org_user_account
        })

        return [DbDocument.from_json(doc) for doc in docs]

    def to_json(self):
        return {
            'org_user_account': self.org_user_account,
            'name': self.name,
            'content': self.content,
            'refs': [ref.to_json() for ref in self.references],
        }

    @staticmethod
    def from_json(document):
        return DbDocument(
            document['org_user_account'],
            document['name'],
            document['content'],
            [DbDocument.FileReference.from_json(ref) for ref in document['refs']]
        )
