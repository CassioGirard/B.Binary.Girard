## Two Factor Auth

Enable two factor auth on iqoption site then use this code to and auth code

```python
from iqoptionapi.stable_api import IQ_Option

print("Conecting...")
api = IQ_Option("email", "password")
status, reason = api.connect()
print('##### first try #####')
print('Status:', status)
print('Reason:', reason)
print("Email:", api.email)

if reason == "2FA":
    print('##### 2FA enabled #####')
    print("An sms has been sent with a code to your number")

    code_sms = input("Enter the code received: ")
    status, reason = api.connect_2fa(code_sms)

    print('##### second try #####')
    print('Status:', status)
    print('Reason:', reason)
    print("Email:", api.email)

print("Balance:", api.get_balance())
print("##############################")
```