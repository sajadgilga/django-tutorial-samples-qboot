class Observer:
    def data_changed(self, data):
        pass


class Observable:
    def subscribe(self, observer: Observer):
        pass


class ColdObservable(Observable):
    def __init__(self, source):
        self.source = source
        self.observers = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)
        observer.data_changed(self.source.data)


class HotObservable(Observable):
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.data_changed(data)


class SampleObserver(Observer):
    def data_changed(self, data):
        print(f'data is:', data)


data = [1, 2, 3, 4]

cold_observable = ColdObservable(data)
observer = SampleObserver()
observer1 = SampleObserver()
observer2 = SampleObserver()
cold_observable.subscribe(observer)
cold_observable.subscribe(observer1)
cold_observable.subscribe(observer2)

hot_observable = HotObservable()
hot_observable.subscribe(observer)
hot_observable.notify(data[0])
hot_observable.subscribe(observer1)
hot_observable.notify(data[1])
hot_observable.subscribe(observer2)

hot_observable.notify(data[2])
