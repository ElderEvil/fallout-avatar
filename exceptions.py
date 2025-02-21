class MinioError(Exception):
    """Base class for MinIO related exceptions."""


class BucketNotFoundError(MinioError):
    """Raised when a specified bucket does not exist."""


class FileUploadError(MinioError):
    """Raised when a file upload to MinIO fails."""


class FileDownloadError(MinioError):
    """Raised when a file download from MinIO fails."""
