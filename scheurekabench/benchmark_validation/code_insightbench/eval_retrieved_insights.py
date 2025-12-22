import json

rt_insights = json.load(open("paper1/rt_insight_claude.json"))

correct_incorrect_counts = {}
for key, value in rt_insights.items():
    gt = value["gt_files"].split(";")
    rt = value["rt_files"].split(";")

    # make the gt unique
    gt = list(set(gt))
    correct = sum(1 for f in gt if f in rt)
    incorrect = len(gt) - correct

    correct_incorrect_counts[key] = {
        "correct": correct,
        "incorrect": incorrect,
        "total_gt": len(gt),
        "total_rt": len(rt),
        "percentage": correct / len(gt),
    }

print(f"Average percentage correct: {sum(v['percentage'] for v in correct_incorrect_counts.values()) / len(correct_incorrect_counts)}")
# print correct incorrect distribution, i.e., how many keys have x correct and y incorrect
correct_distribution = {}
incorrect_distribution = {}
for counts in correct_incorrect_counts.values():
    c = counts["correct"]
    i = counts["incorrect"]
    correct_distribution[c] = correct_distribution.get(c, 0) + 1
    incorrect_distribution[i] = incorrect_distribution.get(i, 0) + 1

print("Correct distribution:", correct_distribution)
print(f"Sum of correct counts: {sum(k*v for k,v in correct_distribution.items())}")
print(f"sum of total_gt: {sum(v['total_gt'] for v in correct_incorrect_counts.values())}")
print("Incorrect distribution:", incorrect_distribution)


