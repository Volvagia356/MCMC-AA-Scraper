import io

import requests

URL = "https://www.skmm.gov.my/legal/registers/register-of-apparatus-assignments-search"

EVENT_TARGETS = {
    "AAMaritime": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager14$pagerElem",
    "AAAero": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager15$pagerElem",
    "AARadio": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager16$pagerElem",
    "AABroadcast": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager17$pagerElem",
    "AAEarth": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager18$pagerElem",
    "AATerrestrial": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager19$pagerElem",
    "lmob_cell": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager20$pagerElem",
    "celcom_cell": None,
    "celcom_celltpa": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager22$pagerElem",
    "digi_cell": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager23$pagerElem",
    "maxis_cell": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager24$pagerElem",
    "maxis_celltpa": None,
    "tm_cell": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager26$pagerElem",
    "mmob_cell": "p$lt$ctl13$pageplaceholder$p$lt$ctl11$UniPager27$pagerElem",
}

OUTPUT_TARGET = "p_lt_ctl13_pageplaceholder_p_lt_ctl11_sys_pnlUpdate"


HEADERS = {
    "User-Agent": "Mozilla",
    "X-MicrosoftAjax": "Delta=true",
}

def fetch(aa_type, page=1):
    params = {
        "type": aa_type,
    }

    data = {
        "lng": "ms-MY",
        "__EVENTTARGET": EVENT_TARGETS[aa_type],
        "__EVENTARGUMENT": page,
        "__ASYNCPOST": "true",
    }

    return requests.post(URL, params=params, data=data, headers=HEADERS)

def _read_until(buf, end):
    out_buf = io.StringIO()

    while True:
        c = buf.read(1)
        if len(c) == 0:
            raise EOFError()
        if c == end:
            break
        out_buf.write(c)

    value = out_buf.getvalue()
    return value

def parse(data):
    buf = io.StringIO(data)

    commands = []
    try:
        while True:
            entry = {}
            entry['size'] = int(_read_until(buf, "|"))
            entry['function'] = _read_until(buf, "|")
            entry['target'] = _read_until(buf, "|")
            entry['value'] = buf.read(entry['size'])
            assert buf.read(1) == "|"
            commands.append(entry)
    except EOFError:
        pass

    return commands

def get_content(commands):
    for command in commands:
        if command['function'] == "updatePanel" and command['target'] == OUTPUT_TARGET:
            return command['value']
