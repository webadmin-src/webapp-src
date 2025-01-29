from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import time
import random
import hashlib

app = Flask(__name__)
app.secret_key = hashlib.sha256(str(time.time()).encode()).hexdigest()
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
Session(app)

# 用户配置
CORRECT_PASSWORD = ''  # 登录密码
VERIFICATION_CODE = '' # 验证码
ADJECTIVES = ['Happy', 'Clever', 'Swift', 'Brave', 'Gentle', 'Honest', 'Lucky', 'Wise']
NOUNS = ['Panda', 'Tiger', 'Eagle', 'Dolphin', 'Phoenix', 'Wolf', 'Lion', 'Dragon']

def generate_random_username():
    """生成随机用户名 格式：形容词_名词_数字"""
    return f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}_{random.randint(100, 999)}"

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        PASSWORD = request.form.get('password')
        if len(PASSWORD) != len(CORRECT_PASSWORD):
            return render_template('login.html', error='密码长度错误')
        for i in range(len(PASSWORD)):
            if PASSWORD[i] != CORRECT_PASSWORD[i]:
                return render_template('login.html', error='密码错误')
            time.sleep(0.1)
        session['logged_in'] = True
        session['username'] = generate_random_username()
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_code = request.form.get('code', '')
        if user_code == VERIFICATION_CODE:
            try:
                with open('/flag', 'r') as f:
                    flag = f.read().strip()
                return render_template('index.html', flag=flag)
            except Exception as e:
                print(f"读取flag文件失败: {e}")
                return render_template('index.html', error='系统错误，请联系系统管理员')
        return render_template('index.html', error='验证码错误，请重新输入')
    
    return render_template('index.html')

@app.route('/robots.txt', methods=['GET', 'POST'])
def robot():
    return send_from_directory(app.static_folder,'robots.txt')

@app.route('/webinfo.md', methods=['GET', 'POST'])
def webinfo():
    return send_from_directory(app.static_folder,'webinfo.md')
