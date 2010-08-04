# -*- encoding: utf-8 -*-
import httplib, urllib, Cookie, time
from exceptions import Exception
from lxml import etree


class PmbClient:
    """Classe permettant de charger des pages par http, en utilisant des 
    cookies pour conserver la session (authentification).
    """
    handle = None
    cookies = ""

    def __init__ (self):
        pass

    def __del__ (self):
        if self.handle:
            self.handle.close ()

    def connect (self, server, port=80):
        """Etablit la connexion au serveur http `server`, sur le `port`.
        """
        if self.handle:
            self.handle.close ()

        self.handle = httplib.HTTPConnection (server, port)

    def login (self, params, script):
        """S'autentifie sur le serveur en envoyant les paramètres 
        `params` au `script`
        """
        params = urllib.urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}

        self.handle.request ("POST", script, params, headers)
        r = self.handle.getresponse ()

        if r.status != 200:
            raise Exception ("Login failed: %s %s" % (r.status, r.reason))
        r.read ()

        bc = Cookie.BaseCookie ()
        bc.load (r.getheader ("set-cookie"))
        tmp = bc.output (header="Cookie:").replace (",", "").split("\n")
        cookies = []
        for line in tmp:
            cookie = line.replace ("Cookie: ", "").strip ()
            cookies.append (cookie)
        self.cookies = "; ".join (cookies)

    def get_response (self):
        r = None
        while r is None:
            try:
                r = self.handle.getresponse ()
            except:
                r = None
            time.sleep (1)
        return r

    def find_next_location (self, buffer):
        """Cherche dans `buffer` une redirection javascript pour trouver la 
        prochaine page a charger.
        """
        rc = ""

        root = etree.HTML (buffer)
        tmp = root.findall (".//script")
        script = tmp[len(tmp)-1]

        buffer = script.text
        match = "document.location='"
        i = buffer.rfind (match)
        if i >= 0:
            i += len (match)
            tmp = buffer[i:]
            j = tmp.find ("'\"")
            if j >= 0:
                rc = tmp[0:j]
        return rc

    def make_url (self, old, script):
        tmp = old.split ("/")
        tmp[len(tmp)-1] = script
        nextscript = "/".join(tmp)
        return nextscript

    def read_form (self, buffer):
        """Retourne un dictionnaire représentant un formulaire HTML présent 
        dans `buffer`.
        """
        script = ""
        params = {}

        root = etree.HTML(buffer)
        form = root.find (".//form")
        script = form.attrib['action']
        
        inputs = form.findall (".//input")
        for input in inputs:
            try:
                params[input.attrib['name']] = input.attrib['value']
            except:
                pass

        return (params, script)

    def export (self, params, script):
        """Méthode principale de la classe, automatise toute la mécanique 
        d'authentification et d'exportation des données.
        """
        params = urllib.urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain",
                "Cookie": self.cookies}

        self.handle.request ("POST", script, params, headers)
        r = self.get_response ()
        next = self.find_next_location (r.read ())
        nextscript = self.make_url (script, next)

        self.handle.request ("GET", nextscript, headers={"Cookie": self.cookies})
        r = self.get_response ()
        next = self.find_next_location (r.read ())
        nextscript = self.make_url (script, next)

        self.handle.request ("GET", nextscript, headers={"Cookie": self.cookies})
        r = self.get_response ()
        (params, next) = self.read_form (r.read ())

        nextscript = self.make_url (script, next)
        params = urllib.urlencode(params)
        self.handle.request ("POST", nextscript, params, headers)
        r = self.get_response ()
        content = r.read ()

        # Saloperie de PMB force le retour en iso crap
        return content.decode('iso-8859-1')
