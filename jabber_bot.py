from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol
from wokkel.xmppim import AvailablePresence
from wokkel.xmppim import PresenceClientProtocol

class EchoBotProtocol(MessageProtocol):
    def connectionMade(self):
        print("Connected!")

        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print("Disconnected: %s" % reason)

    def onMessage(self, msg):
        print(str(msg))
        self.send(AvailablePresence())

        if msg["type"] == 'chat' and msg.body:
            reply = domish.Element((None, "message"))
            reply['to'] = msg['from']
            reply['from'] = msg['to']
            reply['type'] = 'chat'
            reply.addElement("body", content="echo: %s" % str(msg.body))

            self.send(reply)


class BotPresenceClientProtocol(PresenceClientProtocol):
    def connectionInitialized(self):
        PresenceClientProtocol.connectionInitialized(self)
        self.available(statuses={None: 'Here'})
        print("Connection Initialized")

    def subscribeReceived(self, entity):
        self.subscribed(entity)
        self.available(statuses={None: 'Here'})
        print("Subscribe Received")

    def unsubscribeReceived(self, entity):
        self.unsubscribed(entity)
        print("Unsubscribe Received")
