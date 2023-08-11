from apimedic.api_requests import get_auth_token, get_item

# # Information for accessing the sandbox API
#username = 'lennyklo@web.de'
#password = 'Bw3f8JNj56Zer2EAm'
#
#medicapi_auth = 'https://sandbox-authservice.priaid.ch/login'
#medicapi_health = 'https://sandbox-healthservice.priaid.ch'
#  'aqk81678@bcaoo.com', 'qtd50336@eoopy.com','fr67hs892jsnshdz284', 'h56683hsss9988'

# live accounts
username = ['c7Y8E_WEB_DE_AUT', 'Kc89A_AWDRT_NET_AUT', 'Ex7r6_AWDRT_NET_AUT', 'p3L9C_BCAOO_COM_AUT', 's7RLi_EOOPY_COM_AUT','Sa32N_TASHJW_COM_AUT','y5DHp_TASHJW_COM_AUT','Wr58C_TASHJW_COM_AUT','x2XPd_PSK3N_COM_AUT','Ay9x5_PSK3N_COM_AUT','Tm8n7_TASHJW_COM_AUT','Qp87W_PSK3N_COM_AUT','Bo86X_TASHJW_COM_AUT','Ey64H_LERWFV_COM_AUT','g4M2P_LERWFV_COM_AUT','g7BKx_DFB55_COM_AUT','Rs53N_DFB55_COM_AUT','Er9c2_DFB55_COM_AUT','Se3f4_LERWFV_COM_AUT','e5AWb_LYWENW_COM_AUT','Kp48J_LYWENW_COM_AUT','r2YCc_DFFWER_COM_AUT','y7YPj_LERWFV_COM_AUT','Tj3x7_LERWFV_COM_AUT','Tj93M_LERWFV_COM_AUT']
password = ['Ms92Hjw8AXd36Jtx7', 'p7BPk34MtYq9x2H6K', 'r2B8FdTi6s4HWp35P', 'Ad9f8BLi35PsWm7c4', 'b7Z8Hwa2B4FdXr5j6','w4BTy7a3G8Dic9H6W','Rp23Eky5SBd74NzQw','i9WXj72RkEt84Qbr6','Qq2e5SXx48GfMt96W','Sd3w9WLs5b8XGp47C','Tq3i4QRt6f9X7Fpe5','q3YSm48EiNe75Btf2','Yd6c5ZPg39Dmx7B2G','Tm2k9MKf6x4EAd73Z','c6F5Kmw4Q7DaAe9n3','p9E7Hgz3D6BeAj2y4','p8P7Wfk6M4Nwo5F3X','Tm93Bxq6P7LnHb84J','c8BTt37Jeo4DKf92P','Nw76JkDn94EoBc8g5','Sn57YmMj8c9H4Aak3','Xs78JbRa42FzBq3m9','t2RLr63QqKx89Nzy7','Qj8e3F7RtJr29Gpa4','Xi3z7L2Wax5M8Tyg9']

medicapi_auth = 'https://authservice.priaid.ch/login'
medicapi_health = 'https://healthservice.priaid.ch'


# test validity of account information
if __name__ == '__main__':
    print('usernames: '+ str(len(username)))
    print('passwords: ' + str(len(password)))

    for i in range(len(username)):
        print('Trying username ' + str(i) + ': ' + str(username[i]))
        token = get_auth_token(username[i], password[i], medicapi_auth)
        params = {'token': token, 'format': 'json', 'language': 'en-gb'}
        response = get_item('issues', params=params, url=medicapi_health)
        res = response.json()
        if (res[0]['Name'] == 'Abdominal hernia'):
            print('Success!')
        else:
            print('Fail...')

