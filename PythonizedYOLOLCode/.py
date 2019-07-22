

# Line 1
# COMMENT:  variable setting

# Line 2
:f += 1 
g -= 1 
a = 1 
:b += 2 
c -= 3 
d *= 4 
e /= 5 
h %= 2 
i = "hello" 
:j = "world" 

# Line 3
# COMMENT:  conditionals

# Line 4
if var == 0: #(start_indent)
    endres = 1 
    if var == 1: #(start_indent)
        endres = 2 #(last_indent)#(last_indent)

# Line 5
if var == 0: #(start_indent)
    if endres != 1: #(start_indent)
        endres = 2 #(last_indent)
    endres = 1 
    if endres != 1: #(start_indent)
        endres = 2 #(last_indent)#(last_indent)
a = :b 