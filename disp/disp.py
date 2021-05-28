def disp(matrix, title = "MATRIX", mode = 0, noprint = False):
    """
    Drop in replacement for python print. Operates like Matlab's disp() function.
    Takes in an object to print, a title, and an optional mode
    """
    matstr = ""
    if mode == 0:
        matstr = dispa(matrix, title)[:-1]
    else:
        matstr = disptex(matrix, title)[:-1]
    if not noprint:
        if title != "MATRIX":
            print(title + ": " + matstr)
        else:
            print(matstr)
    return matstr

def dispa(matrix, title = "MATRIX", nd = 3, pdims = True, h=""):
    t_bar = ""
    t_tl = "╔"
    t_bl = "╚"
    #╚╔╝╗║═ Symbols Required

    #Accounts for Even or Odd amounts of letters in a title
    if (len(title) % 2 == 0):
        t_tl = t_tl + "═"
        t_bl = t_bl + "═"

    strr = ""
    #Accounts for a List of Objects, Calls itself Recursively
    if hasattr(matrix, 'TM'):
        return dispa(matrix.TAA, title)
    if isinstance(matrix, list):
        alltf = True
        for mat in matrix:
            if not hasattr(mat, 'TM'):
                alltf = False
        if alltf == True:
            return printTFlist(matrix, title, nd)

        i = 0
        str1 = (t_tl + "════════════" + " " + title + " BEGIN " + "════════════" + "╗\n")
        strm = ""
        for mat in matrix:
            if ~isinstance(mat, list) and ~isinstance(mat, tuple) and hasattr(matrix, 'TM'):
                strm += (str(mat) + "\n")
            else:
                if pdims:
                    strm+=("Dim " + str(i) + ":\n")
                strm += dispa(mat)
            i = i + 1
        str2 = (t_bl + t_bar + "════════════" + title + " END ═" + "════════════" + "╝\n")
        return str1 + strm + str2;

    shape = 0

    #Variety of try catch to prevent crashes due to liberal use of disp()
    try:
        try:
            shape = matrix.shape
        except:
            #Panda obects IIRC use shape as a method
            shape = matrix.shape()

        dims = len(shape)
        if dims >= 2:
            t_key = shape[dims - 1]
        else:
            t_key = max(shape)
    except:
        #If all else fails, print Normally
        if title != "MATRIX":
            strr += (title + "\n")
        strr += (str(matrix) + "\n")
        return strr
    #Formats correct number of top and bottom markers for t_bar
    while(len(title) + 8 + (len(t_bar) * 2)) < (t_key * (nd + 7) ):
        t_bar = t_bar + "═"

    #Prints a single Dimension Vector
    if dims == 1:
        cn = 0
        if h == "╔ ":
            cn = 1
        elif h == "╚ ":
            cn = 2
        else:
            h = h + "║ "
        for i in range(shape[0]):
            t_nd = nd
            if (abs(matrix[i]) >= 9999):
                nm = len(str(abs(round(matrix[i]))))
                while t_nd > 0 and nm > 6:
                    t_nd = t_nd - 1
                    nm = nm - 1
            fmat = "{:" + str(nd + 6) +"." + str(t_nd) + "f}"


            h = h + fmat.format(matrix[i])
            if i != shape[0] - 1:
                h = h + ","

        if cn == 0:
            h = h + " ║"
        elif cn == 1:
            h = h + " ╗"
        else:
            h = h + " ╝"

        strr+= (str(h) + "\n")

    #Prints traditional Square Matrix, allows for title
    elif dims == 2:
        if title != "MATRIX":
            strr+=(t_tl + t_bar + " " + title + " BEGIN " + t_bar + "╗\n")
        for i in range(shape[0]):
            if i == 0:
                strr += dispa(matrix[i,], nd = nd, h = "╔ ")
            elif i == shape[0] - 1:
                strr += dispa(matrix[i,], nd = nd, h = "╚ ")
            else:
                strr += dispa(matrix[i,], nd = nd)
        if title != "MATRIX":
            strr+=(t_bl + t_bar + "═ " + title + " END ═" + t_bar + "╝\n")

    #Prints 3D Matrix by calling 2D recursively
    elif dims == 3:
        strr += (t_tl + t_bar + " " + title + " BEGIN " + t_bar + "╗\n")
        for i in range(shape[0]):
            if pdims:
                strr += ("DIM " + str(i) + ":\n")
            strr += dispa(matrix[i,], nd = nd)
        strr += (t_bl + t_bar + "═ " + title + " END ═" + t_bar + "╝\n")

    #Prints 4D Matrix by calling 3D recursively
    elif dims == 4:
        strr += (t_tl + t_bar + "══ " + title + " BEGIN ══" + t_bar + "╗\n")
        for i in range(shape[0]):
            strr += dispa(matrix[i,], nd = nd, title = title + " d:" + str(i), pdims = pdims)
        strr += (t_bl + t_bar + "═══ " + title + " END ═══" + t_bar + "╝\n")
    else:
        taux = "═"
        for i in range (dims - 3):
            taux = taux + taux
        strr += (t_tl + t_bar + taux +" " + title + " BEGIN " + taux + t_bar + "╗\n")
        for i in range(shape[0]):
            strr += dispa(matrix[i,], title = title + " s" + str(i))
        strr += (t_bl + t_bar + taux + "═ " + title + " END ═" + taux + t_bar + "╝\n")
    return strr
    #More dimensions can be added as needed if neccessary

def disptex(matrix, title,  nd = 3, pdims = True, h=""):
    try:
        shape = matrix.shape
    except:
        return dispa(matrix, title)
    strr = "\\begin{table}\n\\centering\n\\begin{tabular}{|"
    for i in range(shape[1]):
        strr = strr + " c "
        if i == shape[1] - 1:
            strr = strr + ("|}\n\\hline\n")
    strr+="\\toprule\n"
    strr+="%INSERT CAPTIONS HERE\n"
    strr+="\\midrule\n"
    for i in range(shape[0]):
        #strr+= "\\hline\n"
        for j in range(shape[1]):
            strr+= str(round(matrix[i,j], nd))
            if j != shape[1] - 1:
                strr+=" & "
                continue
            else:
                break
        strr+="\\\\\n"
    strr+="\\bottomrule\n"
    strr+="\\end{tabular}\n\\caption{" + title + "}\n\\end{table}\n"
    return strr


def printTFlist(matrix, title, nd):
    strr =  "╔"
    nTF = len(matrix)
    tLen = (2 * nTF * (nd+1) + (2*nTF+1))
    j = 0
    for i in range(round((2 * nTF * (nd+1) + (2*nTF+1))/2 - len(title)/2 - 1)):
        j+=1
        strr+="═"
    strr += (" " + title + " ")
    j+= 2 + len(title)
    for i in range(j, tLen):
        strr+="═"
    strr += "╗\n"
    strr+= "╠═"
    for i in range(nTF):
        #strr +=  "╔"
        for j in range(nd + 6):
            strr+="═"
        if i != nTF - 1:
            strr += "╦"
    strr+="═╣\n"
    for j in range(6):
        strr+= "║ "
        for i in range(len(matrix)):
            t_nd = nd
            if (abs(matrix[i][j]) >= 9999):
                nm = len(str(abs(round(matrix[i][j]))))
                while t_nd > 0 and nm > 6:
                    t_nd = t_nd - 1
                    nm = nm - 1
            fmat = "{:" + str(nd + 6) +"." + str(t_nd) + "f}"

            strr = strr + fmat.format(matrix[i][j])
            if i != nTF - 1:
                strr = strr + ","
        strr+=" ║\n"
    strr+= "╠═"
    for i in range(nTF):
        #strr +=  "╚"
        for j in range(nd + 6):
            strr+="═"
        if i != nTF - 1:
            strr += "╩"
    strr+="═╣\n"
    strr +="╚"
    for i in range(2 * nTF * (nd+1) + (2*nTF+1)):
        strr+="═"
    strr += "╝\n"
    return strr


def disp2(matrix, nd = 3, title = "MATRIX", pdims = True, h=""):
    lines = d_help(matrix, nd, title, pdims, h)
    for str in lines:
        print(str)

def progressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
    percent = ("{0:." + str(decimals) + "f}").format(100*(iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total:
        print("")


def d_help(matrix, nd = 3, title = "MATRIX", pdims = True, h=""):
    t_bar = ""
    t_tl = "╔"
    t_bl = "╚"
    #╚╔╝╗║═ Symbols Required

    lines = []
    #Accounts for Even or Odd amounts of letters in a title
    if (len(title) % 2 == 0):
        t_tl = t_tl + "═"
        t_bl = t_bl + "═"

    #Accounts for a List of Objects, Calls itself Recursively
    if isinstance(matrix, list):
        i = 0
        lines.append(t_tl + "════════════" + " " + title + " BEGIN " + "════════════" + "╗")
        for mat in matrix:
            if ~isinstance(mat, list) and ~isinstance(mat, tuple):
                print(mat)
            else:
                if pdims:
                    print("Dim " + str(i) + ":")
                t_list = (d_help(mat))
                for strn in t_list:
                    lines.append(strn)
            i = i + 1
        lines.append(t_bl + t_bar + "════════════" + title + " END ═" + "════════════" + "╝")
        return;

    shape = 0

    #Variety of try catch to prevent crashes due to liberal use of disp()
    try:
        try:
            shape = matrix.shape
        except:
            #Panda obects IIRC use shape as a method
            shape = matrix.shape()

        dims = len(shape)
        if dims >= 2:
            t_key = shape[dims - 1]
        else:
            t_key = max(shape)
    except:
        #If all else fails, print Normally
        lines.append(str(matrix))
        return
    #Formats correct number of top and bottom markers for t_bar
    while(len(title) + 8 + (len(t_bar) * 2)) < (t_key * (nd + 7) ):
        t_bar = t_bar + "═"

    #Prints a single Dimension Vector
    if dims == 1:
        cn = 0
        if h == "╔ ":
            cn = 1
        elif h == "╚ ":
            cn = 2
        else:
            h = h + "║ "
        for i in range(shape[0]):
            t_nd = nd
            if (abs(matrix[i]) >= 9999):
                nm = len(str(abs(round(matrix[i]))))
                while t_nd > 0 and nm > 6:
                    t_nd = t_nd - 1
                    nm = nm - 1
            fmat = "{:" + str(nd + 6) +"." + str(t_nd) + "f}"


            h = h + fmat.format(matrix[i])
            if i != shape[0] - 1:
                h = h + ","

        if cn == 0:
            h = h + " ║"
        elif cn == 1:
            h = h + " ╗"
        else:
            h = h + " ╝"

        lines.append(h)

    #Prints traditional Square Matrix, allows for title
    elif dims == 2:
        if title != "MATRIX":
            lines.append(t_tl + t_bar + " " + title + " BEGIN " + t_bar + "╗")
        for i in range(shape[0]):
            if i == 0:
                t_list = d_help(matrix[i,], nd = nd, h = "╔ ")
                for strn in t_list:
                    lines.append(strn)
            elif i == shape[0] - 1:
                t_list = d_help(matrix[i,], nd = nd, h = "╚ ")
                for strn in t_list:
                    lines.append(strn)
            else:
                t_list = d_help(matrix[i,], nd = nd)
                for strn in t_list:
                    lines.append(strn)
        if title != "MATRIX":
            lines.append(t_bl + t_bar + "═ " + title + " END ═" + t_bar + "╝")

    #Prints 3D Matrix by calling 2D recursively
    elif dims == 3:
        lines.append(t_tl + t_bar + " " + title + " BEGIN " + t_bar + "╗")
        for i in range(shape[0]):
            if pdims:
                lines.append("DIM " + str(i) + ":")
            t_list = d_help(matrix[i,], nd = nd)
            for strn in t_list:
                lines.append(strn)
        lines.append(t_bl + t_bar + "═ " + title + " END ═" + t_bar + "╝")

    #Prints 4D Matrix by calling 3D recursively
    elif dims == 4:
        lines.append(t_tl + t_bar + "══ " + title + " BEGIN ══" + t_bar + "╗")
        for i in range(shape[0]):
            t_list = d_help(matrix[i,], nd = nd, title = title + " d:" + str(i), pdims = pdims)
            for strn in t_list:
                lines.append(strn)
        lines.append(t_bl + t_bar + "═══ " + title + " END ═══" + t_bar + "╝")
    else:
        taux = "═"
        for i in range (dims - 3):
            taux = taux + taux
        lines.append(t_tl + t_bar + taux +" " + title + " BEGIN " + taux + t_bar + "╗")
        for i in range(shape[0]):
            t_list = d_help(matrix[i,], title = title + " s" + str(i))
            for strn in t_list:
                lines.append(strn)
        lines.append(t_bl + t_bar + taux + "═ " + title + " END ═" + taux + t_bar + "╝")
    return lines

    #More dimensions can be added as needed if neccessary


def mult(mat1, mat2):
    mat3 = mat1 @ mat2
    lines1 = d_help(mat1)
    lines2 = d_help(mat2)
    lines3 = d_help(mat3)

    nh = max(len(lines1), len(lines2), len(lines3)) / 2

    dim1 = len(lines1[0])
    dim2 = len(lines2[0])
    dim3 = len(lines3[0])

    lines4 = []
    i = 0
    while (i < len(lines1) or i < len(lines2) or i < len(lines3)):
        lines4.append("")
        if i < len(lines1):
            lines4[i] = lines4[i] + lines1[i]
        else:
            for j in range(dim1):
                lines4[i] = lines4[i] + " "
        if i == nh:
            lines4[i] = lines4[i] + " * "
        else:
            lines4[i] = lines4[i] + "   "
        if i < len(lines2):
            lines4[i] = lines4[i] + lines2[i]
        else:
            for j in range(dim2):
                lines4[i] = lines4[i] + " "
        if i == nh:
            lines4[i] = lines4[i] + " = "
        else:
            lines4[i] = lines4[i] + "   "
        if i < len(lines3):
            lines4[i] = lines4[i] + lines3[i]
        else:
            for j in range(dim3):
                lines4[i] = lines4[i] + " "
        i = i + 1
    for line in lines4:
        print(line)
