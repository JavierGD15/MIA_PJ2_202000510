import re

def parse_command(command):
    
    patterns = {
        'create': {
            'required': [
                r'-name->(.*?)(?=\s*-|$)', 
                r'-path->(.*?)(?=\s*-|$)', 
                r'-body->\"(.*?)\"(?=\s*-|$)', 
                r'-type->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'delete': {
            'required': [
                r'-path->(.*?)(?=\s*-|$)', 
                r'-type->(.*?)(?=\s*-|$)'
            ],
            'optional': [
                r'-name->(.*?)(?=\s*-|$)'
            ]
        },
        'copy': {
            'required': [
                r'-from->(.*?)(?=\s*-|$)', 
                r'-to->(.*?)(?=\s*-|$)', 
                r'-type_to->(.*?)(?=\s*-|$)', 
                r'-type_from->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'transfer': {
            'required': [
                r'-from->(.*?)(?=\s*-|$)', 
                r'-to->(.*?)(?=\s*-|$)', 
                r'-type_to->(.*?)(?=\s*-|$)', 
                r'-type_from->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'rename': {
            'required': [
                r'-path->(.*?)(?=\s*-|$)', 
                r'-name->(.*?)(?=\s*-|$)', 
                r'-type->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'modify': {
            'required': [
                r'-path->(.*?)(?=\s*-|$)', 
                r'-body->\"(.*?)\"(?=\s*-|$)', 
                r'-type->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'backup': {
            'required': [
                r'-type_to->(.*?)(?=\s*-|$)', 
                r'-type_from->(.*?)(?=\s*-|$)', 
                r'-name->\"(.*?)\"(?=\s*-|$)'
            ],
            'optional': [
                r'-ip->(.*?)(?=\s*-|$)', 
                r'-port->(.*?)(?=\s*-|$)'
            ]
        },
        'recovery': {
            'required': [
                r'-type_to->(.*?)(?=\s*-|$)', 
                r'-type_from->(.*?)(?=\s*-|$)', 
                r'-name->\"(.*?)\"(?=\s*-|$)'
            ],
            'optional': [
                r'-ip->(.*?)(?=\s*-|$)', 
                r'-port->(.*?)(?=\s*-|$)'
            ]
        },
        'delete_all': {
            'required': [
                r'-type->(.*?)(?=\s*-|$)'
            ],
            'optional': []
        },
        'open': {
            'required': [
                r'-type->(.*?)(?=\s*-|$)', 
                r'-name->(.*?)(?=\s*-|$)'
            ],
            'optional': [
                r'-ip->(.*?)(?=\s*-|$)', 
                r'-port->(.*?)(?=\s*-|$)'
            ]
        },
    }

    matches_list = []

    for cmd, pattern_dict in patterns.items():
        matches = {}
        for pattern in pattern_dict['required']:
            match = re.findall(pattern, command, re.IGNORECASE)
            if match:
                arg = pattern.split('->')[0].lstrip('-')
                matches[arg] = match[0]
                
        if len(matches) != len(pattern_dict['required']):
            continue  

        for pattern in pattern_dict['optional']:
            match = re.findall(pattern, command, re.IGNORECASE)
            if match:
                arg = pattern.split('->')[0].lstrip('-')
                matches[arg] = match[0]
        
        total_params = len(matches)
        
        
        if re.match(r'^' + cmd, command, re.IGNORECASE):
            matches_list.append((cmd, matches, total_params))

    if matches_list:
        print(matches_list)
        matches_list.sort(key=lambda x: x[2], reverse=True)
        return matches_list[0][0], matches_list[0][1]

    return None, None 
