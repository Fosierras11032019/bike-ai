
ROLES = {
    "Diseñador" : ["imagenes"],
    "Redactor"  : ["texto"],
    "Aprobador" : ["texto", "imagenes","revision"]
}
    
def get_permissions(role):
    return ROLES.get(role, [])
