def parseCurly(s):
    ans = []
    if not s:
        return ans
    
    # find the firstCurly
    start = None
    end = None

    for index, letter in enumerate(s):
        if letter == "{":
            start = index
        elif letter == "}":
            if start is not None:
                end = index
                break

    if start is not None and end is not None:
        prefix = s[:start]
        midStr = s[start + 1: end]
        splits = midStr.split(",")
        
        if len(splits) < 2:
            ans.append(s[:end + 1])
        else:
            for split in splits:
                ans.append(prefix + split)
        
        suffix = parseCurly(s[end + 1:])
        totalAns = []

        for pre in ans:
            if not suffix:
                totalAns.append(pre)
            for suff in suffix:
                totalAns.append(pre + suff)
        return totalAns
    else:
        ans.append(s)

    return ans

print(parseCurly("/2022/{jan,feb,march}/report"))
print(parseCurly('over{crowd,eager,bold,fond}ness'))
print(parseCurly("read.txt{,.bak}"))
print(parseCurly("/2022/{jan,feb,march}/report/{important,nonimportant}"))
print(parseCurly('sun{mars}rotation'))
print(parseCurly('hello-}-weird-{-world'))
print(parseCurly('{curly,brace}/letsee/'))