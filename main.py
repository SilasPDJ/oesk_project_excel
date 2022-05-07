import win32com.client as win32

outlook = win32.Dispatch('outlook.application') 

mail = outlook.CreateItem(0)
mail.Subject = "Test subject"
mail.To = "yourrecipient@gmail.com"

# If you want to set which address the e-mail is sent from. 
# The e-mail needs to be part of your outlook account.
From = None
for myEmailAddress in outlook.Session.Accounts:
    if "@gmail.com" in str(myEmailAddress):
        From = myEmailAddress
        break

if From != None:
    # This line basically calls the "mail.SendUsingAccount = xyz@email.com" outlook VBA command
    mail._oleobj_.Invoke(*(64209, 0, 8, 0, From))

    mail.Send()