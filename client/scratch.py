masterList = []
for x in range(1,12):
    row = []
    for y in range(1,5):
        row.append(None)
    masterList.append(row)

masterList[0][0] = "hi!"
print masterList
