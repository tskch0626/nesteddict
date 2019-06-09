from collections import defaultdict
import re

ndict = lambda: defaultdict(ndict)

class nesteddict:
    def __init__(self):
        self.nd = ndict()

    def __recursive_add(self, nd, keys, val):
        if len(keys)==1:
            nd[keys[0]] = val
        else:
            self.__recursive_add(nd[keys[0]], keys[1:], val)

    def add(self, keys, val):
        self.__recursive_add(self.nd, keys, val)

    def __recursive_find(self, nd, val, keys):
        if nd==val:
            return keys
        elif type(nd)!=defaultdict:
            return []
        else:
            search_keys = list(nd.keys())
            for key in search_keys:
                keys.append(key)
                return_keys = self.__recursive_find(nd[key], val, keys)
                if return_keys!=[]:
                    return return_keys
                else:
                    keys.pop(-1)
            
            return []

    def find(self, val):
        keys = []
        return self.__recursive_find(self.nd, val, keys)

    def __recursive_search(self, nd, keys):
        if type(nd)!=defaultdict:
            return False
        if len(keys)==0:
            return False
        elif keys[0] in nd.keys():
            if len(keys)==1:
                return True
            else:
                return self.__recursive_search(nd[keys[0]], keys[1:])
        else:
            return False 

    def search(self, keys):
        return self.__recursive_search(self.nd, keys)

    def __recursive_delete(self, nd, keys):
        if len(keys)==1:
            if len(nd.keys())>=2:
                nd.pop(keys[0])
                return True
            else:
                return False
        else:
            fin = self.__recursive_delete(nd[keys[0]], keys[1:])
            if not fin and len(nd.keys())>=2:
                nd.pop(keys[0])
                return True
            else:
                return fin
    
    def delete(self, keys):
        if self.search(keys):
            if not self.__recursive_delete(self.nd, keys):
                self.nd.pop(keys[0])
            return True
        return False
    
    def delete_val(self, val):
        keys = self.find(val)
        if keys!=[]:
            self.delete(keys)
            return True
        return False   

    def __recursive_count(self, nd, cnt):
        if type(nd)!=defaultdict:
            return cnt+1
        else:
            for key in nd.keys():
                cnt = self.__recursive_count(nd[key], cnt)
            return cnt

    def count_vals(self):
        cnt = 0
        return self.__recursive_count(self.nd, cnt)

    def __get_successive_keys(self, nd, keys):
        if len(keys)==1:
            if type(nd[keys[0]])!=defaultdict:
                return []
            else:
                return list(nd[keys[0]].keys())
        else:
            return self.__get_successive_keys(nd[keys[0]], keys[1:])

    def succesive_keys(self, keys):
        if self.search(keys):
            return self.__get_successive_keys(self.nd, keys)
        return []

    def __recursive_write_XML(self, nd, f, i):
        if type(nd)!=defaultdict:
            f.write("\t"*i + "{0:s}\n".format(nd))
            return
        else:
            i+=1
            for key in nd.keys():
                f.write("\t"*i + "<{0:s}>\n".format(key))
                self.__recursive_write_XML(nd[key], f, i)
                f.write("\t"*i + "</{0:s}>\n".format(key))
            return

    def output_nested_dict_as_XML(self, filename):
        with open(filename+".xml", "w") as f:
            self.__recursive_write_XML(self.nd, f, -1)

    def __recursive_get_val(self, nd, keys):
        if type(nd)!=defaultdict:
            return nd
        else:
            return self.__recursive_get_val(nd[keys[0]], keys[1:])

    def get_val(self, keys):
        if self.search(keys):
            return self.__recursive_get_val(self.nd, keys)
        else:
            return None
    
    def make_ndict_from_XML(self, xmlfile):
        keys = []
        with open(xmlfile, "r") as f:
            for line in f:
                if re.match(r'^\s*</', line):
                    keys.pop(-1)
                else:
                    result = re.match(r'^\s*<(.+)>', line)
                    if result:
                        keys.append(result.group(1))
                    else:
                        val = line.strip()
                        self.add(keys, val)