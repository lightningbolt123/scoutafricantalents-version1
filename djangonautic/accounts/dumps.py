def signup(request):
    User = settings.AUTH_USER_MODEL
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and group_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = group_form.cleaned_data['group']
            group.user_set.add(user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, 
                        message, 
                        to=[to_email]
            )
            email.send()
            return HttpResponse('Please visit the link sent to your email to activate your account')

    else:
        form = CustomUserCreationForm()
        group_form = UserGroupForm()
    return render(request, 'accounts/signup-form.html', {'form':form, 'group_form':group_form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        messages.add_message(request, messages.INFO, 'account activated successfully')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#url for the activate account view
re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')
  #     firstname = ipn_obj.first_name
    #     lastname = ipn_obj.last_name
    #     mail = ipn_obj.payer_email
    #     membership = ipn_obj.item_name
    #     membership_group = Group.objects.get(name=membership)
    #     user = User.objects.create_user(first_name=firstname, last_name=lastname, email=mail)
    #     user.is_active = False
    #     user.save()
    #     if user.save():
    #         membership_group.user_set.add(user)
    #         current_site = get_current_site(request)
    #         mail_subject = "Thank You For Signing Up"
    #         message = render_to_string('store/mails/signup-confirmation.html', {
    #             'domain':current_site.domain,
    #             'firstname':firstname,
    #             'lastname':lastname,
    #         })
    #         email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[mail])
    #         email.send()

    # elif ipn_obj.txn_type == "subscr_payment":
    #     firstname = ipn_obj.first_name
    #     lastname = ipn_obj.last_name
    #     mail = ipn_obj.payer_email
    #     user = User.objects.get(email=mail)
    #     if user.exists():
    #         user.is_active = True
    #         user.save()
    #         mail_subject = "Membership Renewal Confirmed"
    #         current_site = get_current_site(request)
    #         message = render_to_string('store/mails/membership-renewal.html', {
    #             'firstname': firstname,
    #             'lastname': lastname,
    #             'domain': current_site.domain
    #         })
    #         email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[mail])
    #         email.send()


    # elif ipn_obj.txn_type == "subscr_eot":
    #     mail = ipn_obj.payer_email
    #     user = User.objects.get(email=mail)
    #     firstname = user.first_name
    #     lastname = user.last_name
    #     current_site = get_current_site(request)
    #     mail_subject = "Your Subscription Has Expired"
    #     message = render_to_string('store/mails/end-of-membership.html', {
    #         'firstname':firstname,
    #         'lastname':lastname,
    #         'domain':current_site.domain,
    #     })
    #     if user.is_active == True:
    #         user.is_active = False
    #         user.save()
    #         email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[mail])
    #         email.send()

    # elif ipn_obj.txn_type == "subscr_failed":
    #     mail = ipn_obj.payer_email
    #     firstname = ipn_obj.first_name
    #     lastname = ipn_obj.last_name
    #     current_site = get_current_site(request)
    #     mail_subject = "Your subscription was not successful"
    #     message = render_to_string('',
    #     {
    #         'firstname':firstname,
    #         'lastname':lastname,
    #         'domain':current_site.domain, 
    #     })
    #     email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[mail])
    #     email.send()

    # else:
    #     pass
valid_ipn_received.connect(payment_receiver)

# def show_me_the_money(sender, **kwargs):
#     ipn_obj = sender
# # Undertake some action depending upon `ipn_obj`.
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         print('Payment is completed')
#         user_infor = ast.literal_eval(ipn_obj.custom)
#         if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
#             print('And Payment is valid')
#             # generate and send an email with pdf certificate file to the user's email
#             user_infor = ast.literal_eval(ipn_obj.custom)
#             user_info = {
#                 "name": user_infor['name'],
#                 "hours": user_infor['hours'],
#                 "taggedArticles": user_infor['taggedArticles'],
#                 "email": user_infor['email'],
#                 "date": user_infor['date'],
#             }
#             html = render_to_string('users/certificate_template.html',
#                                     {'user': user_info})
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'filename=certificate_{}'.format(user_info['name']) + '.pdf'
#             pdf = weasyprint.HTML(string=html, base_url='http://8d8093d5.ngrok.io/users/process/').write_pdf(
#                 stylesheets=[weasyprint.CSS(string='body { font-family: serif}')])
#             to_emails = [str(user_infor['email'])]
#             subject = "Certificate from Nami Montana"
#             email = EmailMessage(subject, body=pdf, from_email=settings.EMAIL_HOST_USER, to=to_emails)
#             email.attach("certificate_{}".format(user_infor['name']) + '.pdf', pdf, "application/pdf")
#             email.content_subtype = "pdf"  # Main content is now text/html
#             email.encoding = 'us-ascii'
#             email.send()
#         else:
#             payment_was_flagged.connect(do_not_show_me_the_money)

# def do_not_show_me_the_money(sender, **kwargs):
#     print('And Payment is not valid')
#     ipn_obj = sender
#     user_infor = ast.literal_eval(ipn_obj.custom)
#     to_emails = [str(user_infor['email'])]
#     subject = "Certificate from Nami Montana"
#     # message = 'Enjoy your certificate.'
#     email = EmailMessage(subject, body='Unfortunately, there\'s something wrong with your payment as it\'s'
#                                    'not validated.Check your PayPal account, please!',
#                      from_email=settings.EMAIL_HOST_USER, to=to_emails)
#     email.send()

# valid_ipn_received.connect(show_me_the_money)