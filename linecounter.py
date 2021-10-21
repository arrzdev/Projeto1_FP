FILE = "prj.py"

comments = 0
code = 0
white = 0

with open(FILE, "r") as f:
    lines = f.readlines()

    for line in lines:
        if line.strip() == "":
            white += 1
        elif line.strip()[0] == "#":
            comments += 1
        else:
            code += 1


    print(f'''
=========================================

    Your code have [{len(lines)}] lines:    
    - Actual code lines: [{code}]        
    - Empty lines: [{white}]              
    - Lines with only comments: [{comments}]  

=========================================
   ''')