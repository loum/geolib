CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

REST_IP = '172.20.1.101'
REST_PORT = '5150'
REST_SERVER = '%s:%s' % (REST_IP, REST_PORT)

META_REST_URL = 'http://%s/geolib/meta/v0.1/' % REST_SERVER
FREE_TEXT_URL = 'http://%s/geolib/meta/v0.1/search?' % REST_SERVER
AUDIT_URL = 'http://%s/geolib/audit/v0.1/recent' % REST_SERVER
POINTS_API = 'http://%s/geolib/image/v0.1/points?' % REST_SERVER
