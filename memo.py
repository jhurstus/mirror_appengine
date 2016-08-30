import os

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

MEMO_ID = 'jl'
MEMO_KEY = ndb.Key('Memo', MEMO_ID)


class Memo(ndb.Model):
  memo = ndb.StringProperty()


def getMemoText():
  memo_row = MEMO_KEY.get()
  if memo_row is not None:
    return memo_row.memo
  return ''


class MainPage(webapp2.RequestHandler):
  def get(self):
    memo_text = getMemoText()

    template_values = {
      'memo': memo_text
    }
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))


class MemoPost(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write(getMemoText())

  def post(self):
    text = self.request.get('memo')
    if text is None:
      text = ''
    else:
      # Cap memo length to 10k to prevent spamming of datastore.
      text = text[:10**4]

    memo = Memo(memo=text, id=MEMO_ID)
    memo.put()


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/memo', MemoPost),
    ])
