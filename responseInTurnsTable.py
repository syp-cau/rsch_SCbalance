import sympy as sym
import pandas as pd

x, y, e1, e2, e, g = sym.symbols('x y e1 e2 e g')

p0 = (1/2)*(2-x-y+x*e1/4+y*e2/4)*(x+y+e1+e2)
p1 = (1-e1+x*e1/4)*(x+e1)
p2 = (1-e2+y*e2/4)*(y+e2)
p12 = (1-e+g*e/4)*(g+e)

p1diff = p1.diff(e1)
p2diff = p2.diff(e2)
p12diff = p12.diff(e)
e1star = sym.solve(p1diff, e1)[0]
e2star = sym.solve(p2diff, e2)[0]
e12star = sym.solve(p12diff, e)[0]

def eStar(givenVal):
    estar = e12star.subs(g, givenVal)
    print(estar)
    return estar

def calPf0(xVal, yVal, e1Val, e2Val):
    pf = p0.subs([(x, xVal), (y, yVal), (e1, e1Val), (e2, e2Val)])
    return pf

def calPf12(eVal, gVal):
    pf = p12.subs([(e, eVal), (g, gVal)])
    return pf

###create a table
### col: x, y, e1, e2, p0, p1, p2
rows=[]

w = 2 - (2*6**(1/2))/3
#rounds: how many responses each player would give
#step: epsilon. from the starting point, how far x and y would move at once
#xStart: random x value to start
#yStart: random y value to start
def responseTable(rounds, step, xStart, yStart):
    n = 0 
    x_cur = xStart
    y_cur = yStart
    e1_cur = eStar(x_cur)
    e2_cur = eStar(y_cur)
    p0_cur = calPf0(x_cur, y_cur, e1_cur, e2_cur)
    p1_cur = calPf12(e1_cur, x_cur)
    p2_cur = calPf12(e2_cur, y_cur)

    rows = [[n, x_cur, y_cur, e1_cur, e2_cur, p0_cur, p1_cur, p2_cur, 1]]

    x_prev, y_prev = x_cur, y_cur

    n = 1

    while n<rounds+1:

        p0_max8 = -999
        x_argmax = -999
        y_argmax = -999

        ##Given e1 and e2, A0 searches for the best step forward by trying (x +-eps or +0) and (y +-eps or +0) -> it gives 8 combinations to try 
        for dirX in range(-1, 2):
            for dirY in range(-1, 2):
                if (dirX == 0 and dirY == 0):
                    continue
                epsX = dirX*step
                epsY = dirY*step

                argmax = 0

                e1_prev = e1_cur
                e2_prev = e2_cur

                x_cur = x_prev+epsX
                y_cur = y_prev+epsY

                #if x or y goes beyond the range of [0,1], bound the value to the limit
                if x_cur < 0: x_cur = 0
                if x_cur > 1: x_cur = 1
                if y_cur < 0: y_cur = 0
                if y_cur > 1: y_cur = 1

                p0_cur = calPf0(x_cur, y_cur, e1_cur, e2_cur)
                p1_cur = calPf12(e1_cur, x_cur)
                p2_cur = calPf12(e2_cur, y_cur)

                p0_temp = p0_cur
                p1_temp = p1_cur
                p2_temp = p2_cur

                ####among 8 options, A0 chose the best option that gives the biggest profit
                if p0_temp > p0_max8:
                    p0_max8 = p0_temp
                    x_argmax = x_cur
                    y_argmax = y_cur
                    argmax = "xy"

                    row = [n, x_argmax, y_argmax, e1_prev, e2_prev, p0_cur, p1_cur, p2_cur, argmax]
        ##A0 finishes it turn. the choice of x, y. Let's make a record here
        rows.append(row)

        ##the chosen x, y are now becoming the given condition for A1 and A2
        x_prev = x_argmax
        y_prev = y_argmax


        ##A1 and A2 can automatically calculate the best response, which maximizes its own profit, to the given x or y. e1 and e2 are now found
        e1_cur = eStar(x_prev)
        e2_cur = eStar(y_prev)

        p0_cur = calPf0(x_prev, y_prev, e1_cur, e2_cur)
        p1_cur = calPf12(e1_cur, x_prev)
        p2_cur = calPf12(e2_cur, y_prev)


        #let's label this row that it was for choosing e1 and e2
        argmax = "e1e2"

        row = [n, x_prev, y_prev, e1_cur, e2_cur, p0_cur, p1_cur, p2_cur, argmax]
        rows.append(row)

        #each side made decisions ones. 
        n+=1

    #write the result into a csv file 
    df = pd.DataFrame(rows, columns=["nth", "x", "y", "e1", "e2", "profit0", "profit1", "profit2", "chosen"])
    filename = "responseInTurns_x_"+str(xStart)+"_y_"+str(yStart)+"_step_"+str(step)+"_n_"+str(rounds)+".csv"
    df.to_csv(filename)

print(rows)

responseTable(100, 0.0001, 0.367, 0.367)