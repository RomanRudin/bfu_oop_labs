Реализовать механизм оповещения других классов произвольным классом об изменении его свойств:
 - после изменения
 - до изменения (свойство должно поменяться непосредственно перед изменением с возможностью запрета изменения) (obj, prop_name, old_value, new_value) -> bool (валидатор)

 Это будет система: 
 Observer
 Broadcaster, Listener
 Ivent-Driven programming

Example C#: 
 - INotifyPropertyChanged(event)
 - INotifyPropertyChanging(event)