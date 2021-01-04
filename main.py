from flask import *
from form import RegisterForm, LoginForm, Sell_form, Username, Password, Location, Mobile
import pymysql
import os

connection = pymysql.connect('localhost', 'danro', 'sithlord', 'shoplite')
cursor = connection.cursor()
app = Flask('__name__')
app.secret_key = '1233456'
app.config['UPLOAD_FOLDER'] = 'static/media/uploads'


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/register', methods=('POST', 'GET'))
def register():
    reg_form = RegisterForm()
    if request.method == "POST" and reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        mobile = reg_form.mobile.data
        location = reg_form.location.data
        query = f"INSERT INTO `register`(`username`, `email`, `password`, `number`, `location`) VALUES ('{username}','{email}','{password}','{mobile}','{location}')"
        cursor.execute(query)
        connection.commit()
        query_2 = f"SELECT  `email` FROM `register` WHERE email='{email}'"
        cursor.execute(query_2)
        result = cursor.rowcount
        if result == 1:
            flash(f'Account Created {username}', 'success')
            return redirect(url_for('login', title='Register', form=reg_form))
        else:
            flash(f'Invalid Registration', 'danger')
            return redirect(url_for('register', title='Register', form=reg_form))
    else:
        return render_template('register.html', title='Register', form=reg_form)


@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']


@app.route('/login', methods=('POST', 'GET'))
def login():
    logForm = LoginForm()
    session.pop('username', None)
    if request.method == "POST" and logForm.validate_on_submit():
        email = logForm.email.data
        password = logForm.password.data
        remember_me = logForm.remember_me.data
        query = f"SELECT `email`, `password` FROM `register` WHERE email='{email}' AND password='{password}'"
        cursor.execute(query)
        connection.commit()
        results = cursor.rowcount
        query_3 = f"SELECT  `username` FROM `register` WHERE email='{email}' AND password='{password}'"
        cursor.execute(query_3)
        if results == 1:
            username = cursor.fetchall()[0][0]
            if remember_me is True:
                session['username'] = username
                session.permanent = True
                username_in_use = session['username']
                query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
                cursor.execute(query_fetch_quantity)
                connection.commit()
                quantity_tot = cursor.fetchall()[0][0]
                if quantity_tot is None:
                    session['total_quantity'] = 0
                else:
                    session['total_quantity'] = int(float(quantity_tot))
                query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
                cursor.execute(query_fetch_price)
                connection.commit()
                price_tot = cursor.fetchall()[0][0]
                if price_tot is None:
                    session['absolute_total'] = 0
                else:
                    session['absolute_total'] = price_tot
                return redirect(url_for('index', form=logForm))
            else:
                session['username'] = username
                session.permanent = False
                username_in_use = session['username']
                query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
                cursor.execute(query_fetch_quantity)
                connection.commit()
                quantity_tot = cursor.fetchall()[0][0]
                if quantity_tot is None:
                    session['total_quantity'] = 0
                else:
                    session['total_quantity'] = int(float(quantity_tot))
                query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
                cursor.execute(query_fetch_price)
                connection.commit()
                price_tot = cursor.fetchall()[0][0]
                if price_tot is None:
                    session['absolute_total'] = 0
                else:
                    session['absolute_total'] = price_tot
                return redirect(url_for('index', form=logForm))
        else:
            flash('Invalid Account. Register and try again', 'danger')
            return redirect(url_for('login', title='Login', form=logForm))
    else:
        return render_template('login.html', title='Login', form=logForm)


@app.route('/logout')
def logout():
    session.pop('total_quantity', None)
    session.pop('absolute_total', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/account')
def account():
    return render_template('account.html', title='Account')


@app.route('/account/username', methods=["POST", "GET"])
def username():
    username_form = Username()
    if username_form.validate_on_submit():
        uname = username_form.username.data
        email = username_form.email.data
        query_update = f"UPDATE `register` SET `username`='{uname}' WHERE `email`='{email}'"
        cursor.execute(query_update)
        connection.commit()
        query_check = f"SELECT `username` FROM `register` WHERE `username` = '{uname}'"
        cursor.execute(query_check)
        connection.commit()
        results = cursor.rowcount
        if results == 1:
            session['username'] = uname
            flash('Account Updated', 'success')
        else:
            flash('Account not updated', 'danger')
        return redirect(url_for('username', form=username_form, title='Account-Username'))
    return render_template('username.html', form=username_form, title='Account-Username')


@app.route('/account/password', methods=["POST", "GET"])
def password():
    passwordform = Password()
    if passwordform.validate_on_submit():
        oldpassword = passwordform.oldpassword.data
        new_password = passwordform.password.data
        email = passwordform.email.data
        query_update = f"UPDATE `register` SET `password`='{new_password}' WHERE `email`='{email}' AND `password`='{oldpassword}'"
        cursor.execute(query_update)
        connection.commit()
        query_check = f"SELECT `password` FROM `register` WHERE `password` = '{new_password}'"
        cursor.execute(query_check)
        connection.commit()
        results = cursor.rowcount
        if results == 1:
            flash('Account Updated', 'success')
        else:
            flash('Account not updated', 'danger')
        return redirect(url_for('password', form=passwordform, title='Account-Password'))
    return render_template('password.html', form=passwordform, title='Account-Password')


@app.route('/account/number', methods=["POST", "GET"])
def number():
    numberform = Mobile()
    if numberform.validate_on_submit():
        new_number = numberform.mobile.data
        email = numberform.email.data
        query_update = f"UPDATE `register` SET `number`='{new_number}' WHERE `email`='{email}'"
        cursor.execute(query_update)
        connection.commit()
        query_check = f"SELECT `number` FROM `register` WHERE `number` = '{new_number}'"
        cursor.execute(query_check)
        connection.commit()
        results = cursor.rowcount
        if results == 1:
            flash('Account Updated', 'success')
        else:
            flash('Account not updated', 'danger')
        return redirect(url_for('number', form=numberform, title='Account-Number'))
    return render_template('number.html', form=numberform, title='Account-Number')


@app.route('/account/location', methods=["POST", "GET"])
def location():
    locationform = Location()
    if locationform.validate_on_submit():
        new_location = locationform.location.data
        email = locationform.email.data
        query_update = f"UPDATE `register` SET `location`='{new_location}' WHERE `email`='{email}'"
        cursor.execute(query_update)
        connection.commit()
        query_check = f"SELECT `location` FROM `register` WHERE `location` = '{new_location}'"
        cursor.execute(query_check)
        connection.commit()
        results = cursor.rowcount
        if results == 1:
            flash('Account Updated', 'success')
        else:
            flash('Account not updated', 'danger')
        return redirect(url_for('location', form=locationform, title='Account-Location'))
    return render_template('location.html', form=locationform, title='Account-Location')


@app.route('/products/buy', methods=['POST', 'GET'])
def buy():
    query = "SELECT * FROM products_in_stock"
    cursor.execute(query)
    connection.commit()
    products = cursor.fetchall()
    return render_template('buy.html', title='Buy', products=products)


@app.route('/add', methods=['POST', 'GET'])
def add():
    username_in_use = session['username']
    query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
    cursor.execute(query_fetch_quantity)
    connection.commit()
    quantity_tot = cursor.fetchall()[0][0]
    if quantity_tot is None:
        session['total_quantity'] = 0
    else:
        session['total_quantity'] = int(float(quantity_tot))
    query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
    cursor.execute(query_fetch_price)
    connection.commit()
    price_tot = cursor.fetchall()[0][0]
    if price_tot is None:
        session['absolute_total'] = 0
    else:
        session['absolute_total'] = price_tot
    quantity = int(request.form['quantity'])
    code = request.form['code']
    pdname = request.form['pdname']
    price = float(request.form['price'])
    mobile_no = request.form['mobile']
    if quantity is not None and code is not None and request.method == "POST":
        if quantity > 0:
            total_price_item = quantity * price
            query_if_code_exists = f"SELECT `quantity` FROM `goods_purchased` where username='{session['username']}' AND code='{code}'"
            cursor.execute(query_if_code_exists)
            connection.commit()
            rows_code = cursor.rowcount
            if rows_code >= 1:
                query_update = f"UPDATE `goods_purchased` SET `quantity`= `quantity` + '{quantity}',`total_price`=`total_price` + '{total_price_item}' WHERE username='{session['username']}' AND code='{code}' "
                cursor.execute(query_update)
                connection.commit()
                return redirect(url_for('buy'))
            else:
                query = f"INSERT INTO `goods_purchased`(`name`,`code`,`quantity`,`price`,`total_price`,`username`,`mobile`) VALUES ('{pdname}','{code}','{quantity}','{price}','{total_price_item}','{session['username']}','{mobile_no}')"
                cursor.execute(query)
                connection.commit()
                query_fetch_username = f"SELECT `username` FROM `goods_purchased` where username='{session['username']}'"
                cursor.execute(query_fetch_username)
                connection.commit()
                username = cursor.fetchone()[0]
                if session['username'] == username:
                    username_in_use = session['username']
                    query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
                    cursor.execute(query_fetch_quantity)
                    connection.commit()
                    quantity_tot = int(cursor.fetchall()[0][0])
                    session['total_quantity'] = quantity_tot
                    query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
                    cursor.execute(query_fetch_price)
                    connection.commit()
                    price_tot = cursor.fetchall()[0][0]
                    session['absolute_total'] = price_tot
                    return redirect(url_for('buy'))
                else:
                    return redirect(url_for('buy'))
    else:
        flash('Invalid quantity', 'danger')
    return redirect(url_for('login'))


@app.route('/report', methods=['POST', 'GET'])
def report():
    username_in_use = session['username']
    query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
    cursor.execute(query_fetch_quantity)
    connection.commit()
    quantity_tot = cursor.fetchall()[0][0]
    if quantity_tot is None:
        session['total_quantity'] = 0
    else:
        session['total_quantity'] = int(float(quantity_tot))
    query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
    cursor.execute(query_fetch_price)
    connection.commit()
    price_tot = cursor.fetchall()[0][0]
    if price_tot is None:
        session['absolute_total'] = 0
    else:
        session['absolute_total'] = price_tot
    if request.method == "POST":
        reporter_username = session['username']
        reported_code = request.form['code']
        reported_username = request.form['username']
        query_members = f"SELECT `email` , `number` FROM `register` WHERE `username`='{reported_username}'"
        cursor.execute(query_members)
        connection.commit()
        reported_results = cursor.fetchall()
        for reported_result in reported_results:
            email_result = reported_result[0]
            number_result = reported_result[1]
        query_report = f"INSERT INTO `reports`(`reporter`,`reported_username`,`reported_email`,`reported_number`,`reported_product`) VALUES ('{reporter_username}','{reported_username}','{email_result}','{number_result}','{reported_code}')"
        cursor.execute(query_report)
        connection.commit()
        flash('Report Successful', 'danger')
        return redirect(url_for('buy'))
    return redirect(url_for('buy'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    session.pop('username', None)
    query_members = f"SELECT * FROM `register`"
    cursor.execute(query_members)
    connection.commit()
    members = cursor.fetchall()
    query_products = f"SELECT * FROM `products_in_stock`"
    cursor.execute(query_products)
    connection.commit()
    products = cursor.fetchall()
    query_reports = f"SELECT * FROM `reports`"
    cursor.execute(query_reports)
    connection.commit()
    reports = cursor.fetchall()
    if request.method == 'POST':
        email = request.form['email']
        query_delete_member = f"DELETE FROM `register` WHERE `email`='{email}'"
        cursor.execute(query_delete_member)
        connection.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html', members=members, products=products, reports=reports)


@app.route('/admin_product', methods=['POST', 'GET'])
def admin_product():
    if request.method == 'POST':
        code = request.form['code']
        query_delete_product = f"DELETE FROM `products_in_stock` WHERE `code`='{code}'"
        cursor.execute(query_delete_product)
        connection.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html')


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    query = f"Select * from `goods_purchased`"
    cursor.execute(query)
    connection.commit()
    rows = cursor.rowcount
    if rows > 1:
        items = cursor.fetchall()
        if request.method == 'POST':
            code = request.form.get('code')
            price = float(request.form['itemprice'])
            quantity = int(request.form['itemquantity'])
            total_price_item = price * quantity
            query_subtract = f"UPDATE `goods_purchased` SET `quantity`= `quantity` - '{quantity}',`total_price`=`total_price` - '{total_price_item}' WHERE username='{session['username']}' AND code='{code}' "
            cursor.execute(query_subtract)
            connection.commit()
            query_delete = f"DELETE FROM `goods_purchased` WHERE `total_price` <= '0' OR `quantity` <= '0'"
            cursor.execute(query_delete)
            connection.commit()
            username_in_use = session['username']
            query_fetch_quantity = f"SELECT sum(`quantity`) FROM `goods_purchased` where username='{username_in_use}'"
            cursor.execute(query_fetch_quantity)
            connection.commit()
            quantity_tot = cursor.fetchall()[0][0]
            if quantity_tot is None:
                session['total_quantity'] = 0
            else:
                session['total_quantity'] = int(float(quantity_tot))
            query_fetch_price = f"SELECT sum(`total_price`) FROM `goods_purchased` where username='{username_in_use}'"
            cursor.execute(query_fetch_price)
            connection.commit()
            price_tot = cursor.fetchall()[0][0]
            if price_tot is None:
                session['absolute_total'] = 0
            else:
                session['absolute_total'] = price_tot
            return redirect(url_for('cart', items=items, title="Cart"))
        else:
            return render_template('cart.html', items=items, title="Cart")
    else:
        flash('No items in cart', 'primary')
        return render_template('cart.html', title="Cart")


@app.route('/products/sell', methods=['POST', 'GET'])
def sell():
    sell_form = Sell_form()
    name = sell_form.name.data
    price = sell_form.price.data
    code = sell_form.code.data
    image = sell_form.image.data
    details = sell_form.details.data
    mobile = sell_form.mobile.data
    if image and name and price and code and sell_form.validate_on_submit() and 'username' in session:
        username = session['username']
        filename = image.filename
        query3 = f"SELECT `code` FROM `products_in_stock` WHERE code='{code}'"
        cursor.execute(query3)
        connection.commit()
        results1 = cursor.rowcount
        if results1 == 1:
            flash('Duplicate Code. Try again', category='danger')
        else:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            query = f"INSERT INTO `products_in_stock`(`name`,`code`,`price`,`image`,`username`,`details`,`number`) VALUES ('{name}','{code}','{price}','{filename}','{username}','{details}','{mobile}')"
            cursor.execute(query)
            connection.commit()
            query2 = f"SELECT `code` FROM `products_in_stock` WHERE code='{code}'"
            cursor.execute(query2)
            connection.commit()
            results = cursor.rowcount
            if results == 1:
                flash('Product added', category='success')
            else:
                flash('Invalid entry.', category='danger')

        return render_template('sell.html', title='Create', form=sell_form)
    else:
        return render_template('sell.html', title='Create', form=sell_form)


if app.name == '__name__':
    app.run(debug=True, port=8000)
