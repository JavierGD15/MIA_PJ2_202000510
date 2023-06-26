import re

def parse_command(command):
    patterns = {
        'Configure': r'configure -type->(.*?) -encrypt_log->(.*?) -encrypt_read->(.*?) (-llave->\"(.*?)\")?',
        'create': r'create -name->(.*?) -path->(.*?) -body->\"(.*?)\"',
        'delete': r'delete -path->(.*?) (-name->\"(.*?)\")?',
        'copy': r'copy -from->(.*?) -to->(.*)',
        'transfer': r'transfer -from->(.*?) -to->(.*?) -mode->\"(.*?)\"',
        'rename': r'rename -path->(.*?) -name->(.*)',
        'modify': r'modify -path->(.*?) -body->\"(.*?)\"',
        'add': r'add -path->(.*?) -body->\"(.*?)\"',
        'exec': r'exec -path->(.*)',
        'backup': r'backup'
}

    

    for cmd, pattern in patterns.items():
        
        match = re.match(pattern, command, re.IGNORECASE)
        if match:
            return cmd, match.groups()

    return None, None

#ejemplo de exec
#exec -path->"C:\Users\josea\Documents\GitHub\Archivos_P1\Archivos_P1-develop\Archivos_P1\org\Archivos\prueba.txt"