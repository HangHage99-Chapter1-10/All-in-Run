from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.utsxudu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dball_in_run

from datetime import datetime

@app.route('/')
def writing():
    msg = request.args.get("msg")
    return render_template('writing.html', msg=msg)

@app.route('/detail')
def detail():
    msg = request.args.get("msg")
    return render_template('detail.html', msg=msg)

@app.route("/writing_list", methods=["POST"])
def save_writing():
    title_receive = request.form['title_give']
    place_receive = request.form['place_give']
    content_receive = request.form['content_give']
    channel_receive = request.form['channel_give']

    file = request.files["file_give"]  # 파일 업로드

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'  # 파일 업로드
    file.save(save_to)

    doc = {
        'title':title_receive,
        'place':place_receive,
        'content':content_receive,
        'channel':channel_receive,
        'file': f'{filename}.{extension}'
    }

    db.writing.insert_one(doc)

    return jsonify({'msg':'작성 완료!'})

@app.route("/comment_list", methods=["POST"])
def save_comment():
    comment_receive = request.form['comment_give']

    doc = {
              'comment': comment_receive
    }

    db.comment.insert_one(doc)

    return jsonify({})

@app.route("/writing_list", methods=["GET"])
def give_writing():
    writings = list(db.writing.find({}, {'_id': False}))
    return jsonify({'all_writing': writings})

@app.route("/comment_list", methods=["GET"])
def give_comment():
    comments = list(db.comment.find({}, {'_id': False}))
    return jsonify({'all_comment': comments})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)