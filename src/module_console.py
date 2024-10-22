class style():
    END      = '\33[0m'

    BOLD     = '\33[1m'
    DARK     = '\33[2m'
    ITALIC   = '\33[3m'
    UNDER    = '\33[4m'
    SELECTED = '\33[7m'
    EMPTY    = '\33[8m'
    STRIKE   = '\33[9m'
    DBLUNDER = '\33[21m'

    BLACK   = '\33[30m'
    GREY    = '\33[90m'
    RED     = '\33[31m'
    RED2    = '\33[91m'
    GREEN   = '\33[32m'
    GREEN2  = '\33[92m'
    YELLOW  = '\33[33m'
    YELLOW2 = '\33[93m'
    BLUE    = '\33[34m'
    BLUE2   = '\33[94m'
    VIOLET  = '\33[35m'
    VIOLET2 = '\33[95m'
    BEIGE   = '\33[36m'
    BEIGE2  = '\33[96m'
    WHITE   = '\33[37m'
    WHITE2  = '\33[97m'

    BLACKBG   = '\33[40m'
    GREYBG    = '\33[100m'
    REDBG     = '\33[41m'
    REDBG2    = '\33[101m'
    GREENBG   = '\33[42m'
    GREENBG2  = '\33[102m'
    YELLOWBG  = '\33[43m'
    YELLOWBG2 = '\33[103m'
    BLUEBG    = '\33[44m'
    BLUEBG2   = '\33[104m'
    VIOLETBG  = '\33[45m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG   = '\33[46m'
    BEIGEBG2  = '\33[106m'
    WHITEBG   = '\33[47m'
    WHITEBG2  = '\33[107m'


def Test():
    import os
    os.system("")

    codes = [0, 1, 2, 3, 4, 7, 8, 9, 21, 30, 90, 31, 91, 32, 92, 33, 93, 34, 94, 35, 95, 36, 96, 37, 97, 40, 100, 41, 101, 42, 102, 43, 103, 44, 104, 45, 105, 46, 106, 47, 107]

    for code in codes:
        print("\33[" + str(code) + "m\\33[" + str(code) + "m\033[0m")


def Info(content):
    print(style.WHITE + content + style.END)


def Pass(content):
    print(style.GREEN + content + style.END)


def Warn(content):
    print(style.YELLOW + content + style.END)


def Error(content):
    print(style.RED + content + style.END)
