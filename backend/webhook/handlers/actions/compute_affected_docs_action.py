from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from mongo.models.db_doc_model import DbDocModel
from webhook.handlers.actions.abstract_webhook_action import AbstractWebhookAction


class ComputeAffectedDocsAction(AbstractWebhookAction):

    class RefGithubFilePair:

        def __init__(self, ref, commit_file):
            self.__ref = ref
            self.__commit_file = commit_file

        @property
        def ref(self):
            return self.__ref

        @property
        def commit_file(self):
            return self.__commit_file

    def __init__(self, github_account_login, repo, commit_files):
        self.__github_account_login = github_account_login
        self.__repo = repo
        self.__commit_files = commit_files

    def perform(self):
        affected_docs = []
        ref_commit_file_pairs = []

        for doc in DbDocumentClient().find(self.__github_account_login):
            is_current_doc_affected = False

            for ref in doc.refs:
                related_commit_file = self.__compute_related_commit_file(ref, self.__commit_files, self.__repo)

                if related_commit_file:
                    is_current_doc_affected = True
                    ref_commit_file_pairs.append(ComputeAffectedDocsAction.RefGithubFilePair(ref, related_commit_file))

            if is_current_doc_affected:
                affected_docs.append(doc)

        return affected_docs, ref_commit_file_pairs

    def __compute_related_commit_file(self, ref, commit_files, repo):
        if not (ref.github_account_login == repo.github_account_login
                or ref.repo_name == repo.name):
            return

        for commit_file in commit_files:
             if ref.path in commit_file.previous_path:
                 return commit_file
