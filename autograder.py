import sys
import os
from subprocess import DEVNULL, check_call
from datetime import datetime
from pathlib import Path


BACKSLASH = "/"


def is_error(val):
    return 'error' in val.lower() or val == ""


def check_line(ans, ref, w_per_case):

    ans_ = 0.0
    try:
        ans_ = float(ans)
    except:
        ans_ = ans

    try:
        ref_ = float(ref)
    except:
        ref_ = ref

    if not isinstance(ref_, type(ans_)):
        return 0

    if(isinstance(ans_, str)):
        result = int('error' in ans_.lower()) * w_per_case
        return result
    else:
        result = int(ans_ == float(ref)) * w_per_case
        return result


def check_q1(f, infile, outfile, reffile, w_per_case):

    with open(reffile, 'r') as ref:
        ref_answers = ref.read().split('\n')

    with open(infile, 'r') as inp:
        lines = inp.read().split('\n')
        single_case = len(lines) == 1
        test_case = lines[0] if single_case else '<given>'

    try:
        if not os.path.exists(logfolder):
            os.mkdir(logfolder)
        fpath = Path(
            f'{logfolder}/{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}_{infile.split(BACKSLASH)[-1]}_errlog.txt')
        with open(fpath, 'wb') as logfile:
            check_call(['python3', '-W', 'ignore', f, '-i', infile, '-o',
                       outfile, '-m', 'eval'], stdout=logfile, stderr=logfile)
    except Exception as e:
        return (
            0,
            len(ref_answers) * w_per_case,
            test_case,
            '<CRASH>',
            ref_answers[0] if single_case else '-'
        )

    with open(outfile, 'r') as output:
        stu_answers = output.read().split('\n')
    os.remove(outfile)

    score = 0
    test_failed = True

    for i, ans in enumerate(stu_answers):
        score += check_line(ans, ref_answers[i], w_per_case)
        # test_failed = score == 0

    return (
        score,
        len(ref_answers) * w_per_case,
        test_case,
        stu_answers[0] if single_case and test_failed else '-',
        ref_answers[0] if single_case and test_failed else '-'
    )


def check_q2(f, infile, outfile, reffile, w_per_case):
    with open(reffile, 'r') as ref:
        ref_answers = ref.read().split('\n')

    with open(infile, 'r') as inp:
        lines = inp.read().split('\n')
        single_case = len(lines) == 1
        test_case = lines[0] if single_case else '<given>'

    try:
        check_call(['python3', '-W', 'ignore', f, '-i', infile, '-o',
                   outfile, '-m', 's2s'], stdout=DEVNULL, stderr=DEVNULL)
    except:
        return (
            0,
            len(ref_answers) * w_per_case,
            test_case,
            '<CRASH>',
            ref_answers[0] if single_case else '-'
        )

    with open(outfile, 'r') as output:
        stu_answers_ = output.read().split('\n')
    os.remove(outfile)

    stu_answers = []
    for s in stu_answers_:
        if not is_error(s):
            try:
                stu_answers.append(eval(s))
            except:
                stu_answers.append("CRASH: Invalid Infix Syntax")
        else:
            stu_answers.append(s)

    score = 0
    test_failed = True

    for i, ans in enumerate(stu_answers):
        score += check_line(ans, ref_answers[i], w_per_case)
    return (
        score,
        len(ref_answers) * w_per_case,
        test_case,
        stu_answers[0] if single_case and test_failed else '-',
        ref_answers[0] if single_case and test_failed else '-'
    )


def run_check(f, tests, outfile, checker):
    line = ''
    s, t = 0, 0
    for infile, reffile, w in tests:
        score, total, testcase, student_out, expected_out = checker(
            f, infile, outfile, reffile, w)
        line += f'\t{infile} => {score:.2f}/{total:.2f} | Test Case: {testcase} | Student Output: {student_out} | Expected Output: {expected_out} \n'
        s += score
        t += total
    line += f'\tSUBTOTAL: {s:.2f}/{t:.2f}\n'
    return line, s, t


logfolder = 'error_logs'
student = 'trey'


def filterer(s):
    return student in s


def test():
    solution_file = sys.argv[0]
    temp_tests = ["59 14 -", "8 14  *", "38 72 49 +  +", "32 40 + 69 40 94 - 19 / 71 86 * 71 * * -  -", "30 88 1 11 + 85 96 / + 42 + 34 - +  -",
                  "85 58 4 97 86 + 20 - * 87 * 65 84 * +  / +", "57 92 / 75 16 / 64 / 57 * + 68  -", "54 61 37  * "]
    temp_oracles = ["45", "112", "159", "-1232123.5263157894", "-78.88541666666666",
                    "85.00093271581115", "-63.205630095108695", "ERROR: Too many literals"]

    test_cases = zip(temp_tests, temp_oracles)

    i = 0
    tests = []
    score = 5

    if not os.path.exists(".cache"):
        os.mkdir(".cache")

    for test, oracle in test_cases:
        with open(f".cache/test_{i}", "w") as f:
            f.write(test)
        with open(f".cache/oracle_{i}", "w") as f:
            f.write(oracle)
        tests.append((f".cache/test_{i}", f".cache/oracle_{i}", score))
        i += 1

    outfile = "tmp"
    q1_report, s1, t1 = run_check(solution_file, tests, outfile, check_q1)
    q2_report, s2, t2 = run_check(solution_file, tests, outfile, check_q2)
    print('EVAL SCORES:\n')
    print(f'{q1_report}\n')
    print('S2S SCORES:\n')
    print(f'{q2_report}\n')
    print(f'TOTAL: {(s1+s2):.2f}\n')
