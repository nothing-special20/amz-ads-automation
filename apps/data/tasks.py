from django.conf import settings
from celery import Celery

from .functions import SignUserUpForReports, RequestAmzReportDataAllReports, UploadDataToGoogleSheetsAllReports

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

@app.task
def sign_up_user_for_reports_task(user, metrics, gs_file_name):
    instance = SignUserUpForReports(user, metrics, gs_file_name)
    instance.execute()

@app.task
def request_amz_report_data_all_reports(user, date):
    instance = RequestAmzReportDataAllReports(user, date)
    instance.execute()
        
@app.task
# @app.task(name='upload_all_reports_to_gs_task_')
def upload_all_reports_to_gs_task(user):
    instance = UploadDataToGoogleSheetsAllReports(user)
    instance.execute()