import os


class Path:
    def __init__(self, path=None):
        self.CWD = os.getcwd()  # текущая рабочая директория
        self.sep = os.sep
        if path:
            self.__current = os.fspath(path)
        else:
            self.__current = os.path.dirname(__file__)  # путь к родительскому каталогу, где расположен файл с классом Path

    def parent(self):
        self.__current = os.path.dirname(self.__current)  # родительский путь на директорию выше
        return self
    
    def add_child(self, *dirname):
        self.__current = os.path.join(self.__current, *dirname)
        return self

    def get_children(self, *, just_names=True):
        if just_names:
            return os.listdir(self.__current)        
        children = []
        for child in os.scandir(self.__current):
            if child.is_dir():
                obj = Path(child.path)
                children.append(obj)
        return children

    def exists(self):
        return os.path.exists(self.__current) 
    
    def is_link(self):
        return os.path.islink(self.__current) 

    def depth(self):
        return len(self.__current.split(self.sep)) - 1
    
    def get_path(self):
        return self.__current
    
    def create(self):
        if not self.exists():
            os.makedirs(self.__current)
        return self

    def __add__(self, obj):
        if isinstance(obj, str):
            return Path(os.path.join(self.__current, obj))
        elif isinstance(obj, Path):
            return Path(os.path.join(self.__current, obj.__current))
        return NotImplemented
    
    def __radd__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return Path(os.path.join(self.__current, obj))  # Альтернативное поведение, когда у первого операнда нет соответствующего метода
        
    def __truediv__(self, obj):
        if isinstance(obj, str):
            return Path(os.path.join(self.__current, obj))
        elif isinstance(obj, Path):
            return Path(os.path.join(self.__current, obj.__current))
        return NotImplemented
    
    def __rtruediv__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return Path(os.path.join(self.__current, obj))

    def __len__(self):
        """Returns path depth."""
        return self.depth()  # Если записать depth() без self - depth() будет искаться в глобальной области видимости
    
    def __bool__(self):
        """Returns True if exists."""
        return self.exists()

    def __eq__(self, obj):
        if isinstance(obj, str):
            return self.__current == obj
        elif isinstance(obj, Path):
            return self.__current == obj.__current
        return NotImplemented
    
    def __ne__(self, obj):
        return self.__current != obj.current
    
    # def __ne__(self, obj):  # Так делать нельзя!
    #     return NotImplemented
    
    def __contains__(self, obj):
        if isinstance(obj, str):
            return obj in self.__current
        elif isinstance(obj, Path):
            return obj.__current in self.__current
        return NotImplemented   

    def __fspath__(self):
        return str(self)  # Служебный метод, делает наш объект (path) "похожим" на путь для использования в методе os.path.join.
        
    def __repr__(self):
        return f"Path('{self.__current}')"

    def __str__(self):
        return self.__current





