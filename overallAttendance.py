from bs4 import BeautifulSoup
import requests

class oaScrapper:
    
    def scrap(self, username, password):
        URL = 'http://portal.lnct.ac.in/'

        LOGIN_ROUTE = 'Accsoft2/StudentLogin.aspx'

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()
# csrf_token = s.get(URL).cookies['csrftoken']

        login_payload = {
            'ctl00$ScriptManager1': 'ctl00$cph1$UpdatePanel5|ctl00$cph1$btnStuLogin',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '/wEPDwULLTE2MDI1OTUyNjEPZBYCZg9kFgICAw9kFgQCBw9kFggCDQ8WAh4HVmlzaWJsZWcWAmYPZBYCAgEPFgIeA3NyYwUbaW1hZ2VzL0xOQ1RfQmhvcGFsX0xvZ28ucG5nZAIRD2QWAmYPZBYCAgEPEGRkFgFmZAITD2QWAmYPZBYCAgEPFgIfAGcWAgIFD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ9kFgRmD2QWAmYPZBYCAgEPZBYCZg9kFgICAQ8QZGQWAGQCAQ9kFgJmD2QWAgIDDxYCHgVWYWx1ZQUCNTFkAhUPZBYCZg9kFgICAQ8WAh8AaBYCAgQPZBYCZg9kFgICAQ9kFgJmD2QWAgIBD2QWBGYPZBYCZg9kFgICAQ9kFgJmD2QWAgIBDxAPFgYeDURhdGFUZXh0RmllbGQFB0ZpblllYXIeDkRhdGFWYWx1ZUZpZWxkBQlGaW5ZZWFySUQeC18hRGF0YUJvdW5kZ2QQFREKLS1TZWxlY3QtLQoyMDIxLTIwMjIgCjIwMjAtMjAyMSAKMjAxOS0yMDIwIAoyMDE4LTIwMTkgCjIwMTctMjAxOCAKMjAxNi0yMDE3IAoyMDE1LTIwMTYgCjIwMTQtMjAxNSAKMjAxMy0yMDE0IAoyMDEyLTIwMTMgCjIwMTEtMjAxMiAKMjAxMC0yMDExIAoyMDA5LTIwMTAgCjIwMDgtMjAwOSAKMjAwNy0yMDA4IAoyMDA2LTIwMDcgFREBMAIxNgIxNQIxNAIxMwIxMgIxMQIxMAE5ATgBNwE2ATUBNAEzATIBMRQrAxFnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBAgFkAgEPZBYCZg9kFgICAQ9kFgJmD2QWAgIBDxBkZBYAZAIJDw8WAh4EVGV4dAULMTEtRmViLTIwMjJkZGRBeiGUVNjc/s2MEelIsPytRdianHTq/zeUXRH7lqF+pg==',
            '__VIEWSTATEGENERATOR': 'AE43C86C',
            '__EVENTVALIDATION': '/wEdAAnrJ+guAwVW1WiBV0iTxOI4seDjO4OjzzusyZ26WwJoA+zQjwyf5g+4ezBNg2ywlcSjjWGi3txshLAmmT4JdN7fK07E9QiEVcg0FYyK8QuVpoODxP24oSCS7D+CpT9vdzVWRY5uqcphA2smPJPFzLHn+mo9SV2v/SHtiocBMWq7cO7ou5vayuKtr5/nHS8pGkVycJjdzclT9OsEkiSJ2Y/m6FgZC9Wf9Nct3/C2yTKmUw==',
            'ctl00$cph1$rdbtnlType': 2,
            'ctl00$cph1$hdnSID': '',
            'ctl00$cph1$hdnSNO': '',
            'ctl00$cph1$hdnRDURL': '',
            'ctl00$cph1$txtStuUser': username,
            'ctl00$cph1$txtStuPsw': password,
            '__ASYNCPOST': True,
            'ctl00$cph1$btnStuLogin': 'Login >>'
        }

        login_request = s.post(URL + LOGIN_ROUTE, headers= HEADERS, data= login_payload)
        print(login_request.status_code)

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
                'response': login_request.status_code
            }
            result.append(temp)
            return result

        
        
