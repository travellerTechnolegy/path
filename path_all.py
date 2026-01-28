import os


class Path:
    def __init__(self, path=None):
        self.CWD = os.getcwd()  # текущая рабочая директория
        self.sep = os.sep
        if path:
            self.current = os.fspath(path)
        else:
            self.current = os.path.dirname(__file__)  # путь к родительскому каталогу, где расположен файл с классом Path

    def parent(self):
        self.current = os.path.dirname(self.current)  # родительский путь на директорию выше
        return self
    
    def add_child(self, *dirname):
        self.current = os.path.join(self.current, *dirname)
        return self

    def get_children(self, *, just_names=True):
        if just_names:
            return os.listdir(self.current)        
        children = []
        for child in os.scandir(self.current):
            if child.is_dir():
                obj = Path(child.path)
                children.append(obj)
        return children

    def exists(self):
        return os.path.exists(self.current) 
    
    def is_link(self):
        return os.path.islink(self.current) 

    def depth(self):
        return len(self.current.split(self.sep)) - 1
    
    def get_path(self):
        return self.current
    
    def create(self):
        if not self.exists():
            os.makedirs(self.current)
        return self

    def __add__(self, obj):  # позволяет добавлять новые каталоги
        if isinstance(obj, str):
            return Path(os.path.join(self.current, obj))
        elif isinstance(obj, Path):
            return Path(os.path.join(self.current, obj.current))
        return NotImplemented
    
    def __radd__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return Path(os.path.join(self.current, obj))  # Альтернативное поведение, когда у первого операнда нет соответствующего метода
        
    def __truediv__(self, obj):
        if isinstance(obj, str):
            return Path(os.path.join(self.current, obj))
        elif isinstance(obj, Path):
            return Path(os.path.join(self.current, obj.current))
        return NotImplemented
    
    def __rtruediv__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return Path(os.path.join(self.current, obj))

    def __len__(self):
        """Returns path depth."""
        return self.depth()  # Если записать depth() без self - depth() будет искаться в глобальной области видимости
    
    def __bool__(self):
        """Returns True if exists."""
        return self.exists()

    def __eq__(self, obj):
        if isinstance(obj, str):
            return self.current == obj
        elif isinstance(obj, Path):
            return self.current == obj.current
        return NotImplemented
    
    def __ne__(self, obj):
        return self.current != obj.current
    
    # def __ne__(self, obj):  # Так делать нельзя!
    #     return NotImplemented
    
    def __contains__(self, obj):
        if isinstance(obj, str):
            return obj in self.current
        elif isinstance(obj, Path):
            return obj.current in self.current
        return NotImplemented   

    def __fspath__(self):
        return str(self)  # Служебный метод, делает наш объект (path) "похожим" на путь для использования в методе os.path.join.
        
    def __repr__(self):
        return f"Path('{self.current}')"

    def __str__(self):
        return self.current
    

class File(Path):
    def __init__(self, path):
        # Path.__init__(self, path) Для явного наследования __init__ (видно из какого класса)
        super().__init__(path)  # ищет __init__ родительского класса и его запускает
        self.current = os.fspath(path)  # переопределяем получение этого атрибута для класса File

    def depth(self):
        return super().depth() - 1
    
    def create(self):
        return None

    def add_child(self, *dirname):
        return None
    
    def get_children(self, *, just_names=True):
        return None

    def file_name(self):
        return self.current.rsplit(self.sep)[-1]
    
    def __add__(self, obj):
        return NotImplemented
    
    def __radd__(self, obj):
        return NotImplemented
    
    def __truediv__(self, obj):
        return NotImplemented
    
    def __rtruediv__(self, obj):
        return NotImplemented
    
    def __repr__(self):
        return f"File('{self.current}')"
    
   







