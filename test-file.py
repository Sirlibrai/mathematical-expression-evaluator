import json
import re

class MySet:
    def __init__(self, *args):
        self._set = set(*args)

    def __contains__(self, x):
        return x in self._set

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{' + ', '.join((str(x) for x in self._set)) + '}'

dictat = {}
dicvalue = {}

def parse_declaration(valinfo):
    tree = valinfo['declared-variable']
    re.match ("x", valinfo['declared-variable'])
    value = parse_rvalue(valinfo['value'])
    if valinfo['declared-variable'] not in dictat.keys():
        dictat.update({valinfo['declared-variable']:(value)})
    dicvalue.update({tree: (value)})
    return (tree ,value)
    
def _rv_parse_set(valinfo):
    assert valinfo['operator'] == 'set'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    try:
        #return set(args)
        return MySet(args)
    except:
        return args
        
def _rv_parse_apply_function(valinfo):
    assert valinfo['operator'] == 'apply-function'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    return "apply_function(" + ', '.join((str(a) for a in args)) + ")"

def _rv_parse_equal(valinfo):
    assert valinfo['operator']=='equal'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    return int(args[0] == args[1])

def _rv_parse_is_function(valinfo):
    assert valinfo['operator'] == 'is-function'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    return "is_function(" + ', '.join((str(a) for a in args)) + ")"

def _rv_parse_tuple(valinfo):
    assert valinfo['operator']== 'tuple'
    args = [parse_rvalue(b) for b in valinfo['arguments']]
    return (tuple(x for x in args))

def _rv_parse_member(valinfo):
    assert valinfo['operator']=='member'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    return int(args[0] in args[1])

def _rv_parse_union(valinfo):
    assert valinfo['operator'] == 'union'
    result= [];
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    print len(args), args[0], '\n', args[1]
    for i in result:
        if i not in result:
            result.append(i)
    for j in result:
        if j not in result:
            result.append(j)
    return result   

def _rv_parse_set_difference(valinfo):
    assert valinfo['operator'] == 'set-difference'
    result = [];
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    for i in args[0]:
        if i != args[1][0]:
            result.append(i)
    print result        
    return result

def _rv_parse_intersection(valinfo):
    assert valinfo['operator'] == 'intersection'
    result = [];
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    for i in args[0]:
        print args[0],'intersect'
        for j in args[1]:
            print args[1],'intersect'
            if j == i:
                result.append(i)
    print result, 'intersect'    
    return result
    
def _rv_parse_domain(valinfo):
    assert valinfo['operator'] == 'domain'
    result = [];
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    for i in args[0]:
        if i != args[1][0]:
            result.append(i)
    return result
    
def _rv_parse_inverse(valinfo):
    assert valinfo['operator'] == 'inverse'
    args = [parse_rvalue(a) for a in valinfo['arguments']]
    return 'Undefined!' 
       
_rv_parser = {
    "apply-function": _rv_parse_apply_function,
    "equal":          _rv_parse_equal,
    "is-function":    _rv_parse_is_function,
    "set":            _rv_parse_set,
    "tuple":          _rv_parse_tuple,
    "member":         _rv_parse_member,
    "union":          _rv_parse_union,
    "set-difference": _rv_parse_set_difference,
    "intersection":   _rv_parse_intersection,
    "domain":         _rv_parse_domain,
    "inverse":        _rv_parse_inverse,
    
}

def parse_rvalue(valinfo):
#    try:
        if type(valinfo) is int:
            return valinfo
        elif type(valinfo) is set:
            return valinfo
        elif 'variable' in valinfo:
            if valinfo['variable'] not in dictat.keys():
                return 'Undefined!'
            if valinfo['variable'] in dictat.keys():
                return dictat[valinfo['variable']]    
        elif 'operator' in valinfo:
            opfunc = _rv_parser[valinfo['operator']]
            return opfunc(valinfo)
        
#    except TypeError:
#        return ('be ', valinfo)


def parse_json(data):
    declaration_list = data['declaration-list']
    for i in declaration_list:
        parse_declaration(i)
        
fo = open('output.txt', "w")
def writeToFile(variable, expression):
    fo.write("let")
    fo.write(variable)
    fo.write("be")
    fo.write(str(expression))
    fo.write(";\n")
    return
    
    with open("output.txt", "w") as outfile:   
	for i in dicvalue:
		if i is not None:
			temp = dicvalue[i]
                        print >> outfile, 'let', i, 'be', temp
    outfile.close()    
            
if __name__ == "__main__":
    jsoninput = open("input.json").read()
    data = json.loads(jsoninput)
    parse_json(data)