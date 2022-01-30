from bs4 import BeautifulSoup
import requests

class oaScrapper:
    
    def scrap(self, username, password):
        URL = 'http://portal.lnct.ac.in/'

        LOGIN_ROUTE = 'Accsoft2/StudentLogin.aspx'

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()
# csrf_token = s.get(URL).cookies['csrftoken']

        login_payload = {
            'ctl00$ScriptManager1': 'ctl00$cph1$UpdatePanel5|ctl00$cph1$btnStuLogin',
            '__EVENTTARGET':  '',
            '__EVENTARGUMENT': '' ,
            '__LASTFOCUS': '' ,
            '__VIEWSTATE': '/wEPDwUJNzE5NjI1MTU4D2QWAmYPZBYCAgMPZBYEAgcPZBYIAg0PFgIeB1Zpc2libGVnFgJmD2QWAgIBDxYCHgNzcmMFG2ltYWdlcy9MTkNUX0Job3BhbF9Mb2dvLnBuZ2QCEQ9kFgJmD2QWAgIBDxBkZBYBZmQCEw9kFgJmD2QWAgIBDxYCHwBnFgICBA9kFgJmD2QWAgIBD2QWAmYPZBYCAgEPZBYEZg9kFgJmD2QWAgIBD2QWAmYPZBYCAgEPEGRkFgBkAgEPZBYCZg9kFgICAw8WAh4FVmFsdWUFAjUxZAIVD2QWAmYPZBYCAgEPFgIfAGgWAgIED2QWAmYPZBYCAgEPZBYCZg9kFgICAQ9kFgRmD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQdGaW5ZZWFyHg5EYXRhVmFsdWVGaWVsZAUJRmluWWVhcklEHgtfIURhdGFCb3VuZGdkEBURCi0tU2VsZWN0LS0KMjAyMS0yMDIyIAoyMDIwLTIwMjEgCjIwMTktMjAyMCAKMjAxOC0yMDE5IAoyMDE3LTIwMTggCjIwMTYtMjAxNyAKMjAxNS0yMDE2IAoyMDE0LTIwMTUgCjIwMTMtMjAxNCAKMjAxMi0yMDEzIAoyMDExLTIwMTIgCjIwMTAtMjAxMSAKMjAwOS0yMDEwIAoyMDA4LTIwMDkgCjIwMDctMjAwOCAKMjAwNi0yMDA3IBURATACMTYCMTUCMTQCMTMCMTICMTECMTABOQE4ATcBNgE1ATQBMwEyATEUKwMRZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAQIBZAIBD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ8QZGQWAGQCCQ8PFgIeBFRleHQFCzEyLURlYy0yMDIxZGRk+ChwWbyQjJpaoB+PpkOJ5rybuPVH3lZKmZNyoWaJwb8=',
            '__VIEWSTATEGENERATOR': 'AE43C86C',
            '__EVENTVALIDATION': '/wEdAAlRz8tiZ/E3Qm86V+rCXAmYseDjO4OjzzusyZ26WwJoA+zQjwyf5g+4ezBNg2ywlcSjjWGi3txshLAmmT4JdN7fK07E9QiEVcg0FYyK8QuVpoODxP24oSCS7D+CpT9vdzVWRY5uqcphA2smPJPFzLHn+mo9SV2v/SHtiocBMWq7cO7ou5vayuKtr5/nHS8pGkUPVOOn7ugu8qvZS7LhOlOJL8s5d4+0B1LsgcAGjGR9VA==',
            'ctl00$cph1$rdbtnlType': 2,
            'ctl00$cph1$hdnSID': '' ,
            'ctl00$cph1$hdnSNO': '' ,
            'ctl00$cph1$hdnRDURL': '' ,
            'ctl00$cph1$txtStuUser': username,
            'ctl00$cph1$txtStuPsw': password,
            '__ASYNCPOST': True,
            'ctl00$cph1$btnStuLogin': 'Login >>'
        }

        login_request = s.post(URL + LOGIN_ROUTE, headers= HEADERS, data= login_payload)
        # print(login_request.status_code)

        LoginState = False

        vsoup = BeautifulSoup(s.get(URL+'Accsoft2/parents/ParentDesk.aspx').text, 'html.parser')
        verifyState = str(vsoup.find('a', id='alertsDropdown'))
        if verifyState.find(str(username)) != -1:
            LoginState = True

        result = list()

        if LoginState:
            soup = BeautifulSoup(s.get(URL+'Accsoft2/parents/StuAttendanceStatus.aspx').text, 'html.parser')
            attend = str(soup.find('span', id='ctl00_ContentPlaceHolder1_lbltotalp'))
            total = str(soup.find('span', id='ctl00_ContentPlaceHolder1_lbltotperiod'))

            attendList = attend.split()
            attendCount = int((attendList[len(attendList)-1].split('<'))[0])

            totalList = total.split()
            totalCount = int((totalList[len(totalList)-1].split('<'))[0])

            percetageAttend = (attendCount/totalCount)*100
            absentCount = totalCount - attendCount

            temp = {
                'Total Classes': totalCount,
                'Present': attendCount,
                'Percentage': percetageAttend,
                'Absent': absentCount
            }
            result.append(temp)
            return result
        else:
            temp = {
                'response code': -1,
                'response': 'login failed'
            }
            result.append(temp)
            return result

        
        
