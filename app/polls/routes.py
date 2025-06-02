from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.polls import bp
from app.polls.forms import CreatePollForm, VoteForm, EditPollForm, DeleteConfirmForm
from app.models import Poll, Option, VoteRecord
import json

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_poll():
    form = CreatePollForm()
    if form.validate_on_submit():
        poll = Poll(question=form.question.data, creator=current_user)
        
        # 添加选项
        options = [
            form.option1.data.strip(),
            form.option2.data.strip(),
            form.option3.data.strip(),
            form.option4.data.strip(),
            form.option5.data.strip()
        ]
        
        for option_text in options:
            if option_text:  # 只添加非空选项
                option = Option(text=option_text, poll=poll)
                db.session.add(option)
        
        db.session.add(poll)
        db.session.commit()
        
        flash('投票创建成功！', 'success')
        return redirect(url_for('polls.poll_detail', unique_id=poll.unique_share_id))
    
    return render_template('polls/create.html', title='创建投票', form=form)

@bp.route('/my_polls')
@login_required
def my_polls():
    polls = Poll.query.filter_by(user_id=current_user.id).order_by(Poll.creation_timestamp.desc()).all()
    return render_template('polls/my_polls.html', title='我的投票', polls=polls)

@bp.route('/poll/<unique_id>', methods=['GET', 'POST'])
def poll_detail(unique_id):
    poll = Poll.query.filter_by(unique_share_id=unique_id).first_or_404()
    
    # 检查用户是否已投票
    has_voted = False
    if current_user.is_authenticated:
        vote_record = VoteRecord.query.filter_by(poll_id=poll.id, user_id=current_user.id).first()
        has_voted = vote_record is not None
    else:
        # 对于未登录用户，使用IP地址检查
        ip_hash = VoteRecord.hash_ip(request.remote_addr)
        vote_record = VoteRecord.query.filter_by(poll_id=poll.id, voter_ip_hash=ip_hash).first()
        has_voted = vote_record is not None
    
    # 如果已投票，直接跳转到结果页面
    if has_voted:
        return redirect(url_for('polls.poll_results', unique_id=unique_id))
    
    form = VoteForm()
    # 动态设置选项
    form.option.choices = [(str(option.id), option.text) for option in poll.options]
    
    if form.validate_on_submit():
        selected_option = Option.query.get(int(form.option.data))
        if not selected_option or selected_option.poll_id != poll.id:
            abort(400)  # 无效的选项
        
        # 记录投票
        if current_user.is_authenticated:
            vote_record = VoteRecord(poll=poll, option=selected_option, user_id=current_user.id)
        else:
            ip_hash = VoteRecord.hash_ip(request.remote_addr)
            vote_record = VoteRecord(poll=poll, option=selected_option, voter_ip_hash=ip_hash)
        
        # 增加选项票数
        selected_option.vote_count += 1
        
        db.session.add(vote_record)
        db.session.commit()
        
        flash('投票成功！', 'success')
        return redirect(url_for('polls.poll_results', unique_id=unique_id))
    
    return render_template('polls/poll_detail.html', title=poll.question, poll=poll, form=form)

@bp.route('/poll/<unique_id>/results')
def poll_results(unique_id):
    poll = Poll.query.filter_by(unique_share_id=unique_id).first_or_404()
    options = poll.options.all()
    
    # 计算总票数
    total_votes = sum(option.vote_count for option in options)
    
    # 计算每个选项的百分比
    for option in options:
        if total_votes > 0:
            option.percentage = round((option.vote_count / total_votes) * 100)
        else:
            option.percentage = 0
    
    return render_template('polls/poll_results.html', title=f'结果: {poll.question}', poll=poll, options=options, total_votes=total_votes)

@bp.route('/poll/<unique_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_poll(unique_id):
    poll = Poll.query.filter_by(unique_share_id=unique_id).first_or_404()
    
    # 确保只有创建者才能修改投票
    if poll.user_id != current_user.id:
        flash('您没有权限修改此投票', 'danger')
        return redirect(url_for('polls.my_polls'))
    
    form = EditPollForm()
    
    # 获取投票的选项
    options = poll.options.all()
    
    if form.validate_on_submit():
        # 更新投票问题
        poll.question = form.question.data
        
        # 准备更新选项
        option_texts = [
            form.option1.data.strip(),
            form.option2.data.strip(),
            form.option3.data.strip(),
            form.option4.data.strip(),
            form.option5.data.strip()
        ]
        
        # 获取现有选项ID列表
        existing_option_ids = []
        if form.option_ids.data:
            try:
                existing_option_ids = json.loads(form.option_ids.data)
            except:
                existing_option_ids = []
        
        # 更新现有选项或创建新选项
        for i, option_text in enumerate(option_texts):
            if not option_text:  # 跳过空选项
                continue
                
            if i < len(existing_option_ids) and existing_option_ids[i]:
                # 更新现有选项
                option_id = existing_option_ids[i]
                option = Option.query.get(option_id)
                if option and option.poll_id == poll.id:
                    option.text = option_text
            else:
                # 创建新选项
                option = Option(text=option_text, poll=poll)
                db.session.add(option)
        
        # 删除不再使用的选项 (谨慎处理，以免丢失投票数据)
        if len(existing_option_ids) > len(option_texts):
            for i in range(len(option_texts), len(existing_option_ids)):
                if existing_option_ids[i]:
                    option = Option.query.get(existing_option_ids[i])
                    if option and option.poll_id == poll.id and option.vote_count == 0:
                        db.session.delete(option)
        
        db.session.commit()
        flash('投票修改成功！', 'success')
        return redirect(url_for('polls.my_polls'))
    
    # 填充表单
    if request.method == 'GET':
        form.question.data = poll.question
        
        # 填充选项字段
        option_ids = []
        for i, option in enumerate(options[:5]):  # 最多显示5个选项
            if i == 0:
                form.option1.data = option.text
            elif i == 1:
                form.option2.data = option.text
            elif i == 2:
                form.option3.data = option.text
            elif i == 3:
                form.option4.data = option.text
            elif i == 4:
                form.option5.data = option.text
            option_ids.append(option.id)
        
        # 将选项ID存储为JSON字符串
        form.option_ids.data = json.dumps(option_ids)
    
    return render_template('polls/edit.html', title='修改投票', form=form, poll=poll)

@bp.route('/poll/<unique_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_poll(unique_id):
    poll = Poll.query.filter_by(unique_share_id=unique_id).first_or_404()
    
    # 确保只有创建者才能删除投票
    if poll.user_id != current_user.id:
        flash('您没有权限删除此投票', 'danger')
        return redirect(url_for('polls.my_polls'))
    
    form = DeleteConfirmForm()
    
    # 计算总票数
    options = poll.options.all()
    total_votes = sum(option.vote_count for option in options)
    
    if form.validate_on_submit():
        # 删除投票及其所有相关数据
        db.session.delete(poll)  # 级联删除会自动删除关联的选项和投票记录
        db.session.commit()
        flash('投票已成功删除', 'success')
        return redirect(url_for('polls.my_polls'))
    
    return render_template('polls/delete.html', title='删除投票', form=form, poll=poll, total_votes=total_votes) 