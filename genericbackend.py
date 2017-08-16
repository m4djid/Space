# Classe générique pour la gestion du backend
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def getNode(self, target, parent, ancestor):
        # Retourne la représentation XML de la node
        raise NotImplementedError('users must define getNode to use this base class')

    @abstractmethod
    def createNode(self, targetUri):
        # Creation de la node
        raise NotImplementedError('users must define getNode to use this base class')

    @abstractmethod
    def setNode(self, target, parent, ancestor, properties):
        # Initialise la node
        raise NotImplementedError('users must define setNode to use this base class')

    @abstractmethod
    def copyNode(self, targetUri, locationUri):
        # Copie la node et ses enfants
        raise NotImplementedError('users must define copyNode to use this base class')

    @abstractmethod
    def moveNode(self, targetUri, locationUri):
        # Deplace la node et ses enfants
        raise NotImplementedError('users must define moveNode to use this base class')

    @abstractmethod
    def deleteNode(self, target, parent, ancestor, targetUri):
        # Deplace la node et ses enfants
        raise NotImplementedError('users must define deleteNode to use this base class')

    @abstractmethod
    def pushToVoSpace(self, targetUri, **kwargs):
        # Execute un push to VOSpace
        raise NotImplementedError('users must define pushToVoSpace to use this base class')

    @abstractmethod
    def pushFromVoSpace(self, targetUri, **kwargs):
        # Execute un push from VOSpace
        raise NotImplementedError('users must define pushFromVoSpace to use this base class')

    @abstractmethod
    def pullFromVoSpace(self, targetUri, **kwargs):
        # Execute un pull from VOSpace
        raise NotImplementedError('users must define pullFromVoSpace to use this base class')

    @abstractmethod
    def pullToVoSpace(self, targetUri, endpointUri):
        # Execute un pull to VOSpace
        raise NotImplementedError('users must define pullToVoSpace to use this base class')
