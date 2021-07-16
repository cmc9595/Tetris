from datetime import datetime
scoreList = [['cmc', '900', '2019-03-05 05:13:12'], ['cmc', '980', '2019-03-05 05:13:15'], ['cmc', '900', '2019-03-05 05:12:15']]



scoreList = sorted(scoreList, key=lambda x:
    (-int(x[1]), x[2][::-1]))

for i in scoreList:
    print(i)