from mongo.mongo_client import DB


class Document:
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
            return Document.FileReference(
                file_ref['ref_id'],
                file_ref['repo'],
                file_ref['path'],
                int(file_ref['start_line']),
                int(file_ref['end_line']),
                file_ref['is_deleted']
            )

    def __init__(self, name, content, references):
        self.name = name
        self.content = content
        self.references = references

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __update(query, new_values):
        return Document.COLLECTION.update_one(query, new_values)

    @staticmethod
    def update_lines_ref(ref_id, new_start_line, new_end_line):
        query = { "refs.ref_id": ref_id }
        new_values = {
            "$set": {
                "refs.$.start_line": new_start_line,
                "refs.$.end_line": new_end_line
            }
        }

        return Document.__update(query, new_values)

    @staticmethod
    def update_path_ref(ref_id, path):
        query = {"refs.ref_id": ref_id}
        new_values = {
            "$set": {
                "refs.$.path": path
            }
        }

        return Document.__update(query, new_values)

    staticmethod

    def update_is_deleted_ref(ref_id, is_deleted):
        query = {"refs.ref_id": ref_id}
        new_values = {
            "$set": {
                "refs.$.is_deleted": is_deleted
            }
        }

        return Document.__update(query, new_values)

    @staticmethod
    def find(name):
        doc = Document.COLLECTION.find_one({
            'name': name
        })

        if not doc:
            return None

        return Document.from_json(doc)

    @staticmethod
    def get_all():
        return [Document.from_json(doc) for doc in Document.COLLECTION.find()]

    def to_json(self):
        return {
            'name': self.name,
            'content': self.content,
            'refs': [ref.to_json() for ref in self.references],
        }

    @staticmethod
    def from_json(document):
        return Document(
            document['name'],
            document['content'],
            [Document.FileReference.from_json(ref) for ref in document['refs']]
        )
