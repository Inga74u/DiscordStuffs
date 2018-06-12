Default = "Default"
Administrator = "Admin"
Kick = "Kick"
Ban = "Ban"
ManageChannels = "ManageChan"
ManageServer = "ManageServer"
ManageMessages = "ManageMessages"
MoveMembers = "MoveMembers"
ManageRoles = "ManageRoles"

def PermsList(Perms):
    P = []
    
    if Perms.administrator:
        P.append(Administrator)
    
    if Perms.kick_members:
        P.append(Kick)
    
    if Perms.ban_members:
        P.append(Ban)
        
    if Perms.manage_channels:
        P.append(ManageChannels)
    
    if Perms.manage_server:
        P.append(ManageServer)
    
    if Perms.manage_messages:
        P.append(ManageMessages)
    
    if Perms.move_members:
        P.append(MoveMembers)
    
    if Perms.manage_roles:
        P.append(ManageRoles)
    
    return P
