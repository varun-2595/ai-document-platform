class DocumentUploadError(Exception):
    pass


class EmptyDocumentError(DocumentUploadError):
    pass


class UnsupportedDocumentTypeError(DocumentUploadError):
    pass


class DocumentTooLargeError(DocumentUploadError):
    pass


class ProcessingError(Exception):
    pass
