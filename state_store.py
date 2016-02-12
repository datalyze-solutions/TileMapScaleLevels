# -*- coding: utf-8 -*-
"""
Get some kind of one-way data binding like Facebook's FLUX.
Prevents cross  connections while sharing states (e.x. checked)
between severel gui elements.
"""

class StateStore(object):

    def __init__(self):
        """wrapper that holds multiple StateVariables"""
        self._variables = {}

    def add(self, name, value):
        """Add a new variable to the store

        Args:
            name (str): Name of the new variable. Whitespaces will be stripped!
            value (object): Initial value of the new variable.
        """
        name = name.replace(' ', '')
        stateVariable = StateVariable(value)
        self._variables[name] = stateVariable
        setattr(self, name, stateVariable)
        return stateVariable

    def remove(self, name):
        """remove an existing variable

        Args:
            name (str): Name of variable to remove.

        Returns:
            True if removal was successfull.
            False if name was not found.
        """
        if name in self._variables:
            self._variables.pop(name)
            return True
        else:
            return False

    def variables(self):
        """Return all registered StateVariables"""
        return self._variables

    def update(self):
        """Call update on all variables"""
        for variable in self._variables.values():
            variable.update()

class StateVariable(object):

    def __init__(self, value):
        """Binds a value to methods of registered components."""
        self._value = value
        self._lastValue = None
        self._registry = []

    def register(self, component, method, dtype):
        """registers a new object and binds _value to method

        Args:
            component (object): Object to register.
            method (string): Method of component to bind _value to.
            dtype (method): Data type for method to set. str, float, int, bool

        Returns:
            True if component added successfully or still registered
        """
        try:
            # check if method is present
            getattr(component, method, dtype)
            if [component, method, dtype] not in self._registry:
                self._registry.append([component, method, dtype])
                return True
            else:
                return True
        except:
            raise

    def unregister(self, component, method, dtype):
        """unregister a registered component

        Args:
            component (object): Object to register.
            method (string): Method of component to bind _value to.
            dtype (method): Data type for method to set. str, float, int, bool

        Returns:
            True if unregistration was successfull. 
            False if unregistration was unsuccessfull.
        """
        if [component, method, dtype] in self._registry:
            self._registry.remove([component, method, dtype])
            return True
        else:
            return False

    def update(self):
        """Updates all registered components. Blocks signals of componenents before setting a value."""
        for [component, method, dtype] in self._registry:
            component.blockSignals(True)
            getattr(component, method)(dtype(self._value))
            component.blockSignals(False)

    def value(self):
        """Get _value"""
        return self._value

    def setValue(self, value):
        "Set _value and call update"
        self._value = value
        # only run update on real changes
        if self._lastValue != value:
            self.update()
            self._lastValue = value

    def __repr__(self):
        return u"{}".format(self._value)

if __name__ == '__main__':
    from PyQt4 import QtGui, QtCore
    import sys
    from random import random
    store = StateStore()
    store.add("value", 10)
    store.add("peter", 10)

    def setRandomValue():
        store.value.setValue(int(random() * 100))

    app = QtGui.QApplication(None)

    widget = QtGui.QPushButton()
    widget.resize(50, 20)
    widget.move(200, 200)
    widget.clicked.connect(setRandomValue)
    widget.show()

    widget2 = QtGui.QPushButton()
    widget2.resize(50, 20)
    widget2.move(200, 250)
    widget2.clicked.connect(setRandomValue)
    widget2.show()

    widget3 = QtGui.QSpinBox()
    widget3.resize(50, 20)
    widget3.move(200, 300)
    widget3.valueChanged.connect(setRandomValue)
    widget3.show()

    store.value.register(widget, "setText", str)
    store.value.register(widget2, "setText", str)
    store.value.register(widget3, "setValue", int)
    store.value.setValue(10)
    store.peter.setValue(10)

    sys.exit(app.exec_())
    