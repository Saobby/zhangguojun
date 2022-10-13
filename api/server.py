from flask import *
import json

app = Flask(__name__)


def check_ans(input_val):
    inp = input_val
    ans = []
    for i in range(4):
        a, b, c, d = inp[0], inp[1], inp[2], inp[3]
        x1 = -a+b+c-d
        x2 = -a-b+c+d
        x3 = -a+b+c-d
        x4 = -a+b-c+d
        x5 = -a+b-c+d
        x6 = -a-b+c+d
        an = [x1, x2, x3, x4, x5, x6]
        for j in an:
            if j <= -a and j != 0:
                ans.append((i, j))
        inp.append(inp.pop(0))
    return ans


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
