Default = "Default"
Administrator = "Admin"

def PermsList(Perms):
    P = []
    
    if Perms.administrator:
        P.append(Administrator)
    
    return P
