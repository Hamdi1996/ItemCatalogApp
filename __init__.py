# Import main modules
from flask import Flask, render_template, g, request, redirect, url_for
from flask import flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from functools import wraps

# Import for Secure Access
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CLIENT_ID = json.loads(
    open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Phone Catalog Application"

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Decorator to check if user is logged in, if not redirect to login decorator.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access that page")
            return redirect('/login')
    return decorated_function


# JSON/API Endpoints for a specific category.
@app.route('/catalog/<string:category_name>/JSON')
@login_required
def categoryJSON(category_name):
    catalog = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=catalog.id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


# JSON/API Endpoints for a specific item.
@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
@login_required
def itemJSON(category_name, item_name):
    name_fix = item_name.replace("_", " ")
    item = session.query(CategoryItem).filter_by(name=name_fix).one()
    return jsonify(Item=[item.serialize])


# View homepage of catalog
@app.route('/')
@app.route('/catalog/')
def main():
    catalog = session.query(Category).all()
    items = session.query(CategoryItem).order_by(
        CategoryItem.id.desc()).limit(10)
    return render_template(
        'home.html',
        catalog=catalog,
        items=items,
        isAuthenticated=isAuthenticated())


# View catalog category
@app.route('/catalog/<string:category_name>/')
def category(category_name):
    catalog = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category.id).all()
    numberOfItems = session.query(CategoryItem).filter_by(
        category_id=category.id).count()
    return render_template(
        'category.html',
        catalog=catalog,
        category=category,
        items=items,
        numberOfItems=numberOfItems,
        isAuthenticated=isAuthenticated())


# View catalog item
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item(category_name, item_name):
    item = session.query(CategoryItem).filter_by(
        name=item_name.replace("_", " ")).first()
    return render_template(
        'item.html',
        item=item,
        isAuthenticated=isAuthenticated())


# Add a new item to the database
@app.route('/catalog/add_item/', methods=["GET", "POST"])
@login_required
def addItem():
    categories = session.query(Category).all()
    item_data = {
        'name': "Product Name",
        'description': "Product Description...",
        'os': "Operating system",
        'category_id': ""
    }
    if request.method == 'POST':
        catID = session.query(Category).filter_by(
            name=request.form['itemCategory'].strip()).one()
        # If item name is not in databse add item
        if session.query(CategoryItem).filter_by(
                name=request.form['itemName'].strip()).first() is None:
            newItem = CategoryItem(
                name=request.form['itemName'].strip(),
                description=request.form['itemDescription'].strip(),
                os=request.form['itemOS'].strip(),
                category_id=catID.id,
                user_id=getUserID(login_session['email'])
            )
            session.add(newItem)
            session.commit()
            flash("Item Added.")
            return redirect(url_for("main"))
        # If item name IS in database, let end user know it already exists.
        else:
            flash("Item already exists")
            item_data['description'] = request.form['itemDescription'].strip()
            item_data['os'] = request.form['itemOS'].strip()
            item_data['category_id'] = request.form['itemCategory'].strip()
            return render_template(
                'add_item.html',
                categories=categories,
                item_data=item_data)
    else:
        return render_template(
            'add_item.html',
            categories=categories,
            item_data=item_data)


# Edit an existing item in the database.
@app.route('/catalog/<string:item_name>/edit', methods=["GET", "POST"])
@login_required
def editItem(item_name):
    item = session.query(CategoryItem).filter_by(
        name=item_name.replace("_", " ")).first()
    categories = session.query(Category).all()
    if request.method == 'POST' and item.user_id == getUserID(
            login_session['email']):
        catID = session.query(Category).filter_by(
            name=request.form['itemCategory'].strip()).one()
        # If the query of the item matches the query of submission of the name
        # allow database object to keep name.
        if session.query(CategoryItem).filter_by(
                id=item.id).first() == session.query(CategoryItem).filter_by(
                name=request.form['itemName'].strip()).first():
            item.name = request.form['itemName'].strip()
        # If the name submitted does not exist in the database all the change
        # of name
        elif session.query(CategoryItem).filter_by(
                name=request.form['itemName'].strip()).first() is None:
            item.name = request.form['itemName'].strip()
        # If ID's don't match the name and the name already exists than return
        # flash error.
        else:
            flash("Item name already exists.")
            return render_template(
                'edit_item.html',
                item_name=item_name,
                item=item,
                categories=categories)
        item.description = request.form['itemDescription'].strip()
        item.os = request.form['itemOS'].strip()
        item.category_id = catID.id
        item.user_id = getUserID(login_session['email'])
        session.add(item)
        session.commit()
        flash("Item Updated")
        return redirect(url_for('category', category_name=catID.name))
    elif item.user_id == getUserID(login_session['email']):
        return render_template(
            'edit_item.html',
            item_name=item_name,
            item=item,
            categories=categories)
    else:
        flash("You are not allowed to edit that item.")
        return redirect(url_for('main'))


# Delete item out of databse
@app.route('/catalog/<string:item_name>/delete', methods=["GET", "POST"])
@login_required
def deleteItem(item_name):
    item = session.query(CategoryItem).filter_by(
        name=item_name.replace("_", " ")).one()
    if request.method == 'POST' and item.user_id == getUserID(
            login_session['email']):
        session.delete(item)
        session.commit()
        flash("Item Deleted.")
        return redirect(url_for('main'))
    elif item.user_id == getUserID(login_session['email']):
        return render_template('delete_item.html', item_name=item_name)
    else:
        flash("You are not allowed to delete that item")
        return redirect(url_for('main'))


# Add category to database
@app.route('/catalog/add_category/', methods=["GET", "POST"])
@login_required
def addCategory():
    categories = session.query(Category).all()
    if request.method == 'POST':
        catName = request.form['categoryName'].strip()
        # Check if category already exists.
        if session.query(Category).filter_by(
                name=catName).scalar() is not None:
            flash("Category already exists.")
            return render_template('add_category.html', categories=categories)
        # If not, create new category
        else:
            newCategory = Category(
                name=catName,
                user_id=getUserID(login_session['email'])
            )
            session.add(newCategory)
            session.commit()
            flash("New Category Added")
            return redirect(url_for("main"))
    else:
        return render_template('add_category.html', categories=categories)


# Delete category and items associated with category from database
@app.route(
    '/catalog/<string:category_name>/delete_category/',
    methods=[
        "GET",
        "POST"])
@login_required
def deleteCategory(category_name):
    category = session.query(Category).filter_by(
        name=category_name.replace("_", " ")).one()
    if request.method == 'POST' and category.user_id == getUserID(
            login_session['email']):
        session.delete(category)
        session.commit()
        flash("Category and Items deleted.")
        return redirect(url_for('main'))
    elif category.user_id == getUserID(login_session['email']):
        return render_template(
            'delete_category.html',
            category_name=category_name)
    else:
        flash("You are not allowed to delete that category")
        return redirect(url_for('main'))


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Login with a facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token
        exchange we have to split the token first on commas and
        select the first index which gives us the key : value for
        the server access token then we split it on colons to pull
        out the actual token value and replace the remaining quotes
        with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# Disconnect facebook account
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Login with a Google Account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Create new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Get user as an object by their user ID
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Look up user ID by email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# Authentication check for login button.
def isAuthenticated():
    if 'username' not in login_session:
        return False
    else:
        return True


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('main'))
    else:
        flash("You were not logged in")
        return redirect(url_for('main'))


# Run application for debugging
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
