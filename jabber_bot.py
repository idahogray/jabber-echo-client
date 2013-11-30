from twisted.words.xish import domish
from twisted.python import log
from wokkel.xmppim import MessageProtocol
from wokkel.xmppim import AvailablePresence
from wokkel.xmppim import PresenceClientProtocol
from wokkel.muc import MUCClient

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

class MUCGreeter(MUCClient):
    def __init__(self, room_jid, nick):
        MUCClient.__init__(self)
        self.room_jid = room_jid
        self.nick = nick

    def connectionInitialized(self):
        def joinedRoom(room):
            if room.locked:
                return self.configure(room.roomJID, {})

        MUCClient.connectionInitialized(self)

        d = self.join(self.room_jid, self.nick)
        d.addCallback(joinedRoom)
        d.addCallback(lambda _: log.msg("Joined Room"))
        d.addErrback(log.err, "Join Failed")

    def receivedGroupChat(self, room, user, message):
        if message.body.startswith(self.nick + u":"):
            nick, text = message.body.split(":", 1)
            text = text.strip().lower()
            if text == u"hello":
                body = u"%s: Hi!" % (user.nick)
                self.groupChat(self.room_jid, body)

