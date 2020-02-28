STR_EOL = '\n'

class IOLeaf(object):
    def __init__(self, head='Null'):
        # [String]head
        # [List[String]]tail
        # [String] single_row: single_row and default:multirow
        self.head = head
        self.tail = []
        self.single_row = False
        self.__indent_level = 0

    def __str__(self):
        tmp_str = str(self.head) + ' '
        for s in self.tail:
            if self.single_row:
                tmp_str += str(s) + ' '
            else:
                tmp_str += STR_EOL + (self.__indent_level+1)*'\t' + str(s) 
        tmp_str = self.__indent_level*'\t' + '(' + tmp_str + ('' if self.single_row else '\n'+self.__indent_level*'\t') + ')'
        return tmp_str

    def _setHead(self, head_str):
        # [string]head_str
        self.head = head_str

    def _setTailList(self, tail_str_list):
        # [list[string]] a list of string
        self.tail = tail_str_list
        
    def _appendTail(self, tail_str):
        # [string]tail_str
        self.tail.append(str(tail_str))

    def _setTail(self, *tail):
        # [string]tail
        for f in tail:
            self.tail.append(f)

    def _setSingleRow(self):
        self.single_row = True

    def _setIndentLevel(self, level):
        self.__indent_level = level

    def _incrIndentLevel(self):
        self.__indent_level += 1
    
    def _decrIndentLevel(self):
        self.__indent_level -= 1

    def _deepCopy(self):
        tmp = IOLeaf()
        tmp.head = self.head
        tmp.tail = self.tail
        tmp.single_row = self.single_row
        tmp._setIndentLevel(self.__indent_level)
        return tmp

class IOTree(object):
    
    def __init__(self, root="Null"):
        # [String]root: root string definition
        # [List]leaf_list: a list of sub-trees or leaves
        self.root = root
        self.leaf_list = []
        self.__indent_level = 0

    def __str__(self):
        tmp_str = str(self.root) + ' ' + STR_EOL
        for s in self.leaf_list:
            s._incrIndentLevel()
            tmp_str += str(s) + ' ' + STR_EOL
            s._decrIndentLevel()
        tmp_str = self.__indent_level*'\t'+'(' + tmp_str + STR_EOL + self.__indent_level*'\t' + ')'
        return tmp_str

    def __getitem__(self, index):
        return  self.leaf_list[index]

    def __setitem__(self, index, value):
        self.leaf_list[index] = value

    @property
    def size(self):
        return len(self.leaf_list)

    def _setRoot(self, root):
        # [String]root, root name
        self.root = root

    def setLeafList(self, leaf_list):
        # [List[IOLeaf]] a list of leaf
        self.leaf_list = leaf_list

    def _appendLeafList(self, leaf):
        # [IOLeaf]leaf
        self.leaf_list.append(leaf)

    def setLeaf(self, *leaves):
        # [IOLeaf]leaves
        for leaf in leaves:
            self.leaf_list.append(leaf)

    def _incrIndentLevel(self):
        self.__indent_level += 1
        for leaf in self.leaf_list:
            leaf._incrIndentLevel()
    
    def _decrIndentLevel(self):
        self.__indent_level -= 1
        for leaf in self.leaf_list:
            leaf._decrIndentLevel()
    
    def _deepCopy(self):
        dst = IOTree()
        dst.root = self.root
        dst.__indent_level = self.__indent_level
        for leaf in self.leaf_list:
            dst._appendLeafList(leaf.deepCopy())
        return dst


class IOAttr(object):
    
    def __init__(self, attr_view, attr_list):
        self.attr_view = attr_view
        self.attr_list = attr_list
        self.freeze = False

    def _addAttr(self, attr_name, attr_default_value):
        self.freeze = False
        self.attr_view.append(attr_name)
        self.attr_list[attr_name] = attr_default_value


class IOAttrLeaf(IOLeaf, IOAttr):
    
    def __init__(self, head="Null"):
        IOLeaf.__init__(self, head)
        IOAttr.__init__(self, attr_view=[], attr_list={})

    def __getattr__(self, attr):
        available_attr_list = []
        for k in self.attr_list:
            available_attr_list.append(k)
        if attr in available_attr_list:
            return self.attr_list[attr]
        else:
            print("Wrong Attribute!")
            print("Available attributes are:", available_attr_list)

    def _construct(self):
        if not self.freeze:
            for ( attr_name, attr_value ) in self.attr_list.items():
                if attr_name in self.attr_view:
                    self._appendTail(
                        str(attr_name) + " = " + str(attr_value)
                    )
        self.freeze = True

    def __str__(self):
        self._construct()
        return IOLeaf.__str__(self)

class IOAttrTree(IOTree):
    
    def __init__(self, root="Null"):
        IOTree.__init__(self, root)