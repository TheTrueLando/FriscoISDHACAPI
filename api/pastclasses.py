from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
import lxml
import cchardet
from urllib import parse

from _lib.getRequestSession import getRequestSession

class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    dic = dict(parse.parse_qsl(parse.urlsplit(self.path).query))

    print(f"REQUEST IP: {self.client_address[0]}")

    username = dic["username"]
    password = dic["password"]
    quarter = dic["quarter"]

    session = getRequestSession(username, password)

    pastCoursesRequestHeaders = {
        "Host": "hac.friscoisd.org",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
        'X-Requested-With': 'XMLHttpRequest',
        "Origin": "https://hac.friscoisd.org",
        "Referer": "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx"
    }

    pastCoursesRequestPayload = {
        "__EVENTTARGET": "ctl00$plnMain$btnRefreshView",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "EUztZv6fUH/kfpDA/0Vv7SjKlDuvPaiQLQojMxnFqbw4cOJAMgOvezlnjYoVywYQJHMRgkCC3K2Le7tjDvmZd1u8bdH3a3rzCOE+KiiNqTh5adwLxFahHC1Q+Z0PBi9S0HH+LEHtn6yF7yCACpwdbjU0dnnIi+cILRKjGt/5c30lZgSMEUE+Kqne+GrJoqvtN2qwS7TrYzLBZw9RKIyoZxb0qs8kZ65JuROtgOKiU/3eveBA5Pyx/lOyTuXEk9i0ztJeW7pyCrPWXtfJOKfgyczTkmFFd4QSAdXOCjAkwlEMr0erVIf9HSr30DbBTs2LP5GBCCFRZd1WPXpHExjrp3GLVJdKBT8zaZvIo1LZzuQI6PSPEwc/u4VNxZSbiwRR1aJYcaLto5Wy0UD0xS+ZgCKYhRhcQFwrVRdquwikEqORbL+OCpjSgXziFQOVOh+HfwGjpMBAfGQTp3Zip7f53Lt5wdgenrLJscMhAMIxESyonfJVDzLBhXH2Cgqh80KoSs696UymJsFvwoPOCzoBfGIOp4NijZsqr6PRBsIRas9O4NYbl/QLWhF1q/tdiFKUUWYRUm6Bb2kSu9+w2pdOJYVxGhQv0jKCuu6uC2zQ1bixIzMtQXFyd0MNpmQ5MZhVPlR0I9yFS6aLaUAZL5ej/5DTCpfqPV0uDGP2+3Qd9Ugr5u4p8/ey+2eyB5NT4zKF4ELNLskXNkB/BM2z5uNZCpN1owWbjJOkVrfR6NYch+tD+TpYPBg2/xDG9ubrHngoE/n7+q/jaIcjy7psUiPwRq+sUjh7AwlBHv38mfGArMV+89MgzzioI0AD5vHrru36avcsQ9wtl4kXKh3mIqSfU46q99toJ1Wd43bJSXoYbfkjYqNserO+CU0Om9qpRh/OG32VOBs7ZiwrRmIBzpe5vw1Krb7QaLyP9ye9UPyueT4Qo0QCuVaQvibmuQ5zzhsRnQyA0CUFaTccmsu0s8S9O6ek6ldtsaC6i9c40XuBBvCRoq6XbgWz1RgqIwKcUVThTxJZ6LlUJVhb5VBXlJYfxY0OSPlvW/b8XqEuzaFQyYZ0/RSczqnral0gbX3EatD+L5htFc72y3/9YO+Edbbl/K/7/n3Ei3QHp7vcnTqbbKKu1O0m6Q5izgGARDFdpFDtrMk/0QiHGtvli4dmPqgcX+P2qPHpnxFGPj9SGXfhVbfoCKatMe5Nx/78+YwVGehysdzRPXmdxtivlSitUsEdMZXxhD4+PeM1zmaQ4CkCvy5Pr8s1LrlsvVzjF/cSJu5Xwgwpdd0acZNwzIQdzonEQgS6zlBe8eDtWubrH5cnR33yRrs0evnApS9yUPsPgn36LGF15zYqVAYNUcUG5rfQcDw1Bpui9j7o4Xx4LOymyZemZKjPX1K7NGvgWi18710IDnzPyB5X0Kh9gf+xXio7StRZiL90mkbMoTfE6z12Rhg9FVNxoZKfX292d2nNNs7ExNDbOpM24pnVVtlW4ueAdPejZcNoC0Gre3v4LCZERMSYKnsV6Q1X/DVjb8yTwuBs44GImsDOuscvxXI0HdfcXKgKLjbMJqnF8P0GXzzNMTUHRhzFQO9wddLD0+U9LSIPRBE/F/4Nn8F9QOerpMCaYsS9L6Oxo0gXxOL8dDeaD2A=",
        "__VIEWSTATEGENERATOR": "B0093F3C",
        "__EVENTVALIDATION": "rVo6Q349ar26gUtGfuaIiHzqYF9IMaPUlIEkCa5nKFTVNfEeYkNuktWuIsqYFhLBJ4AVziUTJbNmofQQ9tPbuGifh+uXywyqHS9+cJ+3E1ezGsGYgwXkYNgFXiYl+yhrYa0JcMMxamGAqqKiZ/ohNwmPd9oYaJ12Fr2+WpxeomrYGWelYDARX5azu0dPUeYVpjg/mdYi5iq97fz317B1vJitegkiLAOt8P1uf59dmKrY0Dxjjt4uvlgZsWdRM47C5wgFnMYpdWercGXdAMGFTcBSPdJxPElzB5LOB52LT6iZCJVv4HFZeIXcgtEaeO3YBJ/1GMcoSVgvL4d1/nK/71dncky39p9MxBiJUHVsIip3FPceiKYuOJY+r6N60Gh31bUbg/YuC9sYAuQjtxjZE2mVI6Hwb7879Gt95KOphNHeHQcctqivfO/a52MJRVzbonj/4EfoGuyeyiw1eshlum9/xa9/lbe2cAjG02Ht26y3LfdF5MmLyP18B9PSWGP6zcJNxrMEWS/nXwIHUKU0FahZHP8l1oq7Q+nPbXrowWNZc5kmkRPCr+EG6IkHzK/c6xmSw9Az29Ho87//IogXdNUQTMjtGGLD5z+ImVaL2RI5bHnRv8DYxDcsMOCWbL0EEuarDThYrXpci1ihkEV3fBi3c2zfRF0ONBPWSrgpwBGn/GAUomy19O6BdGg0otFFZyo+9aAhRrK/zCnF/J1JbKQuc33Teajh7CaW9hkbOXMCr+71Mreb0VD2uKhA/UQWuPR7MKKUsQ3jtwY7VURKbD0V2mq3NTIBNuI6Gtp1Jiw6Wqi8L8S9tPo7ToK9+IEi4ZatkJOMDxQOIMXoRKRvjm7at0eMc9RRzMvAQ8lrLaLjUcDNSEAfkGJjbB+o7ztTzTUUQyt2VG6ZaMkQvAEDjq8pB7Q239rrpD2f5OHtksvdtnFjUqRDGMqgE8ANep/Ubl0Kq3Pf8vrzGA4V6xAsxvkgy1xhQ7YMHJeWl1VX6LYs6sEVbTM07nt45b/HSUbTSeuBKFnF0HgzZcYKd3xdS3eKchlqiu1nmGgbgXP8QRvfl+TBR2Qn90RUQxvHdWcECXS0Fy4JN0D9Drh8SeNvgS6PUncY4GySrIQ92lvkkm3T6xptXdRhcyuoxOvpcLLcNaim3LS4Odh6QrNd1nN5+7fV6bKSSK/gGrz8AvWBQM+Vhr1Ls15gX3l9cUcNif3uqbmY0JNHdbm0DlNl8K60go+tTXpRDK/w8YYMoNt1e7lWHCI5UuDf9dRTk2yahgtf4p+Gbpk/zxaxaihxrCPv7jX57zquSRw3hhI3qDMvCi+uAdglLvFYv4+CsR08oDLgNHOnUGAR7optvJiv2mnbGnacnJ8v9t0Bw1Hlzf6bLJWPi+44BkDNvxTgDSgmLYAU9xWtgvKMdBfkt3m1V0pfcpJFe8u9ka2c8Hkc8W0XU2gNjVzMn6PMfkswaLIr+OUMHt440s1EP3AB0N6GL1IGyPqhkzYtWcTJBEiKD01ptMdQb8XGPTCsIwL80n8UzWStQzNl9NZ2ukk2sxKkXym6Xv/kYEsLuSrwgLu6/Mpa502YOa654JHYidiSaV2ES58l",
        "ctl00$plnMain$hdnValidMHACLicense": "Y",
        "ctl00$plnMain$hdnIsVisibleClsWrk": "N",
        "ctl00$plnMain$hdnIsVisibleCrsAvg": "N",
        "ctl00$plnMain$hdnJsAlert": "Averages+cannot+be+displayed+when++Report+Card+Run+is+set+to+(All+Runs).",
        "ctl00$plnMain$hdnTitle": "Classwork",
        "ctl00$plnMain$hdnLastUpdated": "Last+Updated",
        "ctl00$plnMain$hdnDroppedCourse": "+This+course+was+dropped+as+of+",
        "ctl00$plnMain$hdnddlClasses": "(All+Classes)",
        "ctl00$plnMain$hdnddlCompetencies": "(All+Classes)",
        "ctl00$plnMain$hdnCompDateDue": "Date+Due",
        "ctl00$plnMain$hdnCompDateAssigned": "Date+Assigned",
        "ctl00$plnMain$hdnCompCourse": "Course",
        "ctl00$plnMain$hdnCompAssignment": "Assignment",
        "ctl00$plnMain$hdnCompAssignmentLabel": "Assignments+Not+Related+to+Any+Competency",
        "ctl00$plnMain$hdnCompNoAssignments": "No+assignments+found",
        "ctl00$plnMain$hdnCompNoClasswork": "Classwork+could+not+be+found+for+this+competency+for+the+selected+report+card+run.",
        "ctl00$plnMain$hdnCompScore": "Score",
        "ctl00$plnMain$hdnCompPoints": "Points",
        "ctl00$plnMain$hdnddlReportCardRuns1": "(All+Runs)",
        "ctl00$plnMain$hdnddlReportCardRuns2": "(All+Terms)",
        "ctl00$plnMain$hdnbtnShowAverage": "Show+All+Averages",
        "ctl00$plnMain$hdnShowAveragesToolTip": "Show+all+student's+averages",
        "ctl00$plnMain$hdnPrintClassworkToolTip": "Print+all+classwork",
        "ctl00$plnMain$hdnPrintClasswork": "Print+Classwork",
        "ctl00$plnMain$hdnCollapseToolTip": "Collapse+all+courses",
        "ctl00$plnMain$hdnCollapse": "Collapse+All",
        "ctl00$plnMain$hdnFullToolTip": "Switch+courses+to+Full+View",
        "ctl00$plnMain$hdnViewFull": "Full+View",
        "ctl00$plnMain$hdnQuickToolTip": "Switch+courses+to+Quick+View",
        "ctl00$plnMain$hdnViewQuick": "Quick+View",
        "ctl00$plnMain$hdnExpand": "Expand+All",
        "ctl00$plnMain$hdnExpandToolTip": "Expand+all+courses",
        "ctl00$plnMain$hdnChildCompetencyMessage": "This+competency+is+calculated+as+an+average+of+the+following+competencies",
        "ctl00$plnMain$hdnCompetencyScoreLabel": "Grade",
        "ctl00$plnMain$hdnAverageDetailsDialogTitle": "Average+Details",
        "ctl00$plnMain$hdnAssignmentCompetency": "Assignment+Competency",
        "ctl00$plnMain$hdnAssignmentCourse": "Assignment+Course",
        "ctl00$plnMain$hdnTooltipTitle": "Title",
        "ctl00$plnMain$hdnCategory": "Category",
        "ctl00$plnMain$hdnDueDate": "Due+Date",
        "ctl00$plnMain$hdnMaxPoints": "Max+Points",
        "ctl00$plnMain$hdnCanBeDropped": "Can+Be+Dropped",
        "ctl00$plnMain$hdnHasAttachments": "Has+Attachments",
        "ctl00$plnMain$hdnExtraCredit": "Extra+Credit",
        "ctl00$plnMain$hdnType": "Type",
        "ctl00$plnMain$hdnAssignmentDataInfo": "Information+could+not+be+found+for+the+assignment",
        "ctl00$plnMain$ddlReportCardRuns": f"{quarter}-2022",
        "ctl00$plnMain$ddlClasses": "ALL",
        "ctl00$plnMain$ddlCompetencies": "ALL",
        "ctl00$plnMain$ddlOrderBy": "Class"
    }

    pastCoursesPageContent = session.post(
        "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx",
        data=pastCoursesRequestPayload,
        headers=pastCoursesRequestHeaders
    ).text

    parser = BeautifulSoup(pastCoursesPageContent, "lxml")

    courses = []

    courseContainer = parser.find_all("div", "AssignmentClass")

    for container in courseContainer:
        newCourse = {
            "name": "",
            "grade": "",
            "lastUpdated": "",
            "assignments": []
        }
        parser = BeautifulSoup(
            f"<html><body>{container}</body></html>", "lxml")
        headerContainer = parser.find_all("div", "sg-header sg-header-square")
        assignementsContainer = parser.find_all("div", "sg-content-grid")

        for hc in headerContainer:
            parser = BeautifulSoup(f"<html><body>{hc}</body></html>", "lxml")

            newCourse["name"] = parser.find("a", "sg-header-heading").text.strip()

            newCourse["lastUpdated"] = parser.find(
                "span", "sg-header-sub-heading").text.strip().replace("(Last+Updated: ", "").replace(")", "")

            print(newCourse["lastUpdated"])

            newCourse["grade"] = parser.find("span", "sg-header-heading sg-right").text.strip(
            ).replace("Student Grades ", "").replace("%", "")

        for ac in assignementsContainer:
            parser = BeautifulSoup(f"<html><body>{ac}</body></html>", "lxml")
            rows = parser.find_all("tr", "sg-asp-table-data-row")
            for assignmentContainer in rows:
                try:    
                    parser = BeautifulSoup(f"<html><body>{assignmentContainer}</body></html>", "lxml")
                    tds = parser.find_all("td")
                    assignmentName = parser.find("a").text.strip()
                    assignmentDateDue = tds[0].text.strip()
                    assignmentDateAssigned = tds[1].text.strip()
                    assignmentCategory = tds[3].text.strip()
                    assignmentScore = tds[4].text.strip()
                    assignmentTotalPoints = tds[5].text.strip()

                    newCourse["assignments"].append(
                        {
                           "name": assignmentName,
                           "category": assignmentCategory,
                           "dateAssigned": assignmentDateAssigned,
                           "dateDue": assignmentDateDue,
                           "score": assignmentScore,
                           "totalPoints": assignmentTotalPoints
                        }
                    )         
                except:
                    pass

            courses.append(newCourse)

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps({
      "pastClasses": courses,
    }).encode(encoding="utf_8"))

