import os


class Path:
    def __init__(self, path=None):
        self.CWD = os.getcwd()  # текущая рабочая директория
        self.sep = os.sep
        if path:
            self.__current = os.fspath(path)
        else:
            self.__current = os.path.dirname(__file__)  # путь к родительскому каталогу, где расположен файл с классом Path

    def _get_current(self):
        return self.__current
    
    def _set_current(self, path):
        self.__current = os.fspath(path)

    def parent(self):
        self.__current = os.path.dirname(self)  # Так как есть __fspath__
    
    def exists(self):
        return os.path.exists(self)  # Так как есть __fspath__ 
    
    def is_link(self):
        return os.path.islink(self)  # Так как есть __fspath__

    def depth(self):
        return len(self.__current.split(self.sep)) - 1
    
    def get_path(self):
        return self.__current   

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
    
    def __contains__(self, obj):
        if isinstance(obj, str):
            return obj in self.__current
        elif isinstance(obj, Path):
            return obj.__current in self.__current
        return NotImplemented   

    def __fspath__(self):
        return str(self)  # Служебный метод, делает наш объект (path) "похожим" на путь для использования в методе os.path.join.
        
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.__current}')"

    def __str__(self):
        return self.__current
    

class Dir(Path):
    # Класс Dir использует полностью __init__ класса Path
    def add_child(self, *dirname):
        self._set_current(os.path.join(self._get_current(), *dirname))
        return self
    
    def get_children(self, *, just_names=True):
        if just_names:
            return os.listdir(self)        
        children = []
        for child in os.scandir(self):
            if child.is_dir():
                obj = Path(child.path)
                children.append(obj)
        return children
    
    def create(self):
        os.makedirs(self)
        return self
    
    def _join(self, obj):
        return Dir(os.path.join(self, obj))
    
    def __add__(self, obj):  # позволяет добавлять новые каталоги
        if isinstance(obj, str):
            return self._join(obj)
        elif isinstance(obj, Path):
            return self._join(obj)
        return NotImplemented
    
    def __radd__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return self._join(obj)  # Альтернативное поведение, когда у первого операнда нет соответствующего метода
        
    def __truediv__(self, obj):
        if isinstance(obj, str):
            return self._join(obj)
        elif isinstance(obj, Path):
            return self._join(obj)
        return NotImplemented
    
    def __rtruediv__(self, obj):
        if not isinstance(obj, str):
            return NotImplemented
        return self._join(obj)


class File(Path):
    def __init__(self, path):
        # Path.__init__(self, path) Для явного наследования __init__ (видно из какого класса)
        super().__init__()  # ищет __init__ родительского класса и его запускает: исполняется код Path.__init__
        self._set_current(os.fspath(path))  # переопределяем получение этого атрибута для класса File

    def depth(self):
        return super().depth() - 1  # Исполняется Path.depth    

    def file_name(self):
        return self._get_current().rsplit(self.sep)[-1]
    
    def parent(self):
        return Dir(self).parent()  # Создаем экземпляр Dir как есть, и потом к нему применяем ЕГО метод parent
    
        
    


    