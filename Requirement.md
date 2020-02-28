# 需求文档

## 场景一

用户输入IOpad的cell定义，输入chip的floorplan的信息，size， powerplan，输入chip的top module的netlist，自动生产IO assignment文件。包括自动插入PG pad。

## 场景二

用户输入已经定义好的IO pad分配文档，同时输入使用的IO pad cell定义，应该是用户自己分配PG pad，并生成IO assignment 文件。

有方法能够解析给定的IO pad cell，有方法能解析给定的分配文档/表格，能根据fp信息自动算PG的位置（PG的位置也能被手动修改）

```python
def inputPadCell(pad_def_file):
    pass

def inputNetlist(netlist_file, top_module):
    pass

def inputChipInfo(chip_size, max_power, vdd, **params):
    pass

class IOAssignDef(object):
    def __init__(self):
        self.pad_def = {
            "top": [],
            "topright" : [],
            "right" : [],
            "bottomright": [],
            "bottom":[],
            "bottomleft":[],
            "left":[],
            "topleft":[]
        }

```
