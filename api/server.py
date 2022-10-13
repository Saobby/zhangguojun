from flask import *
import json

app = Flask(__name__)


def is_fail(i):
    j = {}
    for a in i:
        if a in j:
            j[a] += 1
        else:
            j[a] = 1
    for k, v in j.items():
        if v != 2:
            return False
    return True
    

@app.route("/api/act", methods=["get", "post"])
def act():
    inp = request.args.get("input")
    if inp is None:
        return abort(400)
    inp = inp.split(",")
    if len(inp) != 4:
        return abort(400)
    inp_ = []
    for i in inp:
        try:
            inp_.append(int(i))
        except:
            return abort(400)
    inp = inp_
    ans = check_ans(inp)
    final_ans = []
    f = []
    for a in ans:
        now = inp.copy()
        now[a[0]] += a[1]
        ca = check_ans(now)
        fail = False
        for b in ca:
            n = now.copy()
            n[b[0]] += b[1]
            if is_fail(n):
                fail = True
                break
        if not fail:
            final_ans.append(a)
        else:
            f.append(check_ans(now))
    ret = []
    for a in final_ans:
        ret_ = inp.copy()
        ret_[a[0]] += a[1]
        ret.append(ret_)
    return json.dumps(ret)+json.dumps(f)+json.dumps(ans)
