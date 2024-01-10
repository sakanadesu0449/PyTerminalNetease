# -*- coding: utf-8 -*-

from storage import Account
from pyncm import apis
import os

SEP = os.linesep

class Login:

    def __init__(self):

        self.local_data = Account()
        self.local_info = self.local_data.get_stg_accounts
        #print(self.local_info)

    @property
    def get_login_status(self):
        login_st = apis.login.GetCurrentLoginStatus()
        return [
            login_st['code'],
            login_st['account']['id'],
            login_st['profile']['nickname']
            ]

    def save_account_data(self,alias,account,pwd = None):
        
        self.local_data.dump(alias,account,pwd)

    def get_new_account(self):

        alias = input(f'input your account\'s alias:{SEP}')
        account = input(f'input your account\'s phone or email:{SEP}')
        pwd = input(f'input your password,press enter to skip:{SEP}')

        self.local_data.dump(alias,account,pwd)
        return [alias,account,pwd]
    
    def account_login(self,acc_info):
        alias,account,pwd = acc_info
        if not pwd:
            apis.login.SetSendRegisterVerifcationCodeViaCellphone(account)
            captcha = input('input your Captcha:')
            apis.login.LoginViaCellphone(account,captcha = captcha)
            return self.get_login_status

        elif '@' in account:
            apis.login.LoginViaEmail(account,pwd)
            return self.get_login_status

        else:
            apis.login.LoginViaCellphone(account,pwd)
            return self.get_login_status

    def start(self):

        use_account = input(f'''{SEP}Welcome to PyTerminalNetease!: 
            '0' to use a new account
            '1' to continue{SEP}''')
        if (not self.local_data.has_login_history) or (int(use_account) == 0):
            new_account_info = self.get_new_account()
            self.account_login(new_account_info)

        if self.local_data.has_login_history:
            print('Accounts has login:')
            for acc_count in range(1,len(self.local_info)):
                print('{0}      {1}{2}'.format(
                    acc_count,
                    self.local_info[acc_count]['alias'],
                    SEP
                    )
                )

            selection = int(input('Select an account to login(the index number)'))
            selected_acc = [
                    self.local_info[selection]['alias'],
                    self.local_info[selection]['data']['account'],
                    self.local_info[selection]['data']['password']
                    ]
            self.account_login(selected_acc)

