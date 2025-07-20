from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_application_email_to_company(company_email, job_title, seeker_name, application_id, resume=None):
    """Send an email to the company when a job application is created."""
    if not company_email:
        return
    subject = f"Yangi ariza: {job_title}"
    from_email = settings.EMAIL_HOST_USER
    to = [company_email]

    accept_url = f"http://localhost:8000/api/applications/{application_id}/accept/"
    reject_url = f"http://localhost:8000/api/applications/{application_id}/reject/"

    html_content = render_to_string("company_application.html", {
        "job_title": job_title,
        "seeker_name": seeker_name,
        "accept_url": accept_url,
        "reject_url": reject_url,
        "resume": resume if resume else "No resume provided"
    })

    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_result_to_seeker(email, job_title, result, contact):
    subject = f"Arizangiz natijasi: {job_title}"
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    html_content = render_to_string("seeker_result.html", {
        "job_title": job_title,
        "result": result,
        "contact": contact
    })

    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
