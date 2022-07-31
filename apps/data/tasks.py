from django.conf import settings
from celery import Celery
from django.core.management import call_command

from .functions import SignUserUpForReports, RequestAmzReportDataAllReports, UploadDataToGoogleSheetsAllReports, last_n_days

from apps.amazon_api.models import AmzTokens

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

TODAY = last_n_days(1)[0]

#Initial Sign Up
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

#Daily Updates
@app.task
def request_amz_report_data_all_reports_all_users_yesterday():
    users = AmzTokens.objects.all().values('USER').distinct()
    date = TODAY

    for user in users:
        instance = RequestAmzReportDataAllReports(user, date)
        instance.execute()

@app.task
def upload_all_reports_all_users_to_gs_yesterday_task():
    users = AmzTokens.objects.all().values('USER').distinct()
    for user in users:
        instance = UploadDataToGoogleSheetsAllReports(user)
        instance.execute()

@app.task
def backup_database_task():
    with open("db_backup{}.json".format(str(TODAY)), "w", encoding="utf-8") as fp:
        call_command("dumpdata", format="json", indent=2, stdout=fp)