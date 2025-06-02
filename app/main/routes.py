from flask import render_template, redirect, url_for
from flask_login import current_user
from app.main import bp
from app.models import Poll

@bp.route('/')
@bp.route('/index')
def index():
    # 获取所有投票用于首页展示，按创建时间降序排列
    recent_polls = Poll.query.order_by(Poll.creation_timestamp.desc()).all()
    return render_template('main/index.html', title='首页', recent_polls=recent_polls)

@bp.route('/game')
def game():
    return render_template('main/game.html', title='井字棋游戏') 