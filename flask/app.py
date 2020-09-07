import os
import io
import time
import numpy as np
import cv2
# import dlib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
# from werkzeug import secure_filename
from pathlib import Path
import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, request, redirect, url_for
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
from run import pose_estimate


# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'

POSED_FOLDER = './pose_estimated'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POSED_FOLDER'] = POSED_FOLDER


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hello')
def index():
    return 'Hello World!'


@app.route('/post', methods=['POST'])
def post_json():
    pass


@app.route('/show-data', methods=['POST'])
def show_json():
    pass


@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['POSED_FOLDER'], filename)


html = '''
        <!doctype html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>
                    ファイルをアップロードして判定しよう
                </title>
            </head>
            <body>
                <h1>
                    ファイルをアップロードして判定しよう
                </h1>
                <form method = post enctype = multipart/form-data>
                <p><input type=file name = file>
                <input type = submit value = Upload>
                </form>
            </body>
        '''


# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # 保存した画像に対してpose_estimateし、bone推定した画像のpathをもらう
            path = pose_estimate({'image': os.path.join(app.config['UPLOAD_FOLDER'], filename)})

            # アップロード後のページに転送
            return redirect(url_for('uploaded_file', filename=path))
        else:
            html_lines = html.split('\n')
            html_lines = html_lines[:-1] + ['<h1>', 'Sth went wrong', '</h1>'] + html_lines[-1]
            return '\n'.join(html_lines)
            
    return html


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))