from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext, Http404, get_object_or_404
from django.template.loader import render_to_string

from django.core import mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from email.MIMEImage import MIMEImage
connection = mail.get_connection()

from .forms import ContactForm


def contact(request):	
	form = ContactForm(request.POST or None)
	if form.is_valid():
		new_message = form.save()

		site = "http://www.your-site-here.com/"
		ctx_dict = {'name': new_message.name, 'email': new_message.email, 'message': new_message.message}
		message_html = render_to_string('emails/new_message.html', ctx_dict)
		msg = mail.EmailMessage("New Message", message_html, settings.DEFAULT_FROM_EMAIL, ['your-email-address@your-host.com'])
		msg.content_subtype = "html"
		msg.send()

		messages.success(request, 'Thank You %s. Your message was successfully sent.' %(new_message.name))
		return HttpResponseRedirect("contact/contact_success")

	return render_to_response("contact/contact.html", locals(), context_instance=RequestContext(request))

def contact_success(request):
	return render_to_response("contact/contact_success.html", locals(), context_instance=RequestContext(request))

