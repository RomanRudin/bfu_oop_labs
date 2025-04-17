## Лабораторная работа 4 (валидация и автообновление)

Создать, класс позволяющий отслеживать изменения в нем, а также проводить валидацию изменений,
Реализуем паттерн Broadcaster/receiver или observer, симулируем событийное программирование.

1. Создать интерфейс / протокол IPropertyChangedListener / PropertyChangedListenerProtocol
  - on_property_changed(obj: T, property_name) -> None

2. Создать интерфейс / протокол INotifyDataChanged / DataChangedProtocol для отслеживания изменения свойств классов
 - add_property_changed_listener(listener: PropertyChangedListenerProtocol)
 - remove_property_changed_listener(listener: PropertyChangedListenerProtocol)

3. Реализовать класс, поддерживающий INotifyDataChanged / DataChangedProtocol с несколькими свойствами, изменение в каждом из которых приводит к вызову on_property_changed для всех слушателей класса

4. Создать интерфейс / протокол IPropertyChangingListener / PropertyChangingListenerProtocol
  - on_property_changing(obj: T, property_name, old_value, new_value) -> bool

5. Создать интерфейс / протокол INotifyDataChanging / DataChangingProtocol для валидации изменений свойств классов
 - add_property_changing_listener(listener: PropertyChangingListenerProtocol)
 - remove_property_changing_listener(listener: PropertyChangingListenerProtocol)

6. Реализовать класс, поддерживающий INotifyDataChanging / DataChangingProtocol с несколькими свойствами, попутка изменения в каждом из которых приводит к вызову on_property_changing для всех слушателей класса с возможностью недопущения изменений, если валидация не пройдена

7. Создать несколько слушателей DataChangedProtocol и несколько валидаторов DataChangingProtocol и продемонстрировать работу реализованной системы