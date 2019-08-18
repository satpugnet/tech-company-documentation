from mongo.mongo_client import DB


class Document:
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    COLLECTION = DB['document']  # Reference to the mongo collection

    ORGANISATION_FIELD = "organisation"
    NAME_FIELD = "name"
    CONTENT_FIELD = "content"
    REFS_FIELD = "refs"

    class FileReference:
        """
        A FileReference is part of a Document, and references lines of code in repositories
        """

        REF_ID_FIELD = "ref_id"
        REPO_FIELD = "repo"
        PATH_FIELD = "path"
        START_LINE_FIELD = "start_line"
        END_LINE_FIELD = "end_line"
        IS_DELETED_FIELD = "is_deleted"

        def __init__(self, ref_id, repo, path, start_line, end_line, is_deleted):
            self.ref_id = ref_id
            self.repo = repo
            self.path = path
            self.start_line = start_line
            self.end_line = end_line
            self.is_deleted = is_deleted

        def to_json(self):
            return {
                Document.FileReference.REF_ID_FIELD: self.ref_id,
                Document.FileReference.REPO_FIELD: self.repo,
                Document.FileReference.PATH_FIELD: self.path,
                Document.FileReference.START_LINE_FIELD: self.start_line,
                Document.FileReference.END_LINE_FIELD: self.end_line,
                Document.FileReference.IS_DELETED_FIELD: self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return Document.FileReference(
                file_ref[Document.FileReference.REF_ID_FIELD],
                file_ref[Document.FileReference.REPO_FIELD],
                file_ref[Document.FileReference.PATH_FIELD],
                int(file_ref[Document.FileReference.START_LINE_FIELD]),
                int(file_ref[Document.FileReference.END_LINE_FIELD]),
                file_ref[Document.FileReference.IS_DELETED_FIELD]
            )

    def __init__(self, organisation, name, content, references):
        self.organisation = organisation
        self.name = name
        self.content = content
        self.references = references

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __update(query, new_values):
        return Document.COLLECTION.update_one(query, new_values)

    @staticmethod
    def update_lines_ref(organisation, ref_id, new_start_line, new_end_line):
        query = {
            Document.ORGANISATION_FIELD: organisation,
            "{}.{}".format(Document.REFS_FIELD, Document.FileReference.REF_ID_FIELD): ref_id
        }
        new_values = {
            "$set": {
                "{}.$.{}".format(Document.REFS_FIELD, Document.FileReference.START_LINE_FIELD): new_start_line,
                "{}.$.{}".format(Document.REFS_FIELD, Document.FileReference.END_LINE_FIELD): new_end_line,
            }
        }

        return Document.__update(query, new_values)

    @staticmethod
    def update_path_ref(organisation, ref_id, path):
        query = {
            Document.ORGANISATION_FIELD: organisation,
            "{}.{}".format(Document.REFS_FIELD, Document.FileReference.REF_ID_FIELD): ref_id
        }
        new_values = {
            "$set": {
                "{}.$.{}".format(Document.REFS_FIELD, Document.FileReference.PATH_FIELD): path,
            }
        }

        return Document.__update(query, new_values)

    @staticmethod
    def update_is_deleted_ref(organisation, ref_id, is_deleted):
        query = {
            Document.ORGANISATION_FIELD: organisation,
            "{}.{}".format(Document.REFS_FIELD, Document.FileReference.REF_ID_FIELD): ref_id
        }
        new_values = {
            "$set": {
                "{}.$.{}".format(Document.REFS_FIELD, Document.FileReference.IS_DELETED_FIELD): is_deleted,
            }
        }

        return Document.__update(query, new_values)

    @staticmethod
    def find(organisation, name):
        doc = Document.COLLECTION.find_one({
            Document.ORGANISATION_FIELD: organisation,
            Document.NAME_FIELD: name
        })

        if not doc:
            return None

        return Document.from_json(doc)

    @staticmethod
    def get_all(organisation):
        docs = Document.COLLECTION.find({
            Document.ORGANISATION_FIELD: organisation
        })

        return [Document.from_json(doc) for doc in docs]

    def to_json(self):
        return {
            Document.ORGANISATION_FIELD: self.organisation,
            Document.NAME_FIELD: self.name,
            Document.CONTENT_FIELD: self.content,
            Document.REFS_FIELD: [ref.to_json() for ref in self.references],
        }

    @staticmethod
    def from_json(document):
        return Document(
            document[Document.ORGANISATION_FIELD],
            document[Document.NAME_FIELD],
            document[Document.CONTENT_FIELD],
            [Document.FileReference.from_json(ref) for ref in document[Document.REFS_FIELD]]
        )
