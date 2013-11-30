from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient
from wokkel.xmppim import PresenceProtocol
from wokkel.xmppim import RosterClientProtocol
from wokkel.xmppim import RosterItem
from wokkel.muc import MUCClient
from twisted.words.protocols.jabber.jid import JID

from jabber_bot import EchoBotProtocol
from jabber_bot import BotPresenceClientProtocol
from jabber_bot import MUCGreeter

application = service.Application("echobot")

xmppclient = XMPPClient(jid.internJID(
    "simulator@idahogray.home/echobot"), "simulator",
    host="vmserver.idahogray.home")
xmppclient.logTraffic = True

echobot = EchoBotProtocol()
echobot.setHandlerParent(xmppclient)

roster = RosterClientProtocol()
roster.setHandlerParent(xmppclient)
a = roster.setItem(RosterItem(JID("keith@idahogray.home")))

presence = BotPresenceClientProtocol()
presence.setHandlerParent(xmppclient)

mucHandler = MUCGreeter(JID('test_room@conference.idahogray.home'), 'simulator_muc')
mucHandler.setHandlerParent(xmppclient)

xmppclient.setServiceParent(application)

