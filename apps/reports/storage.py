from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateReportStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        kwargs.update({
            "location": settings.PRIVATE_STORAGE_ROOT,
            "base_url": settings.MEDIA_URL,
        })
        super(PrivateReportStorage, self).__init__(**kwargs)


private_report_storage = PrivateReportStorage()
