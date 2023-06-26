import re

def parse_command(command):
    patterns = {
        'create': r'create -name->(.*?) -body->\"(.*?)\" -path->(.*?) -type->(.*?)',
        'delete': r'delete -path->(.*?)( -name->\"(.*?)\")? -type->(.*?)',
        'copy': r'copy -from->(.*?) -to->(.*) -type_to->(.*?) -type_from->(.*?)',
        'transfer': r'transfer -from->(.*?) -to->(.*?) -type_to->(.*?) -type_from->(.*?)',
        'rename': r'rename -path->(.*?) -name->(.*) -type->(.*?)',
        'modify': r'modify -path->(.*?) -body->\"(.*?)\" -type->(.*?)',
        'backup': r'backup -type_to->(.*?) -type_from->(.*?)( -ip->(.*?))?( -port->(.*?))? -name->\"(.*?)\"',
        'recovery': r'recovery -type_to->(.*?) -type_from->(.*?)( -ip->(.*?))?( -port->(.*?))? -name->\"(.*?)\"',
        'delete_all': r'delete_all -type->(.*?)',
        'open': r'open -type->(.*?)( -ip->(.*?))?( -port->(.*?))? -name->\"(.*?)\"',
}
    for cmd, pattern in patterns.items():
        
        match = re.match(pattern, command, re.IGNORECASE)
        if match:
            return cmd, match.groups()

    return None, None

#ejemplo de exec
#exec -path->"C:\Users\josea\Documents\GitHub\Archivos_P1\Archivos_P1-develop\Archivos_P1\org\Archivos\prueba.txt"