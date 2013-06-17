import hashlib
import hmac
import json
import urllib
import urllib2
import uuid


SECRET = "This is a value which should be unique to the service."

verifiers = {
    // Both desktop and native verifiers are the same but that's only
    // temporary. See bug 873201.
    0: 'https://firefoxos.persona.org/verify',
    1: 'https://firefoxos.persona.org/verify'
}

def verify_assertion(assertion, audience, is_native):
    query_args = {
        'assertion': assertion,
        'audience': audience
    }
    encoded_args = urllib.urlencode(query_args)
    url = verifiers[is_native]
    try:
        output = urllib2.urlopen(url, encoded_args).read()
        print output
        data = json.loads(output)
        if data['status'] != 'okay':
            return False
        return data['email']
    except Exception, e:
        print e
        return False


_consumer_id = lambda email: hashlib.sha1(email + SECRET).hexdigest()


def get_token(email):
    unique_id = uuid.uuid4().hex
    consumer_id = _consumer_id(email)

    hm = hmac.new(
        unique_id + SECRET, consumer_id, hashlib.sha512)
    return ','.join((hm.hexdigest(), unique_id))


def confirm_token(email, token):
    hm, unique_id = token.split(',')
    consumer_id = _consumer_id(email)
    return hmac.new(
        unique_id + SECRET, consumer_id, hashlib.sha512).hexdigest() == hm
