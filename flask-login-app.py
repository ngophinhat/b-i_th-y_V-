from flask import Flask, render_template, request, session, redirect, url_for
import re

app = Flask(__name__)
app.secret_key = '222222222222222223333333333333333123123'

# Dữ liệu user cứng
USERS = {
    'user@example.com': 'password123'
}

def multiply(a, b):
    """Hàm nhân hai số"""
    return a * b

def validate_email(email):
    """Kiểm tra email có chứa @"""
    return '@' in email

def validate_password(password):
    """Kiểm tra password có ≥ 8 ký tự"""
    return len(password) >= 8

@app.route('/')
def index():
    """Trang chủ - redirect đến login nếu chưa đăng nhập"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Trang login"""
    error = None
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validate email
        if not email:
            error = '❌ Email không được để trống'
        elif not validate_email(email):
            error = '❌ Email phải chứa ký tự @'
        # Validate password
        elif not password:
            error = '❌ Mật khẩu không được để trống'
        elif not validate_password(password):
            error = '❌ Mật khẩu phải ≥ 8 ký tự'
        # Check username/password
        elif email not in USERS or USERS[email] != password:
            error = '❌ Email hoặc mật khẩu sai!\n(Dùng: user@example.com / password123)'
        else:
            # Đăng nhập thành công
            session['user'] = email
            return redirect(url_for('dashboard'))
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 400px;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 28px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 500;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            .error {
                background: #ffe0e0;
                color: #c00;
                padding: 12px;
                border-radius: 5px;
                margin-bottom: 20px;
                border-left: 4px solid #c00;
                white-space: pre-wrap;
                font-size: 13px;
            }
            .info {
                background: #e0f0ff;
                color: #004;
                padding: 12px;
                border-radius: 5px;
                margin-top: 20px;
                border-left: 4px solid #004;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Login</h1>
            ''' + (f'<div class="error">{error}</div>' if error else '') + '''
            <form method="POST">
                <div class="form-group">
                    <label for="email">📧 Email:</label>
                    <input type="text" id="email" name="email" placeholder="user@example.com" required>
                </div>
                <div class="form-group">
                    <label for="password">🔑 Mật khẩu:</label>
                    <input type="password" id="password" name="password" placeholder="Nhập mật khẩu" required>
                </div>
                <button type="submit">Đăng nhập</button>
            </form>
            <div class="info">
                <strong>Demo:</strong><br>
                Email: user@example.com<br>
                Mật khẩu: password123
            </div>
        </div>
    </body>
    </html>
    '''
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Trang dashboard sau login"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            a = float(request.form.get('a', 0))
            b = float(request.form.get('b', 0))
            result = multiply(a, b)
        except ValueError:
            error = '❌ Vui lòng nhập số hợp lệ'
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #eee;
                padding-bottom: 20px;
            }
            h1 {
                color: #333;
                font-size: 24px;
            }
            .user-info {
                font-size: 14px;
                color: #666;
            }
            .logout-btn {
                background: #e74c3c;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 13px;
                text-decoration: none;
                display: inline-block;
            }
            .logout-btn:hover {
                background: #c0392b;
            }
            .section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 18px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 6px;
                color: #555;
                font-weight: 500;
                font-size: 14px;
            }
            input {
                width: 100%;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            button {
                width: 100%;
                padding: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            .result {
                background: #d4edda;
                border-left: 4px solid #28a745;
                color: #155724;
                padding: 15px;
                border-radius: 5px;
                margin-top: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            .error {
                background: #ffe0e0;
                border-left: 4px solid #c00;
                color: #c00;
                padding: 15px;
                border-radius: 5px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Dashboard</h1>
                <div>
                    <span class="user-info">👤 ''' + session['user'] + '''</span><br>
                    <a href="/logout" class="logout-btn">Đăng xuất</a>
                </div>
            </div>
            
            <div class="section">
                <h2>🧮 Máy tính nhân số</h2>
                <form method="POST">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="a">Số thứ nhất (a):</label>
                            <input type="number" id="a" name="a" step="0.01" placeholder="Nhập số" required>
                        </div>
                        <div class="form-group">
                            <label for="b">Số thứ hai (b):</label>
                            <input type="number" id="b" name="b" step="0.01" placeholder="Nhập số" required>
                        </div>
                    </div>
                    <button type="submit">Tính toán (a × b)</button>
                </form>
                ''' + (f'<div class="result">✅ Kết quả: {result}</div>' if result is not None else '') + '''
                ''' + (f'<div class="error">{error}</div>' if error else '') + '''
            </div>
            
            <div class="section" style="background: #fff3cd; border-left: 4px solid #ffc107;">
                <strong style="color: #856404;">💡 Hướng dẫn:</strong><br>
                <small style="color: #856404;">Nhập hai số bất kỳ rồi nhấn "Tính toán" để nhân chúng lại với nhau.</small>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """Đăng xuất"""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)