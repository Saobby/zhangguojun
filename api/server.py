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
    for a in ans:
        now = inp.copy()
        now[a[0]] += a[1]
        if not check_ans(now):
            final_ans.append(a)
    ret = []
    for a in final_ans:
        ret_ = inp.copy()
        ret_[a[0]] += a[1]
        ret.append(ret_)
    return json.dumps(ans)
